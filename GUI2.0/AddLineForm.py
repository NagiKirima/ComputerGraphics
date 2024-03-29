import math
import tkinter.messagebox
from tkinter import *
from Primitives import *
from Settings import BUTTON_FONT, LABEL_FONT, LEN
import GUI
import re


class AddLineForm(Toplevel):
    def __init__(self, mainapp, master=None):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.title("Add Line")
        self.geometry("500x120")
        self.resizable(False, False)
        self.mainapp = mainapp
        check = (self.register(self._is_valid), "%P")

        # widget init
        self.send_button = Button(self, text="Добавить прямую", font=BUTTON_FONT,
                                  command=self._send_button_click)
        self.entry_list = [
            Entry(self, validate="key", validatecommand=check),
            Entry(self, validate="key", validatecommand=check),
            Entry(self, validate="key", validatecommand=check),
            Entry(self, validate="key", validatecommand=check),
            Entry(self, validate="key", validatecommand=check),
            Entry(self, validate="key", validatecommand=check)
        ]

        # label grid
        Label(self, text="x1:", font=LABEL_FONT).grid(row=0, column=0, sticky=NSEW)
        Label(self, text="y1:", font=LABEL_FONT).grid(row=0, column=2, sticky=NSEW)
        Label(self, text="z1:", font=LABEL_FONT).grid(row=0, column=4, sticky=NSEW)
        Label(self, text="x2:", font=LABEL_FONT).grid(row=1, column=0, sticky=NSEW)
        Label(self, text="y2:", font=LABEL_FONT).grid(row=1, column=2, sticky=NSEW)
        Label(self, text="z2:", font=LABEL_FONT).grid(row=1, column=4, sticky=NSEW)
        # entry grid
        self.entry_list[0].grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
        self.entry_list[1].grid(row=0, column=3, padx=5, pady=5, sticky=NSEW)
        self.entry_list[2].grid(row=0, column=5, padx=5, pady=5, sticky=NSEW)
        self.entry_list[3].grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)
        self.entry_list[4].grid(row=1, column=3, padx=5, pady=5, sticky=NSEW)
        self.entry_list[5].grid(row=1, column=5, padx=5, pady=5, sticky=NSEW)
        self.send_button.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        # grid configure
        for i in range(6):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(2, weight=1)

    @staticmethod
    def _is_valid(value):
        return True if re.match("^-$|^$|-?(0|[1-9]\d*)(?<!-0)$", value) is not None else False

    def _send_button_click(self):
        values = []
        error = False
        for i in self.entry_list:
            if isinstance(i, Entry):
                try:
                    value = int(i.get())
                    if math.fabs(value) < LEN:
                        values.append(value)
                    else:
                        raise 0
                except:
                    error = True
                    tkinter.messagebox.showerror("Ошибка", "Ошибка в вводе значения")
                    return
        if isinstance(self.mainapp, GUI.Engine):
            l = Line(
                Point(values[0], values[1], values[2]),
                Point(values[3], values[4], values[5]))
            self.mainapp.lines.append(l)
            self.mainapp.current_line = l
            self.mainapp.redraw_scene()
            self._on_closing()

    def _on_closing(self):
        self.grab_release()
        self.destroy()
