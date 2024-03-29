import tkinter.filedialog
import tkinter.messagebox
import json
from tkinter import *
from AddLineForm import *
from EditLineForm import *
from Settings import *
from tkinter.colorchooser import askcolor
from Primitives import *
import math
from Enums import *
from FormFor2dOperation import FormFor2dOperation
from FormFor3dOperation import FormFor3dOperation
from TrimetricForm import TrimetricForm


class Engine(object):
    def __init__(self):
        self.line_color = "#000000"
        self.line_width = 1

        # mode flags
        self.work_mode = WorkingMode.add_mode
        self.transit = TransitMode.nothing
        self.projection_mode = ProjectionMode.xy
        self.line_text_flag = True
        self.is_first_cursor_pos_on_line = False

        # objects
        self.current_zero_coord = [0, 0]
        self.transit_line_deltas = None
        self.current_mouse = None
        self.prev_mouse = None
        self.rect_start_pos = None
        self.line_points = [None, None]
        self.lines = []
        self.current_line = None
        self.current_lines = []

        # init tk window
        self.root = WINDOW

        # init canvas field
        self.canvas = CANVAS
        self.y_bar = YBAR
        self.x_bar = XBAR

        # buttons init
        self.line_button = Button(self.root, text="Добавить линию", font=BUTTON_FONT,
                                  command=self._open_add_line_form)
        self.color_button = Button(self.root, text="Цвет", font=BUTTON_FONT,
                                   command=self._set_color)
        self.add_button = Button(self.root, text="Добавить", font=BUTTON_FONT,
                                 command=self._set_add, relief=SUNKEN)
        self.edit_button = Button(self.root, text="Изменить", font=BUTTON_FONT,
                                  command=self._set_edit)
        self.xy_button = Button(self.root, text="XY", font=BUTTON_FONT,
                                command=self._set_xy_projection, relief=SUNKEN)
        self.zy_button = Button(self.root, text="ZY", font=BUTTON_FONT,
                                command=self._set_zy_projection)
        self.xz_button = Button(self.root, text="XZ", font=BUTTON_FONT,
                                command=self._set_xz_projection)
        self.save_button = Button(self.root, text="Сохранить проект", font=BUTTON_FONT,
                                  command=self._save_file)
        self.load_button = Button(self.root, text="Загрузить проект", font=BUTTON_FONT,
                                  command=self._load_file)
        self.operations_2d_button = Button(self.root, text="2D операции", font=BUTTON_FONT,
                                           command=self._open_2d_opeation_form)
        self.operations_3d_button = Button(self.root, text="3D операции", font=BUTTON_FONT,
                                           command=self._open_3d_form)
        self.trimetric_matrix_button = Button(self.root, text="Осмотр", font=BUTTON_FONT,
                                              command=self._open_trimetric_form)

        # init slider
        self.width_slider = WIDTH_SCALE

        # init labels
        self.status_bar = STATUS_BAR
        self.width_label = WIDTH_LABEL

        # binds
        self.canvas.bind("<B1-Motion>", self._canvas_b1_motion)
        self.canvas.bind("<ButtonRelease-1>", self._canvas_b1_release)
        self.width_slider.bind("<B1-Motion>", self._set_width)
        self.canvas.bind("<Motion>", self._cursor_motion)
        self.canvas.bind("<1>", self._canvas_b1_click)
        self.x_bar.bind("<B1-Motion>", self._update_zero_x_coord)
        self.y_bar.bind("<B1-Motion>", self._update_zero_y_coord)
        self.root.bind("f", self._change_line_text_flag)
        self.root.bind("<BackSpace>", self._backspace_clicked)
        self.canvas.bind("<Control-1>", self._canvas_control_b1_clicked)
        self.canvas.bind("<Control-B1-Motion>", self._canvas_control_b1_motion)
        self.canvas.bind("<Control-ButtonRelease-1>", self._canvas_control_b1_motion_release)

        # grid window objects
        self.canvas.grid(row=0, column=0, columnspan=7, rowspan=9, padx=5, pady=5, sticky=NSEW)
        self.add_button.grid(row=0, column=7, columnspan=3, padx=5, pady=5, sticky=NSEW)
        self.edit_button.grid(row=0, column=10, columnspan=3, padx=5, pady=5, sticky=NSEW)
        self.xy_button.grid(row=1, column=7, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.zy_button.grid(row=1, column=9, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.xz_button.grid(row=1, column=11, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.width_label.grid(row=2, column=7, padx=5, pady=5, sticky=NSEW)
        self.width_slider.grid(row=2, column=8, columnspan=5, padx=5, pady=5, sticky=NSEW)
        self.color_button.grid(row=3, column=7, padx=5, pady=5, columnspan=6, sticky=NSEW)
        self.line_button.grid(row=4, column=7, padx=5, pady=5, columnspan=6, sticky=NSEW)
        self.save_button.grid(row=7, column=7, padx=5, pady=5, columnspan=3, sticky=NSEW)
        self.load_button.grid(row=7, column=10, padx=5, pady=5, columnspan=3, sticky=NSEW)
        self.status_bar.grid(row=9, column=0, columnspan=7, padx=5, pady=5, sticky=NSEW)
        self.trimetric_matrix_button.grid(row=6, column=7, padx=5, pady=5, columnspan=6, sticky=NSEW)

        # grid configure
        self.root.rowconfigure(8, weight=1)
        for i in range(7, 13):
            self.root.columnconfigure(i, minsize=50)
        self.root.columnconfigure(0, weight=1)

    # handlers
    # delete current line or group of lines
    def _backspace_clicked(self, event):
        if self.current_line is not None:
            self.lines.remove(self.current_line)
            self.current_line = None
        if len(self.current_lines) != 0:
            for i in self.current_lines:
                self.lines.remove(i)
            self.current_lines = []
        self.redraw_scene()

    # open trimetric form
    def _open_trimetric_form(self):
        if len(self.lines) != 0:
            form = TrimetricForm(self)
            form.grab_set()
        else:
            tkinter.messagebox.showerror("Ошибка", "Нет прямых!")

    # open dialog window with 3d operations
    def _open_3d_form(self):
        if self.current_line is None and len(self.current_lines) == 0:
            tkinter.messagebox.showerror("Ошибка", "Выберите прямые для изменения")
            return
        form = FormFor3dOperation(self)
        form.grab_set()

    # open dialog window with 2d operations
    def _open_2d_opeation_form(self):
        if self.current_line is None and len(self.current_lines) == 0:
            tkinter.messagebox.showerror("Ошибка", "Выберите прямые для изменения")
            return
        form = FormFor2dOperation(self)
        form.grab_set()

    # open dialog window for editing line
    def _open_edit_line_form(self):
        if self.current_line is None and len(self.current_lines) == 0:
            tkinter.messagebox.showerror("Ошибка", "Выберите прямые для изменения")
            return
        form = EditLineForm(self)
        form.grab_set()

    # open dialog window for adding line
    def _open_add_line_form(self):
        form = AddLineForm(self)
        form.grab_set()

    # transit zero coord by x-scrollbar
    def _update_zero_x_coord(self, event):
        self.current_zero_coord[0] = int(self.x_bar.get()[0] * 2 * MAXX + MINX)

    # transit zero coord by y_scrollbar
    def _update_zero_y_coord(self, event):
        self.current_zero_coord[1] = int(self.y_bar.get()[0] * 2 * MAXY + MINY)

    # change line text visible
    def _change_line_text_flag(self, event):
        self.line_text_flag = True if self.line_text_flag == False else False
        self.redraw_scene()

    # set color and width from current_line
    def _set_color_width_from_line(self, line: Line):
        if line is not None:
            self.line_color = line.color
            self.line_width = line.width
            self.color_button.config(fg=line.color)
            self.width_slider.set(line.width)

    # set color
    def _set_color(self):
        color = askcolor()[1]
        if color is not None:
            self.line_color = color
            self.color_button.config(fg=f'{color}')
            if self.work_mode == WorkingMode.edit_mode:
                if self.current_line is not None:
                    self.current_line.color = color
                for i in self.current_lines:
                    i.color = color
                self.redraw_scene()

    # set width
    def _set_width(self, event):
        self.line_width = self.width_slider.get()
        if self.work_mode == WorkingMode.edit_mode:
            if self.current_line is not None:
                self.current_line.width = self.width_slider.get()
            for i in self.current_lines:
                i.width = self.width_slider.get()
            self.redraw_scene()

    # set edit mode
    def _set_edit(self):
        self.canvas.config(cursor="fleur")
        self.edit_button.config(relief=SUNKEN)
        self.add_button.config(relief=RAISED)
        self.line_points = [None, None]
        self.current_line = None
        self.current_lines = []
        self.work_mode = WorkingMode.edit_mode
        self.line_button.config(text="Изменить линию", command=self._open_edit_line_form)
        self.operations_2d_button.grid(row=5, column=7, padx=5, pady=5, columnspan=3, sticky=NSEW)
        self.operations_3d_button.grid(row=5, column=10, padx=5, pady=5, columnspan=3, sticky=NSEW)
        self.redraw_scene()

    # set add mode
    def _set_add(self):
        self.canvas.config(cursor="pencil")
        self.edit_button.config(relief=RAISED)
        self.add_button.config(relief=SUNKEN)
        self.line_points = [None, None]
        self.current_line = None
        self.current_lines = []
        self.work_mode = WorkingMode.add_mode
        self.line_button.config(text="Добавить линию", command=self._open_add_line_form)
        self.operations_2d_button.grid_remove()
        self.operations_3d_button.grid_remove()
        self.redraw_scene()

    # set projection mode methods
    def _set_xy_projection(self):
        self.projection_mode = ProjectionMode.xy
        self.xy_button.config(relief=SUNKEN)
        self.zy_button.config(relief=RAISED)
        self.xz_button.config(relief=RAISED)
        self.redraw_scene()

    def _set_zy_projection(self):
        self.projection_mode = ProjectionMode.zy
        self.xy_button.config(relief=RAISED)
        self.zy_button.config(relief=SUNKEN)
        self.xz_button.config(relief=RAISED)
        self.redraw_scene()

    def _set_xz_projection(self):
        self.projection_mode = ProjectionMode.xz
        self.xy_button.config(relief=RAISED)
        self.zy_button.config(relief=RAISED)
        self.xz_button.config(relief=SUNKEN)
        self.redraw_scene()

    # handler canvas motion event
    def _cursor_motion(self, event):
        self._fill_status_bar(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)
        self.redraw_scene()

    # fill status bar label
    def _fill_status_bar(self, x, y):
        if self.work_mode == WorkingMode.add_mode:
            if self.projection_mode == ProjectionMode.xy:
                self.status_bar.config(
                    text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))
            if self.projection_mode == ProjectionMode.xz:
                self.status_bar.config(
                    text="x:{}, z:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))
            if self.projection_mode == ProjectionMode.zy:
                self.status_bar.config(
                    text="z:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line, self.line_color, self.line_width
                    ))

        if self.work_mode == WorkingMode.edit_mode:
            if self.projection_mode == ProjectionMode.xy:
                self.status_bar.config(
                    text="x:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))
            if self.projection_mode == ProjectionMode.xz:
                self.status_bar.config(
                    text="x:{}, z:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))
            if self.projection_mode == ProjectionMode.zy:
                self.status_bar.config(
                    text="z:{}, y:{}, current line: {}, color: {}, width: {}".format(
                        x, y, self.current_line,
                        self.current_line.color if self.current_line is not None else None,
                        self.current_line.width if self.current_line is not None else None
                    ))

    # left button click and motion (draw line or transit)
    def _canvas_b1_motion(self, event):
        self.current_mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x,
                                                     self.current_zero_coord[1] + event.y)
        self.redraw_scene()
        match self.work_mode:
            case WorkingMode.add_mode:
                self._add_line()
            case WorkingMode.edit_mode:
                self._transit_line()
        self.prev_mouse = self.current_mouse.copy()
        self._fill_status_bar(self.current_mouse[0], self.current_mouse[1])

    # release left button (end drawing or transit line)
    def _canvas_b1_release(self, event):
        self.prev_mouse = None
        self.current_mouse = None
        self.line_points = [None, None]
        self.transit_line_deltas = None
        self.transit = TransitMode.nothing
        match self.work_mode:
            case WorkingMode.add_mode:
                self.lines.append(self.current_line)
            case WorkingMode.edit_mode:
                self.transit = TransitMode.nothing

    # left button click (choose line)
    def _canvas_b1_click(self, event):
        if self.work_mode == WorkingMode.edit_mode:
            mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)
            flag = False
            for i in range(len(self.lines)):
                if self._is_cursor_on_line(mouse[0], mouse[1], self.lines[i]):
                    self.current_line = self.lines[i]
                    flag = True
                    break
            if not flag:
                self.current_line = None
            self.current_lines = []
            self._set_color_width_from_line(self.current_line)
            self._fill_status_bar(mouse[0], mouse[1])
            self.redraw_scene()

    def _canvas_control_b1_clicked(self, event):
        if self.work_mode == WorkingMode.edit_mode:
            mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x, self.current_zero_coord[1] + event.y)
            flag = False
            for i in range(len(self.lines)):
                if self._is_cursor_on_line(mouse[0], mouse[1], self.lines[i]):
                    if self.lines[i] not in self.current_lines:
                        self.current_lines.append(self.lines[i])
                    flag = True
            if not flag:
                self.current_lines = []
            self.current_line = None
            if flag:
                self._set_color_width_from_line(self.current_lines[-1])
            self._fill_status_bar(mouse[0], mouse[1])
            self.redraw_scene()

    def _canvas_control_b1_motion_release(self, event):
        self.prev_mouse = None
        self.current_mouse = None
        self.line_points = [None, None]
        self.rect_start_pos = None

    def _canvas_control_b1_motion(self, event):
        self.current_mouse = self._check_mouse_coord(self.current_zero_coord[0] + event.x,
                                                     self.current_zero_coord[1] + event.y)
        if self.rect_start_pos is None:
            self.current_lines = []
            self.rect_start_pos = self.current_mouse.copy()

        self.redraw_scene()
        if self.work_mode == WorkingMode.edit_mode:
            self._draw_rect()
            self._get_lines_in_rect()
        self.prev_mouse = self.current_mouse.copy()
        self._fill_status_bar(self.current_mouse[0], self.current_mouse[1])

    # calculate methods
    def _get_lines_in_rect(self):
        for i in self.lines:
            p1 = self._get_canvas_coord_from_projection_point(i.p1)
            p2 = self._get_canvas_coord_from_projection_point(i.p2)
            if p1[0] >= min(self.rect_start_pos[0], self.current_mouse[0]) \
                    and p1[0] <= max(self.rect_start_pos[0], self.current_mouse[0]) \
                    and p1[1] >= min(self.rect_start_pos[1], self.current_mouse[1]) \
                    and p1[1] <= max(self.rect_start_pos[1], self.current_mouse[1]) \
                    and p2[0] >= min(self.rect_start_pos[0], self.current_mouse[0]) \
                    and p2[0] <= max(self.rect_start_pos[0], self.current_mouse[0]) \
                    and p2[1] >= min(self.rect_start_pos[1], self.current_mouse[1]) \
                    and p2[1] <= max(self.rect_start_pos[1], self.current_mouse[1]):
                if i not in self.current_lines:
                    self.current_lines.append(i)
            else:
                if i in self.current_lines:
                    self.current_lines.remove(i)


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
        if self.projection_mode == ProjectionMode.xy:
            return Point(self.current_mouse[0], self.current_mouse[1], 0)
        elif self.projection_mode == ProjectionMode.xz:
            return Point(self.current_mouse[0], 0, self.current_mouse[1])
        else:
            return Point(0, self.current_mouse[1], self.current_mouse[0])

    # convert point coord to canvas coord
    def _get_canvas_coord_from_projection_point(self, point):
        if isinstance(point, Point):
            if self.projection_mode == ProjectionMode.xy:
                return [point.x, point.y]
            elif self.projection_mode == ProjectionMode.xz:
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
        self.current_line = buffer_line
        self._draw_line(self.current_line)

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
                fill="red" if (self.current_line == line or line in self.current_lines)
                              and self.work_mode != WorkingMode.add_mode else line.color,
                smooth=True
            )
            # drawing line text
            if self.line_text_flag:
                canvas_p1_projection = self._get_canvas_coord_from_projection_point(line.p1)
                canvas_p2_projection = self._get_canvas_coord_from_projection_point(line.p2)
                anchor_p1 = self._get_line_text_anchor(canvas_p1_projection)
                anchor_p2 = self._get_line_text_anchor(canvas_p2_projection)
                opt1 = self._get_line_text_options(line.p1, anchor_p1)
                opt2 = self._get_line_text_options(line.p2, anchor_p2)
                self.canvas.create_text(canvas_p1_projection[0], canvas_p1_projection[1], opt1)
                self.canvas.create_text(canvas_p2_projection[0], canvas_p2_projection[1], opt2)

    # draw rect
    def _draw_rect(self):
        if self.current_mouse is not None and self.rect_start_pos is not None:
            self.canvas.create_rectangle(
                self.rect_start_pos[0],
                self.rect_start_pos[1],
                self.current_mouse[0],
                self.current_mouse[1],
                width=1,
                dash=(5, 3),
                outline="white"
            )

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
            if self.transit == TransitMode.nothing:
                for i in range(len(self.lines)):
                    if isinstance(self.lines[i], Line):
                        # match with p1
                        point_to_canvas = self._get_canvas_coord_from_projection_point(self.lines[i].p1)
                        if math.fabs(point_to_canvas[0] - self.prev_mouse[0]) <= eps \
                                and math.fabs(point_to_canvas[1] - self.prev_mouse[1]) <= eps:
                            self.transit = TransitMode.point1
                            self.current_line = self.lines[i]
                            break

                        # match with p2
                        point_to_canvas = self._get_canvas_coord_from_projection_point(self.lines[i].p2)
                        if math.fabs(point_to_canvas[0] - self.prev_mouse[0]) <= eps \
                                and math.fabs(point_to_canvas[1] - self.prev_mouse[1]) <= eps:
                            self.transit = TransitMode.point2
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
                            self.transit = TransitMode.parallel
                            break

            # check flags
            if self.transit == TransitMode.point1:
                if self.projection_mode == ProjectionMode.xy:
                    self.current_line.p1.x = self.current_mouse[0]
                    self.current_line.p1.y = self.current_mouse[1]
                elif self.projection_mode == ProjectionMode.xz:
                    self.current_line.p1.x = self.current_mouse[0]
                    self.current_line.p1.z = self.current_mouse[1]
                else:
                    self.current_line.p1.z = self.current_mouse[0]
                    self.current_line.p1.y = self.current_mouse[1]
            if self.transit == TransitMode.point2:
                if self.projection_mode == ProjectionMode.xy:
                    self.current_line.p2.x = self.current_mouse[0]
                    self.current_line.p2.y = self.current_mouse[1]
                elif self.projection_mode == ProjectionMode.xz:
                    self.current_line.p2.x = self.current_mouse[0]
                    self.current_line.p2.z = self.current_mouse[1]
                else:
                    self.current_line.p2.z = self.current_mouse[0]
                    self.current_line.p2.y = self.current_mouse[1]
            if self.transit == TransitMode.parallel:
                # check on bounds p1, p2
                p1 = self._get_canvas_coord_from_projection_point(self.current_line.p1)
                p2 = self._get_canvas_coord_from_projection_point(self.current_line.p2)
                is_not_bound = self._check_point_coord(p1[0], p1[1]) and self._check_point_coord(p2[0], p2[1])
                if is_not_bound:
                    if self.projection_mode == ProjectionMode.xy:
                        self.current_line.p1.x = self.current_mouse[0] + self.transit_line_deltas[0]
                        self.current_line.p2.x = self.current_mouse[0] - self.transit_line_deltas[2]
                        self.current_line.p1.y = self.current_mouse[1] + self.transit_line_deltas[1]
                        self.current_line.p2.y = self.current_mouse[1] - self.transit_line_deltas[3]
                    if self.projection_mode == ProjectionMode.xz:
                        self.current_line.p1.x = self.current_mouse[0] + self.transit_line_deltas[0]
                        self.current_line.p2.x = self.current_mouse[0] - self.transit_line_deltas[2]
                        self.current_line.p1.z = self.current_mouse[1] + self.transit_line_deltas[1]
                        self.current_line.p2.z = self.current_mouse[1] - self.transit_line_deltas[3]
                    if self.projection_mode == ProjectionMode.zy:
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
    # redraw scene
    def redraw_scene(self):
        self.canvas.delete("all")
        # draw lines primitive
        for i in range(len(self.lines)):
            self._draw_line(self.lines[i])

    # save/load methods
    def _save_file(self):
        file_path = tkinter.filedialog.asksaveasfilename(
            filetypes=[('JSON File', '*.json')],
        )
        if file_path != "":
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(self.lines, file, cls=MyEncoder)
                tkinter.messagebox.showinfo("Сохранение", "Файл успешно сохранен!")
            except:
                tkinter.messagebox.showerror("Ошибка сохранения", "Ошибка при записи в файл!")
        else:
            tkinter.messagebox.showinfo("Сохранение", "Файл не был сохранен!")

    def _load_file(self):
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=[('JSON File', '*.json')],
        )
        if file_path != "":
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.lines = json.load(file, object_hook=decode_object)
                self.current_line = None
                self.current_lines = []
                self.line_width = 1
                self.width_slider.set(1)
                self.line_color = "black"
                self.color_button.config(fg="black")
                self.redraw_scene()
                tkinter.messagebox.showinfo("Загрузка", "Файл успешно открыт!")
            except:
                tkinter.messagebox.showerror("Ошибка загрузки", "Ошибка при чтении файла!")
        else:
            tkinter.messagebox.showinfo("Загрузка", "Файл не выбран!")

    # mainloop
    def start(self):
        self.root.mainloop()
