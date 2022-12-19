import numpy as np
from Primitives import *
from Enums import *
import math


class Calculate:
    @staticmethod
    def _normalization(matrix: np.array):
        for i in range(len(matrix)):
            if matrix[i][-1] != 1:
                for j in range(len(matrix[i])):
                    matrix[i][j] /= matrix[i][-1]

    @staticmethod
    def _get_points_from_lines(lines):
        points = []
        for i in lines:
            if isinstance(i, Line):
                points.append(i.p1)
                points.append(i.p2)
        return points

    @staticmethod
    def calculate_2d(lines, projection: ProjectionMode, m: int, n: int,
                   a: float, b: float, alpha: int, z1: int, z2: int, p: float, q: float):
        angle_rad = alpha * math.pi / 180
        points = Calculate._get_points_from_lines(lines)
        # some test
        calculate_matrix = np.array(
            [
                [a * math.cos(angle_rad), a * math.sin(angle_rad), 0],
                [-b * math.sin(angle_rad), b * math.cos(angle_rad), 0],
                [
                    a * m * math.cos(angle_rad) - b * n * math.sin(angle_rad),
                    a * m * math.sin(angle_rad) + b * n * math.cos(angle_rad),
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
        matrix = []
        match projection:
            case ProjectionMode.xy:
                for i in points:
                    matrix.append([i.x, i.y, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(calculate_matrix)
                Calculate._normalization(res)
                for i in range(len(points)):
                    points[i].x = round(res[i][0])
                    points[i].y = round(res[i][1])
                    points[i].ok = round(res[i][2])
            case ProjectionMode.zy:
                for i in points:
                    matrix.append([i.z, i.y, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(calculate_matrix)
                Calculate._normalization(res)
                for i in range(len(points)):
                    points[i].z = round(res[i][0])
                    points[i].y = round(res[i][1])
                    points[i].ok = round(res[i][2])
            case ProjectionMode.xz:
                for i in points:
                    matrix.append([i.x, i.z, i.ok])
                matrix = np.array(matrix)
                res = matrix.dot(calculate_matrix)
                Calculate._normalization(res)
                for i in range(len(points)):
                    points[i].x = round(res[i][0])
                    points[i].z = round(res[i][1])
                    points[i].ok = round(res[i][2])
