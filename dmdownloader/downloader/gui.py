import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter as tk
import dmdownloader.downloader.asyntk as asyntk
import dmdownloader.downloader.sitelib.service as service
import dmdownloader.downloader.components as cmp
import dmdownloader.functional.FLfunctions as fl

FONT_NAME = "微软雅黑"

class DownloaderApp(tk.Tk):
    def __init__(self, cfg, favorites, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # 自身属性
        self.title("DanmakuDownloader")
        self.geometry("800x490+280+130") 
        self.config(bg="gray")
        self.resizable(False, False)
        self.app_config = cfg
        self.favorites = favorites

        # 样式管理
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=(FONT_NAME, 14), background="gray")
        style.configure("title.TLabel", font=(FONT_NAME, 22, "bold"), foreground="light blue", background="gray")
        style.configure("waiting.TLabel", font=(FONT_NAME, 36), foreground="black", background="gray")
        style.configure("anime_title.TLabel", font=(FONT_NAME, 26), foreground="white", background="gray")
        style.configure("ep_title.TLabel", font=(FONT_NAME, 16), foreground="light gray", background="gray")
        style.configure("TButton", font=(FONT_NAME, 14), background="white")
        style.configure("favortes.TButton", font=(FONT_NAME, 12), background="white")
        style.map("ep_button_downloading.TButton", background=[('!disabled', 'light gray')])
        style.map('ep_button_success.TButton', background=[('!disabled', 'lime')])
        style.map('ep_button_failure.TButton', background=[('!disabled', 'red')])

        # 界面切换处理
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        # 初始化界面
        self.frames = {}
        height = len(favorites) <= 9 and 490 or 0
        self.frames["setting_frame"] = cmp.VetcScrollFrame(lambda master: SettingFrame(master=master, controller=self), 800, 0, master=container)
        self.frames["waiting_frame"] = WaitingFrame(master=container, controller=self)
        self.frames["main_frame"] = cmp.VetcScrollFrame(lambda master: MainFrame(master=master, favorites=favorites, controller=self), 800, height, master=container)

        self.frames["main_frame"].grid(row=0, column=0, sticky="nsew")
        self.frames["setting_frame"].grid(row=0, column=0, sticky="nsew")
        self.frames["waiting_frame"].grid(row=0, column=0, sticky="nsew")

        # 初始化 tk 异步任务处理对象
        self.asyn_event = asyntk.AsyncEvent(self)

        self.show_frame("main_frame")

    def show_frame(self, page_name):
        """ 切换页面 """
        frame = self.frames[page_name]
        if (page_name != "anime_info") & ("anime_info" in self.frames.keys()):
            self.frames["anime_info"].destroy()
        frame.tkraise()

    def create_anime_info_frame(self, anime_info):
        height = len(anime_info["eps"]) <= 8 and 490 or 0
        self.frames["anime_info"] = cmp.VetcScrollFrame(lambda master: AnimeFrame(master=master, anime_info=anime_info, controller=self), 800, height, master=self.container)
        self.frames["anime_info"].grid(row=0,column=0,sticky="nsew")
        self.show_frame("anime_info")

