import enum
from tkinter import *
from tkinter.colorchooser import askcolor
from GeometryPrimitives import *
import math
import time


class Engine(object):
    class TransitMode(enum.Enum):
        p1 = 0
        p2 = 1
        full = 2
        nothing = -1

    def __init__(self):
        self.button_font = "Arial 15"
        self.status_bar_font = "Arial 12"
        self.canvas_font = "Arial 10"
        self.window_w = 1000
        self.window_h = 1000
        self.bg_field = "#a6a6a6"
        self.line_color = "#000000"
        self.line_width = 1

        # mode flags
        self.edit = False
        self.add = False
        self.transit = self.TransitMode.nothing

        # objects
        self.transit_line_deltas = [0, 0]
        self.current_mouse = None
        self.prev_mouse = None
        self.line_points = [None, None]
        self.lines = []
        self.pen_primitive = []
        self.current_line = Line()

        # init tk window
        self.root = Tk()
        self.root.geometry("{}x{}".format(self.window_w, self.window_h))
        self.root.title("Gui")
        self.root.resizable(0, 0)

        # init canvas field
        self.canv = Canvas(self.root, bg=self.bg_field)

        # buttons init
        self.color_button = Button(text="Цвет", font=self.button_font,
                                   command=self._set_color)
        self.edit_button = Button(text="Изменить", font=self.button_font,
                                  command=self._set_edit)
        self.add_button = Button(text="Добавить", font=self.button_font,
                                 command=self._set_add)

        # init slider
        self.width_slider = Scale(self.root, orient=HORIZONTAL, from_=1, to=10, resolution=1)

        # init status bar
        self.status_bar = Label(text="", font=self.status_bar_font, anchor=W)

        # binds
        self.canv.bind("<B1-Motion>", self._canvas_b1_motion)
        self.canv.bind("<ButtonRelease-1>", self._canvas_b1_release)
        self.width_slider.bind("<B1-Motion>", self._set_width)

        # grid
        self.canv.grid(row=2, column=0, columnspan=7, rowspan=3, padx=5, pady=5, sticky=NSEW)
        self.width_slider.grid(row=2, column=7, columnspan=1, padx=5, pady=5, sticky=NSEW)
        self.color_button.grid(row=3, column=7, padx=5, pady=5)
        self.edit_button.grid(row=0, column=2, padx=5, pady=5)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        self.status_bar.grid(row=9, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(6, weight=1)

    # handler left mouse button release
    def _canvas_b1_release(self, event):
        self.prev_mouse = None
        self.current_mouse = None
        self.line_points = [None, None]
        if self.add:
            self.lines.append(self.current_line)
        if self.edit:
            self.transit = self.TransitMode.nothing
            self.current_line = Line()

    # handler left mouse button and motion
    def _canvas_b1_motion(self, event):
        self.current_mouse = Point(event.x, event.y)
        self._check_coords()
        self._redraw_scene()
        if self.add:
            self._add_line()
        elif self.edit:
            self._transit_line()
        self.prev_mouse = Point(self.current_mouse.x, self.current_mouse.y)

    def _check_coords(self):
        # checking mouse coord
        if self.current_mouse.x < 0:
            self.current_mouse.x = 0
        elif self.current_mouse.x > self.canv.winfo_width():
            self.current_mouse.x = self.canv.winfo_width()
        if self.current_mouse.y < 0:
            self.current_mouse.y = 0
        elif self.current_mouse.y > self.canv.winfo_height():
            self.current_mouse.y = self.canv.winfo_height()

    # transit line
    def _transit_line(self):
        eps = 10
        if self.prev_mouse is not None:
            if self.transit == self.TransitMode.nothing:
                for i in self.lines:
                    if isinstance(i, Line):
                        # match with p1
                        if math.fabs(i.p1.x - self.prev_mouse.x) <= eps \
                                and math.fabs(i.p1.y - self.prev_mouse.y) <= eps:
                            self.transit = self.TransitMode.p1
                            self.current_line = i
                            break
                        # match with p2
                        if math.fabs(i.p2.x - self.prev_mouse.x) <= eps \
                                and math.fabs(i.p2.y - self.prev_mouse.y) <= eps:
                            self.transit = self.TransitMode.p2
                            self.current_line = i
                            break
                        # match with point between p1, p2

            # check flags
            match self.transit:
                case self.TransitMode.p1:
                    self.current_line.p1 = self.current_mouse
                case self.TransitMode.p2:
                    self.current_line.p2 = self.current_mouse

    # adding line
    def _add_line(self):
        if self.line_points[0] is None:
            self.line_points[0] = self.current_mouse
            return

        self.line_points[1] = self.current_mouse
        buffer_line = Line(
            self.line_points[0],
            self.line_points[1],
            self.line_color,
            self.line_width
        )
        self._draw_line(buffer_line)
        self.current_line = buffer_line

    # draw primitive line
    def _draw_line(self, line):
        if isinstance(line, Line):
            self.canv.create_line(
                line.p1.x,
                line.p1.y,
                line.p2.x,
                line.p2.y,
                width=line.width,
                fill=line.color
            )
            options = {
                "font": self.canvas_font,
                "text": "x: {}, y: {}".format(line.p1.x, line.p1.y),
                "anchor": "w"}
            self.canv.create_text(line.p1.x, line.p1.y, options)
            options = {
                "font": self.canvas_font,
                "text": "x: {}, y: {}".format(line.p2.x, line.p2.y),
                "anchor": "w"}
            self.canv.create_text(line.p2.x, line.p2.y, options)

    # redraw scene
    def _redraw_scene(self):
        self.canv.delete("all")
        # redraw old-lines
        for i in self.lines:
            if isinstance(i, Line):
                self._draw_line(i)

    # mainloop
    def start(self):
        self.root.mainloop()

    # set color
    def _set_color(self):
        color = askcolor()[1]
        if color is not None:
            self.line_color = color

    # set width
    def _set_width(self, event):
        self.line_width = self.width_slider.get()

    # set edit mode
    def _set_edit(self):
        self.canv.config(cursor="fleur")
        self.edit_button.config(relief=SUNKEN)
        self.add_button.config(relief=RAISED)
        self.line_points = [None, None]
        self.current_line = Line()
        self.edit = True
        self.add = False

    # set add mode
    def _set_add(self):
        self.canv.config(cursor="pencil")
        self.edit_button.config(relief=RAISED)
        self.add_button.config(relief=SUNKEN)
        self.line_points = [None, None]
        self.current_line = Line()
        self.edit = False
        self.add = True


w = Engine()
w.start()
