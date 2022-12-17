import numpy as np
from Primitives import *
from FormFor2dOperation import ProjectionMode

class Calculate:
    @staticmethod
    def transit_2d(lines, projection: ProjectionMode):
        points = []
        for i in lines:
            if isinstance(i, Line):
                points.append(i.p1)
                points.append(i.p2)

        match projection:
            case ProjectionMode.xy:
                matrix = np.array([i.x, i.y] for i in points)
            case ProjectionMode.zy:
                matrix = np.array([i.z, i.y] for i in points)
            case ProjectionMode.xz:
                matrix = np.array([i.x, i.z] for i in points)