class SettingFrame(ttk.Frame):
    
    def __init__(self, master=None, controller=None):
        """ 初始界面，输入UserAgent和cookie """
        super().__init__(master, relief="sunken")
        self.master = master
        self.controller = controller
        self.global_config: dict = controller.app_config
        self.vars, self.save_config = self.initBindVariables()

        ttk.Label(self, text="设置", style="title.TLabel").pack(pady=5)
        self.get_input_frame().pack()
        self.get_btn(self).pack(pady=20)

    def initBindVariables(self):
        def defineVar(key: str, value) -> tk.Variable:
            var = None
            if isinstance(value, bool): var = tk.BooleanVar(value=value)
            elif isinstance(value, int): var = tk.IntVar(value=value)
            elif isinstance(value, str): var = tk.StringVar(value=value)
            elif isinstance(value, float): var = tk.DoubleVar(value=value)
            else: raise NotImplementedError("only support int, str, bool and float")
            return var
        vars = fl.dict_map(defineVar, self.global_config)

        def save(config: dict):
            def do(key: str, var: tk.Variable) -> None:
                config[key] = var.get() if not isinstance(var, tk.StringVar) else str.strip(var.get())
            return do
        save_config = lambda: fl.dict_map(save(self.global_config), vars)

        return vars, save_config
    
    def get_input_frame(self):
        FONT = (FONT_NAME, 12)
        STYLE = "ep_title.TLabel"
        fra = ttk.Frame(self)
        
        web_fra = ttk.Frame(fra)
        cmp.strInputBox(web_fra, "UserAgent:", 75, self.vars["user_agent"], FONT, STYLE).pack()
        cmp.strInputBox(web_fra, "Cookie:", 75, self.vars["cookie"], FONT, STYLE).pack()
        
        opt_fra = ttk.Frame(fra)
        cmp.optBox(opt_fra, "顶部弹幕过滤", self.vars["top_filter"], FONT, STYLE).pack(side="left", padx=30)
        cmp.optBox(opt_fra, "底部弹幕过滤", self.vars["bottom_filter"], FONT, STYLE).pack(side="left", padx=30)
        cmp.optBox(opt_fra, "繁转换", self.vars["open_zhconv"], FONT, STYLE).pack(side="left", padx=30)
        cmp.optBox(opt_fra, "下载源文件", self.vars["download_raw"], FONT, STYLE).pack(side="left", padx=30)

        int_fra = ttk.Frame(fra)
        cmp.intInputBox(int_fra, "偏移上限：", 6, self.vars["offset"], FONT, STYLE).pack(side="left", padx=20)
        cmp.intInputBox(int_fra, "最大行数：", 6, self.vars["line_count"], FONT, STYLE).pack(side="left", padx=20)
        cmp.intInputBox(int_fra, "底部偏移：", 6, self.vars["bottom_offset"], FONT, STYLE).pack(side="left", padx=20)
        cmp.intInputBox(int_fra, "字体大小：", 6, self.vars["font_size"], FONT, STYLE).pack(side="left", padx=20)

        str_fra = ttk.Frame(fra)
        cmp.strInputBox(str_fra, "文件后缀：", 20, self.vars["suffix"], FONT, STYLE).pack(side="left", padx=20)
        cmp.strInputBox(str_fra, "分辨率：", 20, self.vars["resolution"], FONT, STYLE).pack(side="left", padx=20)
        cmp.strInputBox(str_fra, "字体名称：", 20, self.vars["font_name"], FONT, STYLE).pack(side="left", padx=20)
        str_fra_2 = ttk.Frame(fra)
        cmp.strInputBox(str_fra_2, "下载路径：", 25, self.vars["download_path"], FONT, STYLE).pack(side="left", padx=20)
        cmp.strInputBox(str_fra_2, "ass头文件路径：", 25, self.vars["ass_head"], FONT, STYLE).pack(side="left", padx=20)
        
        web_fra.pack(pady=10)
        opt_fra.pack(pady=10)
        int_fra.pack(pady=10)
        str_fra.pack(pady=10)
        str_fra_2.pack(pady=10)
        return fra
    
    def get_btn(self, master):
        def handler():
            self.save_config()
            self.controller.show_frame("main_frame")
        return ttk.Button(master, text="确认", style="favortes.TButton", command=handler)

