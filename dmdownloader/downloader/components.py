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

def inputBox(master: tk.Misc, labelText: str, bindVar: tk.Variable, font, style: str) -> ttk.Frame:
    fra = ttk.Frame(master=master)
    ttk.Label(master=fra, text=labelText, width=50, style=style).pack()
    ttk.Entry(master=fra, width=75, font=font, textvariable=bindVar).pack()
    return fra

def optBox(master: tk.Misc, labelText , bindVar: tk.BooleanVar, style) -> tuple[ttk.Frame, tk.Scale]:
    fra = ttk.Frame(master=master)
    ttk.Label(master=fra, text=labelText, style=style).pack()
    opt = optButton(fra, *bindBoolVar(bindVar))
    opt.pack(pady=10)
    return fra, opt