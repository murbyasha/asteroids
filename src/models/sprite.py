"""Базовый движущийся объект на тороидальном поле."""

from __future__ import annotations

from src.config import HEIGHT, WIDTH
from src.models.vector import Vector2


class Sprite:
    """Объект с позицией, скоростью, углом и круговым хитбоксом."""

    def __init__(
        self,
        position: Vector2,
        velocity: Vector2,
        angle: float,
        angle_vel: float,
        radius: float,
        lifespan: float | None = None,
    ) -> None:
        """Создать спрайт.

        Args:
            position: центр объекта в пикселях.
            velocity: линейная скорость, пиксели за кадр.
            angle: ориентация в радианах (0 — вправо).
            angle_vel: угловая скорость, радианы за кадр.
            radius: радиус столкновения.
            lifespan: время жизни в кадрах или ``None``, если бессрочно.
        """
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.angle = angle
        self.angle_vel = angle_vel
        self.radius = radius
        self.lifespan = lifespan
        self.age = 0.0
        self.alive = True

    def update(self) -> None:
        """Сдвинуть объект на один кадр и при необходимости обернуть поле."""
        self.angle += self.angle_vel
        self.position = (self.position + self.velocity).wrap(WIDTH, HEIGHT)
        self.age += 1
        if self.lifespan is not None and self.age >= self.lifespan:
            self.alive = False

    def collide(self, other: "Sprite") -> bool:
        """True, если круги хитбоксов пересекаются на торе."""
        distance = self.position.toroidal_distance(
            other.position,
            WIDTH,
            HEIGHT,
        )
        return distance <= self.radius + other.radius

    def forward(self) -> Vector2:
        """Единичный вектор носа.

        Спрайт корабля смотрит вверх, поэтому угол 0 — это направление
        (0, -1) в координатах pygame (ось Y вниз).
        """
        return Vector2(0.0, -1.0).rotate(self.angle)
