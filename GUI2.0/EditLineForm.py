import math
import tkinter.messagebox
from tkinter import *
from Primitives import *
from Settings import BUTTON_FONT, LABEL_FONT, LEN
import GUI
import re


class EditLineForm(Toplevel):
    def __init__(self, mainapp, master=None):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.title("Edit Line")
        self.geometry("600x600")
        self.resizable(False, False)
        self.mainapp = mainapp
        self.field_object_list = []
        self.check = (self.register(self._is_valid), "%P")

        # widgets init
        self.send_button = Button(self, text="Изменить прямую", font=BUTTON_FONT,
                                  command=self._send_button_click)
        self.send_button.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.field = Canvas(self, highlightthickness=0)
        self.f = Frame(self.field)
        self.field.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        self.field.create_window(0, 0, window=self.f, anchor="nw")
        for i in range(6):
            self.f.columnconfigure(i, weight=1)

        # grid canvas objects
        if self.mainapp.current_line is not None:
            self._add_objects_in_list(self.mainapp.current_line)
            self._grid_canvas_objects(self.field_object_list[0], 0, self.mainapp.current_line)
        elif len(self.mainapp.current_lines) != 0:
            for i in range(len(self.mainapp.current_lines)):
                self._add_objects_in_list(self.mainapp.current_lines[i])
            row = 0
            for i in range(len(self.mainapp.current_lines)):
                self._grid_canvas_objects(self.field_object_list[i], row, self.mainapp.current_lines[i])
                row += 3

        # scrollbar
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.field.yview)
        self.scrollbar.grid(row=0, column=1, sticky=NS)
        self.field.config(yscrollcommand=self.scrollbar.set)
        self.field.bind("<Configure>", lambda e: self.field.configure(scrollregion=self.field.bbox("all")))

        # form grid configure
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    @staticmethod
    def _is_valid(value):
        if re.match("^-$|^$|-?(0|[1-9]\d*)(?<!-0)$", value) is not None:
            if value != "":
                return math.fabs(int(value)) <= LEN
            return True
        return False

    def _send_button_click(self):
        try:
            lines = []
            if self.mainapp.current_line is not None:
                lines.append(self._get_line_from_entries(self.field_object_list[0], self.mainapp.current_line))
                for i in range(len(self.mainapp.lines)):
                    if self.mainapp.lines[i] == self.mainapp.current_line:
                        self.mainapp.lines[i] = lines[0]
                        self.mainapp.current_line = lines[0]

            elif len(self.mainapp.current_lines) != 0:
                for i in range(len(self.field_object_list)):
                    lines.append(self._get_line_from_entries(self.field_object_list[i], self.mainapp.current_lines[i]))

                for i in range(len(self.field_object_list)):
                    for j in range(len(self.mainapp.lines)):
                        if self.mainapp.lines[j] == self.mainapp.current_lines[i]:
                            self.mainapp.current_lines[i] = lines[i]
                            self.mainapp.lines[j] = lines[i]

            self.mainapp.redraw_scene()
            self.destroy()
        except:
            tkinter.messagebox.showerror("Ошибка", f"Введите корректные значения в поля (-{LEN} <= value <= {LEN})")

    def _add_objects_in_list(self, line):
        self.field_object_list.append(
            [
                Label(self.f, text="x1:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
                Label(self.f, text="y1:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
                Label(self.f, text="z1:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
                Label(self.f, text="x2:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
                Label(self.f, text="y2:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
                Label(self.f, text="z2:", font=LABEL_FONT),
                Entry(self.f, validate="key", validatecommand=self.check),
            ]
        )
        # p1
        self.field_object_list[-1][1].insert(-1, str(line.p1.x))
        self.field_object_list[-1][3].insert(-1, str(line.p1.y))
        self.field_object_list[-1][5].insert(-1, str(line.p1.z))
        # p2
        self.field_object_list[-1][7].insert(-1, str(line.p2.x))
        self.field_object_list[-1][9].insert(-1, str(line.p2.y))
        self.field_object_list[-1][11].insert(-1, str(line.p2.z))

    def _grid_canvas_objects(self, objects, start_row, line):
        for j in range(len(objects)):
            row = start_row + 1
            if j > 5:
                row = start_row + 2
            objects[j].grid(row=row, column=j % 6, padx=5, pady=5, sticky=NSEW)
            Label(self.f, text=f"line: {line}",
                  font=LABEL_FONT).grid(row=start_row, column=0, columnspan=6, sticky=NSEW)

    def _get_line_from_entries(self, objects, line):
        return Line(
            Point(
                int(objects[1].get()),
                int(objects[3].get()),
                int(objects[5].get())
            ),
            Point(
                int(objects[7].get()),
                int(objects[9].get()),
                int(objects[11].get())
            ),
            line.color,
            line.width
        )

    def _on_closing(self):
        self.grab_release()
        self.destroy()
