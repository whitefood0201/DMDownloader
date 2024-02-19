import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter as tk
import dmdownloader.downloader.asyntk as asyntk
import dmdownloader.downloader.sitelib.service as service

FAVORITES_PATH = "./resource/favorites.json"
CONFIG_PATH = "./resource/config.json"
FONT_NAME = "微软雅黑"

class DownloaderApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # 载入config
        try:
            self.app_config = service.load_json(CONFIG_PATH)
        except IOError:
            msg.showerror(title="错误", message="配置文件载入错误")
            exit(1)

        # 载入favorites
        favorites = {}
        try:
            favorites = service.load_json(FAVORITES_PATH)
        except IOError:
            pass

        # 自身属性
        self.title("DanmakuDownloader")
        self.geometry("800x490+280+130") 
        self.config(bg="gray")
        self.resizable(False, False)

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
        self.frames["waiting_frame"] = WaitingFrame(master=container, controller=self)
        self.frames["main_frame"] = VetcScrollFrame(lambda master: MainFrame(master=master, favorites=favorites, controller=self), 800, height, master=container)

        self.frames["waiting_frame"].grid(row=0, column=0, sticky="nsew")        
        self.frames["main_frame"].grid(row=0, column=0, sticky="nsew")

        # 初始化 tk 异步任务处理对象
        self.asyn_event = asyntk.AsyncEvent(self)

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
        height = len(anime_info["eps"]) <= 10 and 490 or 0
        self.frames["anime_info"] = VetcScrollFrame(lambda master: AnimeFrame(master=master, anime_info=anime_info, controller=self), 800, height, master=self.container)
        self.frames["anime_info"].grid(row=0,column=0,sticky="nsew")
        self.show_frame("anime_info")


class MainFrame(ttk.Frame):
    """ 主界面，提供搜索栏和收藏栏 """
    def __init__(self, master=None, controller=None, favorites=None):
        super().__init__(master, relief="sunken")
        self.master = master
        self.controller = controller

        self.get_blank_frame().pack(side="top")
        self.get_search_frame().pack(side="top", pady=10)
        self.get_favorite_frame(favorites).pack(side="top")

    def get_blank_frame(self):
        fra = ttk.Frame(self)
        ttk.Label(fra, text="\nDMDownloader", style="title.TLabel").pack()
        return fra

    def get_search_frame(self):
        fra01 = ttk.Frame(self)

        text = tk.StringVar()
        self.eny = ttk.Entry(fra01, width=75, font=(FONT_NAME, 10), textvariable=text)

        def handler(self=self, url=text):
            self.search(text.get())
        self.btn = ttk.Button(fra01, text="搜索", width=5, command=handler)

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
