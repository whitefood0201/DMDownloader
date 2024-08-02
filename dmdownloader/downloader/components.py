import tkinter as tk
import tkinter.ttk as ttk

def optButton(master: tk.Misc, onOn, onOff) -> tk.Scale:
    def on_slide(value):
        if "0" == value:
            onOff()
            scale.config(troughcolor="gray")
        else:
            onOn()
            scale.config(troughcolor="light gray")
    scale = tk.Scale(master=master, from_=0, to=1, orient=tk.HORIZONTAL, length=100, width=20,
                        sliderlength=20, showvalue=0, bg="#ffffff", troughcolor="gray", command=on_slide)
    scale.set(1)
    return scale

def bindBoolVar(boolVar: tk.Variable):
    def onOn():
        boolVar.set(True)
    def onOff():
        boolVar.set(False)
    return onOn, onOff

def strInputBox(master: tk.Misc, labelText: str, width: int, bindVar: tk.Variable, font, style: str) -> ttk.Frame:
    fra = ttk.Frame(master=master)
    ttk.Label(master=fra, text=labelText, style=style).pack(anchor="w")
    ttk.Entry(master=fra, width=width, font=font, textvariable=bindVar).pack()

    return fra

def intInputBox(master: tk.Misc, labelText: str, width: int, bindVar: tk.Variable, font, style: str) -> ttk.Frame:
    fra = ttk.Frame(master=master)
    ttk.Label(master=fra, text=labelText, font=font, style=style).pack(anchor="w", side="left")
    ttk.Entry(master=fra, width=width, font=font, textvariable=bindVar,
              validate='all', validatecommand=(master.register(lambda P: str.isdigit(P) or str(P) == ""), '%P')).pack(side="left")
    return fra


def optBox(master: tk.Misc, labelText: str, bindVar: tk.BooleanVar, font, style: str) -> ttk.Frame:
    fra = ttk.Frame(master=master)
    ttk.Label(master=fra, text=labelText, font=font, style=style).pack()
    opt = optButton(fra, *bindBoolVar(bindVar))
    opt.set(bindVar.get())
    opt.pack(pady=10)
    return fra


class VetcScrollFrame(ttk.Frame):
    
    ## 通过往canva上加frame(inner_frame)实现，为解决innerframe宽高需要手动传入宽高
    def __init__(self, inner_frame, inner_frame_width, inner_frame_height, master=None):
        """ 带滚动条的Frame """
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
