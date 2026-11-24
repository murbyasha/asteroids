"""Двумерный вектор для позиций и скоростей."""

from __future__ import annotations

import math
from typing import Tuple


class Vector2:
    """Вектор на плоскости с обычными операциями.

    Используется и как точка (позиция), и как направление (скорость).
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """Создать вектор с координатами ``x`` и ``y``."""
        self.x = float(x)
        self.y = float(y)

    def copy(self) -> "Vector2":
        """Вернуть независимую копию вектора."""
        return Vector2(self.x, self.y)

    def as_tuple(self) -> Tuple[float, float]:
        """Координаты в виде кортежа (x, y)."""
        return self.x, self.y

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vector2":
        return Vector2(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        """Евклидова длина вектора."""
        return math.hypot(self.x, self.y)

    def normalized(self) -> "Vector2":
        """Единичный вектор того же направления.

        Для нулевого вектора возвращается копия (0, 0).
        """
        length = self.length()
        if length == 0:
            return Vector2(0.0, 0.0)
        return self / length

    def rotate(self, angle: float) -> "Vector2":
        """Повернуть вектор на ``angle`` радиан против часовой стрелки."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    def wrap(self, width: float, height: float) -> "Vector2":
        """Тороидальная геометрия: выход за край переносит на противоположный."""
        return Vector2(self.x % width, self.y % height)

    def distance_to(self, other: "Vector2") -> float:
        """Обычное евклидово расстояние (без учёта тора)."""
        return (self - other).length()

    def toroidal_distance(
        self,
        other: "Vector2",
        width: float,
        height: float,
    ) -> float:
        """Кратчайшее расстояние на торе.

        Берём минимальную из прямых разностей по каждой оси и разностей
        «через край» (width - dx, height - dy).
        """
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        dx = min(dx, width - dx)
        dy = min(dy, height - dy)
        return math.hypot(dx, dy)

    def __repr__(self) -> str:
        return f"Vector2({self.x:.2f}, {self.y:.2f})"
