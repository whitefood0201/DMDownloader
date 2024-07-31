import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter as tk
import dmdownloader.downloader.asyntk as asyntk
import dmdownloader.downloader.sitelib.service as service
import dmdownloader.downloader.components as cmp
import dmdownloader.functional.FLfunctions as fl
import dmdownloader.functional.lambdas as lm

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
        self.frames["setting_frame"] = InitFrame(master=container, controller=self)
        self.frames["waiting_frame"] = WaitingFrame(master=container, controller=self)
        self.frames["main_frame"] = VetcScrollFrame(lambda master: MainFrame(master=master, favorites=favorites, controller=self), 800, height, master=container)

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
        """ 
            创建 AnimeFrame，根据anime_info。
            anime_info 格式为：
                {
                    "title": "title", 
                    "from": "", # baha or bili
                    "eps": {
                        "ep_title": "epid",
                        ...
                    }
                }
        """
        height = len(anime_info["eps"]) <= 8 and 490 or 0
        self.frames["anime_info"] = VetcScrollFrame(lambda master: AnimeFrame(master=master, anime_info=anime_info, controller=self), 800, height, master=self.container)
        self.frames["anime_info"].grid(row=0,column=0,sticky="nsew")
        self.show_frame("anime_info")

class InitFrame(ttk.Frame):
    """ 初始界面，输入UserAgent和cookie """
    def __init__(self, master=None, controller=None):
        super().__init__(master, relief="sunken")
        self.master = master
        self.controller = controller
        self.global_config: dict = controller.app_config
        self.initBindVariables()

        ttk.Label(self, text="设置", style="title.TLabel").pack(ipady=20)
        self.get_input_frame().pack()
        self.get_btn_frame().pack()

    def initBindVariables(self):
        def defineVar(key: str, value) -> tk.Variable:
            var = None
            if isinstance(value, int): var = tk.IntVar(value=value)
            elif isinstance(value, str): var = tk.StringVar(value=value)
            elif isinstance(value, bool): var = tk.BooleanVar(value=value)
            elif isinstance(value, float): var = tk.DoubleVar(value=value)
            else: raise NotImplementedError("only support int, str, bool and float")
            return var
        self.vars = fl.dict_map(defineVar, self.global_config)

        def save(config: dict):
            def do(key: str, var: tk.Variable) -> None:
                config[key] = var.get()
            return do
        self.save_config = lambda: fl.dict_map(save(self.global_config), self.vars)
    
    def get_input_frame(self):
        fra = ttk.Frame(self)

        cmp.inputBox(fra, "UserAgent:", self.vars["user_agent"], (FONT_NAME, 10), "ep_title.TLabel").pack()
        cmp.inputBox(fra, "Cookie:", self.vars["cookie"], (FONT_NAME, 10), "ep_title.TLabel").pack()

        opt_fra = ttk.Frame(fra)
        fra_top, self.opt_top = cmp.optBox(opt_fra, "顶部弹幕过滤", self.vars["top_filter"],"ep_title.TLabel")
        fra_top.pack(side="left", padx=30)
        fra_bot, self.opt_bot = cmp.optBox(opt_fra, "底部弹幕过滤", self.vars["bottom_filter"], "ep_title.TLabel")
        fra_bot.pack(side="left", padx=30)
        fra_zh, self.opt_zh = cmp.optBox(opt_fra, "繁转换", self.vars["open_zhconv"], "ep_title.TLabel")
        fra_zh.pack(side="left", padx=30)
        fra_raw, self.opt_raw = cmp.optBox(opt_fra, "下载源文件", self.vars["download_raw"], "ep_title.TLabel")
        fra_raw.pack(side="left", padx=30)
        opt_fra.pack()

        return fra
    
    def get_btn_frame(self):
        fra = ttk.Frame(self)
        def handler():
            self.save_config()
            self.controller.show_frame("main_frame")
        ttk.Button(fra, text="确认", style="favortes.TButton", command=handler).pack()
        return fra

class MainFrame(ttk.Frame):

    """ 主界面，提供搜索栏和收藏栏 """
    def __init__(self, master=None, controller=None, favorites=None):
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
    """ 动画展示及下载界面 """
    def __init__(self, master=None, controller=None, anime_info=None):
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
        eps_frame = ttk.Frame(self)

        for ep in eps.keys():
            fra = ttk.Frame(self)
            epid = eps[ep]
            ttk.Label(master=fra, text=ep, width=50, style="ep_title.TLabel").pack(side="left", padx=10)
            def handler(event, epid=epid, ofile=ep, site=site):
                self.download(event, epid, ofile, site)
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
    """ 加载界面 """
    def __init__(self, master=None, controller=None):
        super().__init__(master=master, relief="sunken")
        self.master = master
        self.controller = controller
        text = tk.StringVar()
        text.set("\n\n\n加载中")
        self.label = ttk.Label(master=self, textvariable=text, style="waiting.TLabel")

        def reflash_text():
            count = [0]
            def reflash():
                text.set("\n\n\n加载中" + "." * (count[0] % 4))
                count[0] = count[0]+1
                self.label.after(500, reflash)
            return reflash

        self.label.after(0, reflash_text())
        self.label.pack()
    
# 带滚动条的Frame
class VetcScrollFrame(ttk.Frame):
    
    ## 通过往canva上加frame(inner_frame)实现，为解决innerframe宽高需要手动传入宽高
    def __init__(self, inner_frame, inner_frame_width, inner_frame_height, master=None):
        super().__init__(master)
        self.master = master

        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        canva = tk.Canvas(self,width=width, height=height, bg="gray")
        scroll = ttk.Scrollbar(self, orient="vertical", command=canva.yview)
        canva.config(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canva.pack(side="left", fill="both", expand=True)

        self.inner_frame = inner_frame(self)
        ## canva上画inner_Frame，需要宽高
        canva.create_window((0,0), window=self.inner_frame,  width=inner_frame_width, height=inner_frame_height)

        # 通过以下方式调整canvas的scrollable区域
        def on_mousewheel(event):
            canva.yview_scroll(-1 * int(event.delta / 120), 'units')       
        self.inner_frame.bind("<Configure>", lambda e: canva.configure(scrollregion=canva.bbox('all')))
        self.inner_frame.bind("<Enter>", lambda e: self.master.bind_all('<MouseWheel>', on_mousewheel))
        self.inner_frame.bind("<Leave>", lambda e: self.master.unbind_all('<MouseWheel>'))
