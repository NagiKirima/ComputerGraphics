import numpy as np
from Primitives import *
from Enums import *


class Calculate:
    @staticmethod
    def _get_points_from_lines(lines):
        points = []
        for i in lines:
            if isinstance(i, Line):
                points.append(i.p1)
                points.append(i.p2)
        return points

    @staticmethod
    def _write_points_to_lines(points, lines):
        j = 0
        for i in range(len(lines)):
            if isinstance(lines[i], Line):
                lines[i].p1 = points[j]
                lines[i].p2 = points[j + 1]
                j += 2

    @staticmethod
    def transit_2d(lines, projection: ProjectionMode, m: int, n: int):
        points = Calculate._get_points_from_lines(lines)
        transfer_matrix = np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [m, n, 1],
            ]
        )
        match projection:
            case ProjectionMode.xy:
                matrix = []
                for i in points:
                    matrix.append([i.x, i.y, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(transfer_matrix)
                for i in range(len(points)):
                    points[i].x = res[i][0]
                    points[i].y = res[i][1]
                    points[i].ok = res[i][2]
                Calculate._write_points_to_lines(points, lines)
            case ProjectionMode.zy:
                matrix = []
                for i in points:
                    matrix.append([i.z, i.y, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(transfer_matrix)
                for i in range(len(points)):
                    points[i].z = res[i][0]
                    points[i].y = res[i][1]
                    points[i].ok = res[i][2]
                Calculate._write_points_to_lines(points, lines)
            case ProjectionMode.xz:
                matrix = []
                for i in points:
                    matrix.append([i.x, i.z, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(transfer_matrix)
                for i in range(len(points)):
                    points[i].x = res[i][0]
                    points[i].z = res[i][1]
                    points[i].ok = res[i][2]
                Calculate._write_points_to_lines(points, lines)
