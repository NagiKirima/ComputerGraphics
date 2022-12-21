from tkinter import *
from Settings import BUTTON_FONT, LABEL_FONT, LEN
import re
from Enums import *
from CalculateOperation import Calculate
from tkinter import messagebox


class FormFor3dOperation(Toplevel):
    def __init__(self, mainapp, master=None):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.title("3D operations")
        self.geometry("600x400")
        self.resizable(False, False)
        self.mainapp = mainapp
        check = None

        Label(self, text="Перемещение", font=LABEL_FONT). grid(row=0, column=0, columnspan=9, padx=5, pady=5, sticky=NSEW)
        Label(self, text="m", font=LABEL_FONT).grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        Label(self, text="n", font=LABEL_FONT).grid(row=1, column=3, padx=5, pady=5, sticky=NSEW)
        Label(self, text="l", font=LABEL_FONT).grid(row=1, column=6, padx=5, pady=5, sticky=NSEW)
        self.entry_m = Entry(self, font=LABEL_FONT)
        self.entry_n = Entry(self, font=LABEL_FONT)
        self.entry_l = Entry(self, font=LABEL_FONT)
        self.entry_m.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.entry_n.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.entry_l.grid(row=1, column=7, columnspan=2, padx=5, pady=5, sticky=NSEW)


    def _on_closing(self):
        self.grab_release()
        self.destroy()