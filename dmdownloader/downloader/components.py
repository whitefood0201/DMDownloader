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