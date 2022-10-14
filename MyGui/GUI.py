from tkinter import *
from gui_settings import *
from tkinter.colorchooser import askcolor
from GeometryPrimitives import *
import math
import enum
from numba import njit


class Engine(object):
    class TransitMode(enum.Enum):
        point1 = 0
        point2 = 1
        parallel = 2
        nothing = -1

    class WorkingMode(enum.Enum):
        add_mode = 0
        edit_mode = 1
        nothing = -1

    # fields initialization
    def __init__(self):
        self.line_color = "#000000"
        self.line_width = 1

        # mode flags
        self.work_mode = self.WorkingMode.nothing
        self.transit = self.TransitMode.nothing

        # objects
        self.transit_line_deltas = None
        self.current_mouse = None
        self.prev_mouse = None
        self.line_points = [None, None]
        self.lines = []
        self.current_line = None

        # init tk window
        self.root = WINDOW

        # init canvas field
        self.canvas = CANVAS

        # buttons init
        self.color_button = Button(text="Цвет", font=BUTTON_FONT,
                                   command=self._set_color)
        self.edit_button = Button(text="Изменить", font=BUTTON_FONT,
                                  command=self._set_edit)
        self.add_button = Button(text="Добавить", font=BUTTON_FONT,
                                 command=self._set_add)

        # init slider
        self.width_slider = WIDTH_SCALE

        # init labels
        self.status_bar = STATUS_BAR
        self.width_label = WIDTH_LABEL

        # binds
        self.canvas.bind("<B1-Motion>", self._canvas_b1_motion)
        self.canvas.bind("<ButtonRelease-1>", self._canvas_b1_release)
        self.width_slider.bind("<B1-Motion>", self._set_width)
        self.canvas.bind("<Motion>", self._update_status_bar)
        self.canvas.bind("<1>", self._canvas_left_button_click)
        self.canvas.bind("<2>", self._canvas_delete_button_hotkey)

        # grid
        self.canvas.grid(row=2, column=0, columnspan=7, rowspan=3, padx=5, pady=5, sticky=NSEW)
        self.width_slider.grid(row=2, column=9, padx=5, pady=5, sticky=NSEW)
        self.color_button.grid(row=3, column=7, padx=5, pady=5)
        self.edit_button.grid(row=0, column=2, padx=5, pady=5)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        self.status_bar.grid(row=9, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(6, weight=1)

    # update status bar
    def _update_status_bar(self, event):
        self._fill_status_bar(event.x, event.y)

    def _fill_status_bar(self, x, y):
        match self.work_mode:
            case self.WorkingMode.add_mode:
                self.status_bar.config(
                    text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    )
                )
            case self.WorkingMode.edit_mode:
                if self.current_line is not None:
                    self.status_bar.config(
                        text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                            x, y, self.current_line, self.current_line.color, self.current_line.width
                        )
                    )
                else:
                    self.status_bar.config(
                        text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                            x, y, self.current_line, None, None
                        )
                    )

    # handler delete button
    #@njit(fastmath=True, parallel=True)
    def _canvas_delete_button_hotkey(self, event):
        for i in range(len(self.lines)):
            pass

    # handler left mouse click
    def _canvas_left_button_click(self, event):
        mouse_x, mouse_y = self._check_coords(event.x, event.y)
        eps = 10
        for i in self.lines:
            if isinstance(i, Line):
                center_x = (i.p1.x + i.p2.x) / 2
                center_y = (i.p1.y + i.p2.y) / 2
                if math.fabs(center_x - mouse_x) <= eps and math.fabs(center_y - mouse_y) <= eps:
                    self.current_line = i
                    break
        self._fill_status_bar(mouse_x, mouse_y)

    # handler left mouse button release
    def _canvas_b1_release(self, event):
        self.prev_mouse = None
        self.current_mouse = None
        self.line_points = [None, None]
        self.transit_line_deltas = None
        match self.work_mode:
            case self.WorkingMode.add_mode:
                self.lines.append(self.current_line)
            case self.WorkingMode.edit_mode:
                self.transit = self.TransitMode.nothing

    # handler left mouse button and motion
    def _canvas_b1_motion(self, event):
        coords = self._check_coords(event.x, event.y)
        self.current_mouse = Point(coords[0], coords[1])
        self._redraw_scene()
        match self.work_mode:
            case self.WorkingMode.add_mode:
                self._add_line()
            case self.WorkingMode.edit_mode:
                self._transit_line()
        self.prev_mouse = Point(self.current_mouse.x, self.current_mouse.y)
        self._fill_status_bar(self.current_mouse.x, self.current_mouse.y)

    # checking coords
    def _check_coords(self, x, y):
        if x < 0:
            x = 0
        elif x > self.canvas.winfo_width():
            x = self.canvas.winfo_width()
        if y < 0:
            y = 0
        elif y > self.canvas.winfo_height():
            y = self.canvas.winfo_height()
        return [x, y]

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
                            self.transit = self.TransitMode.point1
                            self.current_line = i
                            break
                        # match with p2
                        elif math.fabs(i.p2.x - self.prev_mouse.x) <= eps \
                                and math.fabs(i.p2.y - self.prev_mouse.y) <= eps:
                            self.transit = self.TransitMode.point2
                            self.current_line = i
                            break
                        # match with point between p1, p2
                        else:
                            if math.fabs(self.prev_mouse.x * i.get_a() + self.prev_mouse.y * i.get_b() + i.get_c()) <= eps**3:
                                self.transit_line_deltas = [
                                    # deltas for p1
                                    i.p1.x - self.prev_mouse.x,
                                    i.p1.y - self.prev_mouse.y,
                                    # deltas for p2
                                    self.prev_mouse.x - i.p2.x,
                                    self.prev_mouse.y - i.p2.y
                                ]
                                self.current_line = i
                                self.transit = self.TransitMode.parallel
                                break

            # check flags
            match self.transit:
                case self.TransitMode.point1:
                    self.current_line.p1 = self.current_mouse
                case self.TransitMode.point2:
                    self.current_line.p2 = self.current_mouse
                case self.TransitMode.parallel:
                    self.current_line.p1.x = self.current_mouse.x + self.transit_line_deltas[0]
                    self.current_line.p2.x = self.current_mouse.x - self.transit_line_deltas[2]
                    self.current_line.p1.y = self.current_mouse.y + self.transit_line_deltas[1]
                    self.current_line.p2.y = self.current_mouse.y - self.transit_line_deltas[3]

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
            self.canvas.create_line(
                line.p1.x,
                line.p1.y,
                line.p2.x,
                line.p2.y,
                width=line.width,
                fill=line.color
            )
            self.canvas.create_oval(
                int((line.p1.x + line.p2.x) / 2) - line.width,
                int((line.p1.y + line.p2.y) / 2) - line.width,
                int((line.p1.x + line.p2.x) / 2) + line.width,
                int((line.p1.y + line.p2.y) / 2) + line.width,
                fill=line.color,
                outline="white"
            )
            anchor_p1 = self._get_line_text_anchor(line.p1)
            anchor_p2 = self._get_line_text_anchor(line.p2)
            options1 = self._get_line_text_options(line.p1, anchor_p1)
            options2 = self._get_line_text_options(line.p2, anchor_p2)
            self.canvas.create_text(line.p1.x, line.p1.y, options1)
            self.canvas.create_text(line.p2.x, line.p2.y, options2)

    def _get_line_text_options(self, point, anchor):
        return {
            "font": CANVAS_TEXT_FONT,
            "text": "x: {}, y: {}".format(point.x, point.y),
            "anchor": anchor
        }

    def _get_line_text_anchor(self, point):
        if isinstance(point, Point):
            part1 = ""
            part2 = ""
            delta = 100
            if point.y <= delta:
                part1 = "n"
            elif point.y >= self.canvas.winfo_height() - delta:
                part1 = "s"

            if point.x <= delta:
                part2 = "w"
            elif point.x >= self.canvas.winfo_width() - delta:
                part2 = "e"
            else:
                part2 = "w"
            return part1 + part2
        return "center"

    # redraw scene
    def _redraw_scene(self):
        self.canvas.delete("all")
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
            if self.work_mode == self.WorkingMode.edit_mode:
                self.current_line.color = color
                self._redraw_scene()

    # set width
    def _set_width(self, event):
        self.line_width = self.width_slider.get()
        if self.work_mode == self.WorkingMode.edit_mode:
            self.current_line.width = self.width_slider.get()
            self._redraw_scene()

    # set edit mode
    def _set_edit(self):
        self.canvas.config(cursor="fleur")
        self.edit_button.config(relief=SUNKEN)
        self.add_button.config(relief=RAISED)
        self.line_points = [None, None]
        self.current_line = None
        self.work_mode = self.WorkingMode.edit_mode

    # set add mode
    def _set_add(self):
        self.canvas.config(cursor="pencil")
        self.edit_button.config(relief=RAISED)
        self.add_button.config(relief=SUNKEN)
        self.line_points = [None, None]
        self.current_line = None
        self.work_mode = self.WorkingMode.add_mode

