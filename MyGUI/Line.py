class Point:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = 0
            self.y = 0
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", 1)"


class Line:
    def __init__(self, p1=None, p2=None, color=None, width=None):
        self.p1 = Point()
        self.p2 = Point()
        self.color = "black"
        self.width = 1
        if p1 is not None:
            if isinstance(p1, Point):
                self.p1.x = p1.x
                self.p1.y = p1.y
        if p2 is not None:
            if isinstance(p2, Point):
                self.p2.x = p2.x
                self.p2.y = p2.y
        if color is not None:
            if isinstance(color, str):
                self.color = color
        if width is not None:
            if isinstance(width, int):
                self.width = width

    def __str__(self):
        return str(self.p1.y - self.p2.y) + "x + " \
               + str(self.p2.x - self.p1.x) + "y + " \
               + str(self.p1.x * self.p2.y - self.p2.x * self.p1.y) + " = 0"