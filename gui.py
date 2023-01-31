#! /usr/bin/env python
import tkinter as tk
import os

# set pwd to the directory of this script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from scripts.fetch_prots.gui import gui as fetchprots_gui
from scripts.bulk_rename.gui import gui as bulkrename_gui


window = tk.Tk()
window.title("Gupta Lab Tools (GUI)")

greeting = tk.Label(text="Choose a tool from the list below:")
greeting.pack()

def fetchprots():
    window.withdraw()
    fetchprots_gui()
    window.deiconify()

def bulkrename():
    window.withdraw()
    bulkrename_gui()
    window.deiconify()

tk.Button(window, text="fetch_prots", command=fetchprots).pack()
tk.Button(window, text="bulk_rename", command=bulkrename).pack()


window.mainloop()

