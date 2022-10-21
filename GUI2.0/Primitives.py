class Point:
    def __init__(self, x=None, y=None, z=None, ok=None):
        self.x = 0
        self.y = 0
        self.z = 0
        self.ok = 1
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        if ok is not None:
            self.ok = ok

    def __str__(self):
        return "x: {}, y: {}, z: {}, ok: {}".format(
            self.x, self.y, self.z, self.ok)


class Line:
    def __init__(self, p1=None, p2=None, color=None, width=None):
        self.p1 = Point()
        self.p2 = Point()
        self.color = "#000000"
        self.width = 1
        if p1 is not None:
            if isinstance(p1, Point):
                self.p1.x = p1.x
                self.p1.y = p1.y
                self.p1.z = p1.z
                self.p1.ok = p1.ok
        if p2 is not None:
            if isinstance(p2, Point):
                self.p2.x = p2.x
                self.p2.y = p2.y
                self.p2.z = p2.z
                self.p2.ok = p2.ok
        if color is not None:
            if isinstance(color, str):
                self.color = color
        if width is not None:
            if isinstance(width, int):
                self.width = width

    def get_directive_vector(self):
        return f"({self.p2.x - self.p1.x}, {self.p2.y - self.p1.y}, {self.p2.z - self.p1.z})"

    def __str__(self):
        return self.get_directive_vector()
