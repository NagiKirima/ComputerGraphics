import math
import tkinter.messagebox
import enum
from tkinter import *
from Primitives import *
from Settings import BUTTON_FONT, LABEL_FONT, LEN
import GUI
import re


class FormFor2dOperation(Toplevel):
    class ProjectionMode(enum.Enum):
        xy = 0,
        zy = 1,
        xz = 2

    def __init__(self, mainapp, master=None):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.title("2D operations")
        self.geometry("600x600")
        self.resizable(False, False)
        self.mainapp = mainapp
        self.check = (self.register(self._is_valid), "%P")
        self.proj_mode = self.ProjectionMode.xy

        # projection mode buttons
        self.xy_button = Button(self, text="XY", font=BUTTON_FONT, relief=SUNKEN)
        self.zy_button = Button(self, text="ZY", font=BUTTON_FONT)
        self.xz_button = Button(self, text="XZ", font=BUTTON_FONT)

        # transfer operation widgets
        self.transfer_m_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)
        self.transfer_n_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)

        # scale operation widgets
        self.scale_a_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)
        self.scale_b_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)

        # rotate operation widgets
        self.rotate_angle_scale = Scale(self, orient=HORIZONTAL, from_=-360, to=360, resolution=1, font=LABEL_FONT)

        # mirroring operation widgets
        self.mirror_radio_button_ord = Radiobutton(self, text='по ординате', value=1, font=LABEL_FONT)
        self.mirror_radio_button_abc = Radiobutton(self, text='по абсциссе', value=1, font=LABEL_FONT)

        # projection operation widgets
        self.projection_p_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)
        self.projection_q_entry = Entry(self, validatecommand=self.check, font=LABEL_FONT)

        # confirm changes button
        self.send_button = Button(self, text="Применить", font=BUTTON_FONT)

        # grid all widgets
        self._grid()
        self._set_defaults()

    # grid
    def _grid(self):
        # projection mode buttons
        self.xy_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.zy_button.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.xz_button.grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        # transfer
        Label(self, text="Перемещение", font=LABEL_FONT).grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        Label(self, text="m", font=LABEL_FONT).grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)
        Label(self, text="n", font=LABEL_FONT).grid(row=2, column=3, padx=5, pady=5, sticky=NSEW)
        self.transfer_m_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.transfer_n_entry.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        # scale
        Label(self, text="Масштабирование", font=LABEL_FONT).grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        Label(self, text="a", font=LABEL_FONT).grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)
        Label(self, text="b", font=LABEL_FONT).grid(row=4, column=3, padx=5, pady=5, sticky=NSEW)
        self.scale_a_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.scale_b_entry.grid(row=4, column=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        # rotate
        Label(self, text="Вращение", font=LABEL_FONT).grid(row=5, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        Label(self, text="Угол", font=LABEL_FONT).grid(row=6, column=0, padx=5, pady=5)
        self.rotate_angle_scale.grid(row=6, column=1, columnspan=5, padx=5, pady=5, sticky=NSEW)
        # mirror
        Label(self, text="Зеркалирование", font=LABEL_FONT).grid(row=7, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        self.mirror_radio_button_abc.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=NSEW)
        self.mirror_radio_button_ord.grid(row=8, column=3, columnspan=3, padx=5, pady=5, sticky=NSEW)
        # project
        Label(self, text="Проецирование", font=LABEL_FONT).grid(row=9, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        Label(self, text="p", font=LABEL_FONT).grid(row=10, column=0, padx=5, pady=5, sticky=NSEW)
        Label(self, text="q", font=LABEL_FONT).grid(row=10, column=3, padx=5, pady=5, sticky=NSEW)
        self.projection_p_entry.grid(row=10, column=1, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.projection_q_entry.grid(row=10, column=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        # confirm
        self.send_button.grid(row=11, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)

        for i in range(11):
            self.rowconfigure(i, weight=1, minsize=25)
        for i in range(5):
            self.columnconfigure(i, weight=1, minsize=50)

    def _set_defaults(self):
        self.transfer_m_entry.insert(-1, str(1))
        self.transfer_n_entry.insert(-1, str(1))
        self.scale_a_entry.insert(-1, str(1))
        self.scale_b_entry.insert(-1, str(1))
        self.projection_p_entry.insert(-1, str(1))
        self.projection_q_entry.insert(-1, str(1))

    def _set_projection(self, event):
        pass

    @staticmethod
    def _is_valid(value):
        return re.match("^-$|^$|-?(0|[1-9]\d*)(?<!-0)$", value) is not None

    def _on_closing(self):
        self.grab_release()
        self.destroy()
