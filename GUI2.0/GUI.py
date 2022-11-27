import tkinter
from tkinter import *
from Settings import *
from tkinter.colorchooser import askcolor
from Primitives import *
import math
import enum
# from numba import njit


class Engine(object):
    # enums
    ###############################################################
    class ProjectionMode(enum.Enum):
        xy = 0,
        zy = 1,
        xz = 2

    class TransitMode(enum.Enum):
        point1 = 0
        point2 = 1
        parallel = 2
        nothing = -1

    class WorkingMode(enum.Enum):
        add_mode = 0
        edit_mode = 1

    # initialization
    ###############################################################
    def __init__(self):
        self.line_color = "#000000"
        self.line_width = 1

        # mode flags
        self.work_mode = self.WorkingMode.add_mode
        self.transit = self.TransitMode.nothing
        self.projection_mode = self.ProjectionMode.xy

        # objects
        self.current_zero_coord = [0, 0]
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
        self.y_bar = YBAR
        self.x_bar = XBAR

        # buttons init
        self.color_button = Button(text="Цвет", font=BUTTON_FONT,
                                   command=self._set_color)
        self.add_button = Button(text="Добавить", font=BUTTON_FONT,
                                 command=self._set_add, relief=SUNKEN)
        self.edit_button = Button(text="Изменить", font=BUTTON_FONT,
                                  command=self._set_edit)
        self.xy_button = Button(text="XY", font=BUTTON_FONT,
                                command=self._set_xy_projection, relief=SUNKEN)
        self.zy_button = Button(text="ZY", font=BUTTON_FONT,
                                command=self._set_zy_projection)
        self.xz_button = Button(text="XZ", font=BUTTON_FONT,
                                command=self._set_xz_projection)

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
        self.x_bar.bind("<B1-Motion>", self._update_zero_x_coord)
        self.y_bar.bind("<B1-Motion>", self._update_zero_y_coord)
        # self.canvas.bind("<3>", self._canvas_delete_button_hotkey)

        # grid
        self.canvas.grid(row=2, column=0, columnspan=7, rowspan=3, padx=5, pady=5, sticky=NSEW)
        self.width_slider.grid(row=2, column=9, padx=5, pady=5, sticky=NSEW)
        self.color_button.grid(row=3, column=7, padx=5, pady=5)
        self.edit_button.grid(row=0, column=2, padx=5, pady=5)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        self.status_bar.grid(row=9, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.xy_button.grid(row=1, column=1, padx=5, pady=5)
        self.zy_button.grid(row=1, column=2, padx=5, pady=5)
        self.xz_button.grid(row=1, column=3, padx=5, pady=5)

        # grid configure
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(6, weight=1)

    # handlers
    ###############################################################
    # transit zero coord by x-scrollbar
    def _update_zero_x_coord(self, event):
        self.current_zero_coord[0] = int(self.x_bar.get()[0] * 2 * MAXX + MINX)
        # print(self.current_zero_coord)

    # transit zero coord by y_scrollbar
    def _update_zero_y_coord(self, event):
        self.current_zero_coord[1] = int(self.y_bar.get()[0] * 2 * MAXY + MINY)
        # print(self.current_zero_coord)

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

    # set projection mode methods
    def _set_xy_projection(self):
        self.projection_mode = self.ProjectionMode.xy
        self.xy_button.config(relief=SUNKEN)
        self.zy_button.config(relief=RAISED)
        self.xz_button.config(relief=RAISED)
        self._redraw_scene()

    def _set_zy_projection(self):
        self.projection_mode = self.ProjectionMode.zy
        self.xy_button.config(relief=RAISED)
        self.zy_button.config(relief=SUNKEN)
        self.xz_button.config(relief=RAISED)
        self._redraw_scene()

    def _set_xz_projection(self):
        self.projection_mode = self.ProjectionMode.xz
        self.xy_button.config(relief=RAISED)
        self.zy_button.config(relief=RAISED)
        self.xz_button.config(relief=SUNKEN)
        self._redraw_scene()

    # update status bar
    def _update_status_bar(self, event):
        self._fill_status_bar(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)

    # fill status bar label
    def _fill_status_bar(self, x, y):
        if self.work_mode == self.WorkingMode.add_mode:
            if self.projection_mode == self.ProjectionMode.xy:
                self.status_bar.config(
                    text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))
            if self.projection_mode == self.ProjectionMode.xz:
                self.status_bar.config(
                    text="x:{}, z:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))
            if self.projection_mode == self.ProjectionMode.zy:
                self.status_bar.config(
                    text="z:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))

        if self.work_mode == self.WorkingMode.edit_mode:
            if self.projection_mode == self.ProjectionMode.xy:
                self.status_bar.config(
                    text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))
            if self.projection_mode == self.ProjectionMode.xz:
                self.status_bar.config(
                    text="x:{}, z:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))
            if self.projection_mode == self.ProjectionMode.zy:
                self.status_bar.config(
                    text="z:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))

    # left button click and motion (draw line or transit)
    def _canvas_b1_motion(self, event):
        self.current_mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)
        self._redraw_scene()
        match self.work_mode:
            case self.WorkingMode.add_mode:
                self._add_line()
            case self.WorkingMode.edit_mode:
                self._transit_line()
        self.prev_mouse = self.current_mouse.copy()
        self._fill_status_bar(self.current_mouse[0], self.current_mouse[1])

    # release left button (end drawing or transit line)
    def _canvas_b1_release(self, event):
        self.prev_mouse = None
        self.current_mouse = None
        self.line_points = [None, None]
        self.transit_line_deltas = None
        self.transit = self.TransitMode.nothing
        match self.work_mode:
            case self.WorkingMode.add_mode:
                self.lines.append(self.current_line)
            case self.WorkingMode.edit_mode:
                self.transit = self.TransitMode.nothing

    # left button click (chose line)
    def _canvas_left_button_click(self, event):
        if self.work_mode == self.WorkingMode.edit_mode:
            mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)
            for i in range(len(self.lines)):
                if self._is_cursor_on_line(mouse[0], mouse[1], self.lines[i]):
                    self.current_line = self.lines[i]
                    break
            self._fill_status_bar(mouse[0], mouse[1])

    # calculate methods
    ###############################################################
    # check mouse pos
    def _check_mouse_coord(self, x, y):
        if x < -MAXX:
            x = -MAXX
        elif x > MAXX:
            x = MAXX
        if y < -MAXY:
            y = -MAXY
        elif y > MAXY:
            y = MAXY
        return [x, y]

    # convert canvas mouse coord to point coord with projection
    def _get_mouse_projection_point(self):
        if self.projection_mode == self.ProjectionMode.xy:
            return Point(self.current_mouse[0], self.current_mouse[1], 0)
        elif self.projection_mode == self.ProjectionMode.xz:
            return Point(self.current_mouse[0], 0, self.current_mouse[1])
        else:
            return Point(0, self.current_mouse[1], self.current_mouse[0])

    # convert point coord to canvas coord
    def _get_canvas_coord_from_projection_point(self, point):
        if isinstance(point, Point):
            if self.projection_mode == self.ProjectionMode.xy:
                return [point.x, point.y]
            elif self.projection_mode == self.ProjectionMode.xz:
                return [point.x, point.z]
            else:
                return [point.z, point.y]

    # check cursor pos on line
    def _is_cursor_on_line(self, m_x, m_y, line):
        # point projection to canvas coords
        p1 = self._get_canvas_coord_from_projection_point(line.p1)
        p2 = self._get_canvas_coord_from_projection_point(line.p2)
        if m_x < min(p1[0], p2[0]) or m_x > max(p1[0], p2[0]):
            return False
        if m_y < min(p1[1], p2[1]) or m_y > max(p1[1], p2[1]):
            return False
        # canonical equation of line in the plane: Ax + By + C = 0
        eps = 10
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = p2[0] * p1[1] - p1[0] * p2[1]
        return math.fabs(m_x * a + m_y * b + c) <= eps ** 3

    # add line
    def _add_line(self):
        if self.line_points[0] is None:
            self.line_points[0] = self._get_mouse_projection_point()
            return

        self.line_points[1] = self._get_mouse_projection_point()
        buffer_line = Line(
            self.line_points[0],
            self.line_points[1],
            self.line_color,
            self.line_width
        )
        self._draw_line(buffer_line)
        self.current_line = buffer_line

    # draw line
    def _draw_line(self, line):
        if isinstance(line, Line):
            canvas_x1, canvas_y1 = self._get_canvas_coord_from_projection_point(line.p1)
            canvas_x2, canvas_y2 = self._get_canvas_coord_from_projection_point(line.p2)
            # drawing line
            self.canvas.create_line(
                canvas_x1,
                canvas_y1,
                canvas_x2,
                canvas_y2,
                width=line.width,
                fill=line.color,
                smooth=True
            )
            # drawing line text
            canvas_p1_projection = self._get_canvas_coord_from_projection_point(line.p1)
            canvas_p2_projection = self._get_canvas_coord_from_projection_point(line.p2)
            anchor_p1 = self._get_line_text_anchor(canvas_p1_projection)
            anchor_p2 = self._get_line_text_anchor(canvas_p2_projection)
            opt1 = self._get_line_text_options(line.p1, anchor_p1)
            opt2 = self._get_line_text_options(line.p2, anchor_p2)
            self.canvas.create_text(canvas_p1_projection[0], canvas_p1_projection[1], opt1)
            self.canvas.create_text(canvas_p2_projection[0], canvas_p2_projection[1], opt2)

    # sub methods for draw line
    def _get_line_text_options(self, point, anchor):
        if isinstance(point, Point):
            return {
                "font": CANVAS_TEXT_FONT,
                "text": "({}, {}, {})".format(point.x, point.y, point.z),
                "anchor": anchor
            }

    def _get_line_text_anchor(self, point_coord):
        part1 = ""
        part2 = ""
        delta = 300
        if point_coord[1] <= delta + MINY:
            part1 = "n"
        elif point_coord[1] >= MAXY - delta:
            part1 = "s"
        if point_coord[0] <= delta - MAXX:
            part2 = "w"
        elif point_coord[0] >= MAXX - delta:
            part2 = "e"
        else:
            part2 = "w"
        return part1 + part2

    # transit line
    def _transit_line(self):
        eps = 10
        if self.prev_mouse is not None:
            if self.transit == self.TransitMode.nothing:
                for i in range(len(self.lines)):
                    if isinstance(self.lines[i], Line):
                        # match with p1
                        point_to_canvas = self._get_canvas_coord_from_projection_point(self.lines[i].p1)
                        if math.fabs(point_to_canvas[0] - self.prev_mouse[0]) <= eps \
                                and math.fabs(point_to_canvas[1] - self.prev_mouse[1]) <= eps:
                            self.transit = self.TransitMode.point1
                            self.current_line = self.lines[i]
                            break

                        # match with p2
                        point_to_canvas = self._get_canvas_coord_from_projection_point(self.lines[i].p2)
                        if math.fabs(point_to_canvas[0] - self.prev_mouse[0]) <= eps \
                                and math.fabs(point_to_canvas[1] - self.prev_mouse[1]) <= eps:
                            self.transit = self.TransitMode.point2
                            self.current_line = self.lines[i]
                            break

                        # match with point between p1, p2
                        if self._is_cursor_on_line(self.prev_mouse[0], self.prev_mouse[1], self.lines[i]):
                            p1 = self._get_canvas_coord_from_projection_point(self.lines[i].p1)
                            p2 = self._get_canvas_coord_from_projection_point(self.lines[i].p2)
                            # deltas for canvas coord
                            self.transit_line_deltas = [
                                p1[0] - self.prev_mouse[0],
                                p1[1] - self.prev_mouse[1],
                                # deltas for p2
                                self.prev_mouse[0] - p2[0],
                                self.prev_mouse[1] - p2[1]
                            ]
                            self.current_line = self.lines[i]
                            self.transit = self.TransitMode.parallel
                            break

            # check flags
            if self.transit == self.TransitMode.point1:
                if self.projection_mode == self.ProjectionMode.xy:
                    self.current_line.p1.x = self.current_mouse[0]
                    self.current_line.p1.y = self.current_mouse[1]
                elif self.projection_mode == self.ProjectionMode.xz:
                    self.current_line.p1.x = self.current_mouse[0]
                    self.current_line.p1.z = self.current_mouse[1]
                else:
                    self.current_line.p1.z = self.current_mouse[0]
                    self.current_line.p1.y = self.current_mouse[1]
            if self.transit == self.TransitMode.point2:
                if self.projection_mode == self.ProjectionMode.xy:
                    self.current_line.p2.x = self.current_mouse[0]
                    self.current_line.p2.y = self.current_mouse[1]
                elif self.projection_mode == self.ProjectionMode.xz:
                    self.current_line.p2.x = self.current_mouse[0]
                    self.current_line.p2.z = self.current_mouse[1]
                else:
                    self.current_line.p2.z = self.current_mouse[0]
                    self.current_line.p2.y = self.current_mouse[1]
            if self.transit == self.TransitMode.parallel:
                # check on bounds p1, p2
                p1 = self._get_canvas_coord_from_projection_point(self.current_line.p1)
                p2 = self._get_canvas_coord_from_projection_point(self.current_line.p2)
                is_not_bound = self._check_point_coord(p1[0], p1[1]) and self._check_point_coord(p2[0], p2[1])
                if is_not_bound:
                    if self.projection_mode == self.ProjectionMode.xy:
                        self.current_line.p1.x = self.current_mouse[0] + self.transit_line_deltas[0]
                        self.current_line.p2.x = self.current_mouse[0] - self.transit_line_deltas[2]
                        self.current_line.p1.y = self.current_mouse[1] + self.transit_line_deltas[1]
                        self.current_line.p2.y = self.current_mouse[1] - self.transit_line_deltas[3]
                    if self.projection_mode == self.ProjectionMode.xz:
                        self.current_line.p1.x = self.current_mouse[0] + self.transit_line_deltas[0]
                        self.current_line.p2.x = self.current_mouse[0] - self.transit_line_deltas[2]
                        self.current_line.p1.z = self.current_mouse[1] + self.transit_line_deltas[1]
                        self.current_line.p2.z = self.current_mouse[1] - self.transit_line_deltas[3]
                    if self.projection_mode == self.ProjectionMode.zy:
                        self.current_line.p1.z = self.current_mouse[0] + self.transit_line_deltas[0]
                        self.current_line.p2.z = self.current_mouse[0] - self.transit_line_deltas[2]
                        self.current_line.p1.y = self.current_mouse[1] + self.transit_line_deltas[1]
                        self.current_line.p2.y = self.current_mouse[1] - self.transit_line_deltas[3]

    # check line point pos
    def _check_point_coord(self, x, y):
        if x <= MINX or x >= MAXX or y <= MINY or y >= MAXY:
            return False
        return True

    # render methods
    ###############################################################
    # redraw scene
    def _redraw_scene(self):
        self.canvas.delete("all")
        # draw lines primitive
        for i in range(len(self.lines)):
            self._draw_line(self.lines[i])

    # mainloop
    def start(self):
        self.root.mainloop()
