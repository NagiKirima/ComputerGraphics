from tkinter import *
from tkinter.colorchooser import askcolor
from Line import *
import time


class WindowGUI(object):
    # loop
    def start(self):
        self.root.mainloop()

    # init
    def __init__(self):
        # init args
        self.button_font = "Arial 15"
        self.status_bar_font = "Arial 12"
        self.window_w = 1000
        self.window_h = 1000
        self.canvas_w = 600
        self.canvas_h = 600
        self.bg_window = "white"
        self.bg_field = "#a6a6a6"
        self.line_color = "#000000"
        self.line_width = 1

        # line and points args
        self.line_flag = False
        self.points = []
        self.lines = []
        self.current_line = Line()

        # init tkinter window
        self.root = Tk()
        self.root.geometry(str(self.window_w) + "x" + str(self.window_h))
        self.root.title("My GUI")
        self.root.resizable(width=False, height=False)

        # canvas init
        self.canv = Canvas(self.root, bg=self.bg_field)

        # buttons init
        self.color_button = Button(text="Выбрать цвет", font=self.button_font,
                                   command=self._set_color)

        # slider init
        self.width_scale = Scale(self.root, orient=HORIZONTAL, from_=1, to=10, resolution=1)

        # status_bar init
        self.status_bar = Label(text="x: y:", font=self.status_bar_font, anchor=W)

        # binds
        self.canv.bind("<Motion>", self._fill_status_bar)
        self.canv.bind("<B1-Motion>", self._line_start)
        self.canv.bind("<3>", self._line_end)
        self.root.bind("<Delete>", self._clear_lines)
        self.width_scale.bind("<B1-Motion>", self._set_width)

        # grid
        self.canv.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.status_bar.grid(row=3, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.width_scale.grid(row=0, column=6, columnspan=1, padx=5, pady=5, sticky=NSEW)
        self.color_button.grid(row=0, column=5, padx=5, pady=5)
        # grid configure
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(6, weight=1)

    # handlers
    # delete all lines from scene
    def _clear_lines(self, event):
        self.line_flag = False
        self.points.clear()
        self.lines.clear()
        self.current_line = Line()
        self.canv.delete("all")

    # updating status bar methods
    def _fill_status_bar(self, event):
        self._update_status_bar(event.x, event.y)

    def _update_status_bar(self, x, y):
        self.status_bar.config(text="x:{0} y:{1}; {2}; color: {3}; width: {4}".format(
            str(x), str(y), str(self.current_line), self.line_color, self.line_width))

    #  draw line x0, y0 ---> event.x, event.y
    #  redrawing old lines
    def _line_start(self, event):
        if not self.line_flag:
            self.points = [Point(event.x, event.y)]
            self.line_flag = True
        else:
            if len(self.points) == 1:
                self.points.append(Point(event.x, event.y))
            else:
                self.points[1] = Point(event.x, event.y)

            # clear scene
            self.canv.delete("all")
            # draw old-lines
            for i in self.lines:
                if isinstance(i, Line):
                    self.canv.create_line(i.p1.x, i.p1.y,
                                          i.p2.x, i.p2.y,
                                          width=i.width, fill=i.color)

            # draw current line
            buff_line = Line(self.points[0], self.points[1], self.line_color, self.line_width)
            self.canv.create_line(buff_line.p1.x, buff_line.p1.y,
                                  buff_line.p2.x, buff_line.p2.y,
                                  width=buff_line.width, fill=buff_line.color)
            # read current line
            self.current_line = buff_line

        # update status bar
        self._update_status_bar(event.x, event.y)

    def _line_end(self, event):
        if self.line_flag:
            self.points.clear()
            self.lines.append(self.current_line)
            self.line_flag = False

    # set color
    def _set_color(self):
        color = askcolor()[1]
        if color is not None:
            self.line_color = color

    # set width
    def _set_width(self, event=None):
        self.line_width = self.width_scale.get()


w = WindowGUI()
w.start()