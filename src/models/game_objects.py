"""Корабль, астероид, ракета и анимация взрыва."""

from __future__ import annotations

import random

from src.config import (
    ASTEROID_MAX_ANG_VEL,
    ASTEROID_MAX_VEL,
    ASTEROID_MIN_VEL,
    ASTEROID_RADIUS,
    EXPLOSION_FRAME_DURATION,
    EXPLOSION_FRAMES,
    FRICTION,
    HEIGHT,
    MISSILE_LIFETIME,
    MISSILE_RADIUS,
    MISSILE_SPEED,
    SHIP_NOSE_OFFSET,
    SHIP_RADIUS,
    SHIP_THRUST,
    WIDTH,
)
from src.models.sprite import Sprite
from src.models.vector import Vector2


class Ship(Sprite):
    """Корабль игрока: вращение, тяга и выстрел из носа."""

    def __init__(self, position: Vector2) -> None:
        """Поставить корабль в ``position`` без скорости."""
        super().__init__(
            position=position,
            velocity=Vector2(0.0, 0.0),
            angle=0.0,
            angle_vel=0.0,
            radius=SHIP_RADIUS,
        )
        self.thrusting = False

    def set_angle_vel(self, value: float) -> None:
        """Задать угловую скорость (стрелки влево/вправо)."""
        self.angle_vel = value

    def set_thrust(self, on: bool) -> None:
        """Включить или выключить двигатель (стрелка вверх)."""
        self.thrusting = on

    def update(self) -> None:
        """Ускорить при тяге, затем учесть сопротивление среды."""
        if self.thrusting:
            self.velocity = self.velocity + self.forward() * SHIP_THRUST
        # Сопротивление: скорость затухает, пока корабль не остановится.
        self.velocity = self.velocity * (1.0 - FRICTION)
        super().update()

    def shoot(self) -> "Missile":
        """Создать ракету у носа с суммой скорости корабля и выстрела."""
        nose = self.position + self.forward() * SHIP_NOSE_OFFSET
        velocity = self.velocity + self.forward() * MISSILE_SPEED
        return Missile(nose, velocity, self.angle)

    def reset(self) -> None:
        """Возродить корабль в центре поля без скорости."""
        self.position = Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0.0
        self.angle_vel = 0.0
        self.thrusting = False
        self.alive = True


class Asteroid(Sprite):
    """Камень со случайной линейной и угловой скоростью."""

    def __init__(
        self,
        position: Vector2,
        velocity: Vector2,
        angle_vel: float,
    ) -> None:
        """Создать астероид в заданной точке."""
        super().__init__(
            position=position,
            velocity=velocity,
            angle=random.uniform(0.0, 6.283185307179586),
            angle_vel=angle_vel,
            radius=ASTEROID_RADIUS,
        )

    @classmethod
    def random_away_from(cls, ship: Ship, safe_distance: float) -> "Asteroid":
        """Сгенерировать астероид не ближе ``safe_distance`` к кораблю."""
        for _ in range(40):
            position = Vector2(
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
            )
            if position.toroidal_distance(ship.position, WIDTH, HEIGHT) >= (
                safe_distance
            ):
                break
        speed = random.uniform(ASTEROID_MIN_VEL, ASTEROID_MAX_VEL)
        direction = Vector2(
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0),
        ).normalized()
        if direction.length() == 0:
            direction = Vector2(1.0, 0.0)
        angle_vel = random.uniform(-ASTEROID_MAX_ANG_VEL, ASTEROID_MAX_ANG_VEL)
        return cls(position, direction * speed, angle_vel)


class Missile(Sprite):
    """Ракета с ограниченным временем жизни, без тороидального «вечного» полёта."""

    def __init__(self, position: Vector2, velocity: Vector2, angle: float) -> None:
        """Создать ракету, летящую в сторону ``angle``."""
        super().__init__(
            position=position,
            velocity=velocity,
            angle=angle,
            angle_vel=0.0,
            radius=MISSILE_RADIUS,
            lifespan=MISSILE_LIFETIME,
        )

    def update(self) -> None:
        """Двигать ракету по прямой без оборачивания поля.

        Если выйти за край, объект просто исчезает — это и есть смысл
        ограниченного времени жизни.
        """
        self.angle += self.angle_vel
        self.position = self.position + self.velocity
        self.age += 1
        off_screen = (
            self.position.x < 0
            or self.position.x > WIDTH
            or self.position.y < 0
            or self.position.y > HEIGHT
        )
        if off_screen or (
            self.lifespan is not None and self.age >= self.lifespan
        ):
            self.alive = False


class Explosion(Sprite):
    """Покадровая анимация взрыва, исчезает после последнего кадра."""

    def __init__(self, position: Vector2) -> None:
        """Запустить взрыв в точке столкновения."""
        super().__init__(
            position=position,
            velocity=Vector2(0.0, 0.0),
            angle=0.0,
            angle_vel=0.0,
            radius=0.0,
            lifespan=EXPLOSION_FRAMES * EXPLOSION_FRAME_DURATION,
        )

    def frame_index(self) -> int:
        """Номер кадра спрайт-листа в диапазоне ``[0, EXPLOSION_FRAMES)``."""
        index = int(self.age // EXPLOSION_FRAME_DURATION)
        return min(index, EXPLOSION_FRAMES - 1)