class MainFrame(ttk.Frame):

    def __init__(self, master=None, controller=None, favorites=None):
        """ 主界面，提供搜索栏和收藏栏 """
        super().__init__(master, relief="sunken")
        self.master = master
        self.controller = controller

        def handler(self=self):
            self.controller.show_frame("setting_frame")
        ttk.Button(master=self, text="设置", command=handler, width=5).pack(anchor="nw", side="top", padx=20, pady=5)
        self.get_blank_frame().pack(side="top")
        self.get_search_frame().pack(side="top", pady=10)
        self.get_favorite_frame(favorites).pack(side="top")

    def get_blank_frame(self):
        fra = ttk.Frame(self)
        ttk.Label(fra, text="DMDownloader", style="title.TLabel").pack()
        return fra

    def get_search_frame(self):
        fra01 = ttk.Frame(self)

        text = tk.StringVar()
        self.eny = ttk.Entry(fra01, width=75, font=(FONT_NAME, 10), textvariable=text)
        self.btn = ttk.Button(fra01, text="搜索", width=5, command=lambda:self.search(text.get()))

        self.eny.pack(side="left", padx=2, ipady=1) 
        self.btn.pack(side="left")
        return fra01

    def get_favorite_frame(self, favorites):
        fra02 = ttk.Frame(self)

        for key in favorites.keys():
            def handler(self=self, url=favorites[key]):
                self.search(url)
            ttk.Button(fra02, text=key, style="favortes.TButton", command=handler).pack(pady=2)

        return fra02

    
    def search(self, url):
        """ search button event handler """
        def on_success(result, app=self.controller):
            app.create_anime_info_frame(result)

        def on_failure(exception, app=self.controller): 
            msg.showerror(title="错误", message=repr(exception))
            app.show_frame("main_frame")

        self.controller.asyn_event.submit(service.search, url, self.controller.app_config).then(on_success).catch(on_failure)
        self.controller.show_frame("waiting_frame")


class AnimeFrame(ttk.Frame):
    
    def __init__(self, master=None, controller=None, anime_info=None):
        """ 动画展示及下载界面 """
        super().__init__(master=master, relief="sunken")
        self.master = master
        self.controller = controller

        # bili / baha
        site = anime_info["from"]
        title = anime_info["title"]
        eps = anime_info["eps"]

        fra = ttk.Frame(self)
        ttk.Label(master=fra, text=title, style="anime_title.TLabel").pack(side="left")

        def handler(self=self):
            self.controller.show_frame("main_frame")
        ttk.Button(master=self, text="退回", command=handler, width=5).pack(anchor="ne", side="top", padx=10, pady=10)
        fra.pack(anchor="nw",pady=5, padx=40)
        self.get_eps_frame(eps, site).pack()
        ttk.Label(master=self, text=" ").pack()

    def get_eps_frame(self, eps, site):
        """ 
            根据`anime_info`创建
            anime_info 格式为：
            ```
                {
                    "title": "title", 
                    "from": "", # baha or bili
                    "eps": [{
                        "title": title,
                        "id": id},
                        {...
                    ]
                }
            ```
        """
        eps_frame = ttk.Frame(self)

        for ep in eps:
            fra = ttk.Frame(self)
            epid = ep["id"]
            title = ep["title"]
            ttk.Label(master=fra, text=title, width=50, style="ep_title.TLabel").pack(side="left", padx=10)
            def handler(event, id=epid, title=title, site=site):
                self.download(event, id, title, site)
            btn = ttk.Button(master=fra, text="下载", width=6, style="ep_button.TButton")
            btn.bind("<1>", handler)
            btn.pack()

            fra.pack(anchor="w", padx=50, pady=2)
        
        return eps_frame
    
    def download(self, event, epid, ofile, site):
        """ download button event handler """
        widget = event.widget

        def on_success(result, button=widget):
            button.config(style="ep_button_success.TButton")
        
        def on_failure(exception: Exception, button=widget):
            msg.showerror(title="错误", message=repr(exception))
            button.config(style="ep_button_failure.TButton")

        self.controller.asyn_event.submit(service.download, epid, site, ofile, self.controller.app_config).then(on_success).catch(on_failure)

        widget.config(style="ep_button_downloading.TButton")


class WaitingFrame(ttk.Frame):
    
    def __init__(self, master=None, controller=None):
        """ 加载界面 """
        super().__init__(master=master, relief="sunken")
        self.master = master
        self.controller = controller

        text = tk.StringVar(value="\n\n\n加载中")
        self.label = ttk.Label(master=self, textvariable=text, style="waiting.TLabel")

        def reflash_text():
            count = 0
            def reflash():
                nonlocal count
                text.set("\n\n\n加载中" + "." * (count % 4))
                count += 1
                self.label.after(500, reflash)
            return reflash
        self.label.after(0, reflash_text())
        self.label.pack()