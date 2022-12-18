import numpy as np
from Primitives import *
from Enums import *
import math


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
    def transit_2d(lines, projection: ProjectionMode, m: int, n: int,
                   a: int, b: int, alpha: int, z1: int, z2: int, p: int, q: int):
        points = Calculate._get_points_from_lines(lines)
        # some test
        test_m = np.array(
            [
                [a * math.cos(alpha), a * math.sin(alpha), 0],
                [-b * math.sin(alpha), b * math.cos(alpha), 0],
                [
                    a * m * math.cos(alpha) - b * n * math.sin(alpha),
                    a * m * math.sin(alpha) + b * n * math.cos(alpha),
                    1
                ]
            ]
        ).dot(
            np.array(
                [
                    [z1, 0, p * z1],
                    [0, z2, q * z2],
                    [0, 0, 1]
                ]
            )
        )
        transfer_matrix = np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [m, n, 1],
            ]
        )
        matrix = []
        match projection:
            case ProjectionMode.xy:
                # read points
                for i in points:
                    matrix.append([i.x, i.y, i.ok])
                matrix = np.array(matrix)

                # calculate
                # res = matrix.dot(transfer_matrix)
                res = matrix.dot(test_m)

                # write res points in lines
                for i in range(len(points)):
                    points[i].x = int(res[i][0])
                    points[i].y = int(res[i][1])
                    points[i].ok = int(res[i][2])
                Calculate._write_points_to_lines(points, lines)
            case ProjectionMode.zy:
                for i in points:
                    matrix.append([i.z, i.y, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(transfer_matrix)
                for i in range(len(points)):
                    points[i].z = int(res[i][0])
                    points[i].y = int(res[i][1])
                    points[i].ok = int(res[i][2])
                Calculate._write_points_to_lines(points, lines)
            case ProjectionMode.xz:
                for i in points:
                    matrix.append([i.x, i.z, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(transfer_matrix)
                for i in range(len(points)):
                    points[i].x = int(res[i][0])
                    points[i].z = int(res[i][1])
                    points[i].ok = int(res[i][2])
                Calculate._write_points_to_lines(points, lines)
