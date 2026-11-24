"""Тесты математики: тор, столкновения, время жизни ракеты."""

import math
import unittest

from src.config import HEIGHT, MISSILE_LIFETIME, MISSILE_SPEED, WIDTH
from src.models.game_objects import Missile, Ship
from src.models.sprite import Sprite
from src.models.vector import Vector2


class TestVectorWrap(unittest.TestCase):
    """Тороидальная геометрия поля."""

    def test_wrap_right_edge(self) -> None:
        """Объект, ушедший за правый край, появляется слева."""
        point = Vector2(WIDTH + 10, 100).wrap(WIDTH, HEIGHT)
        self.assertAlmostEqual(point.x, 10)
        self.assertAlmostEqual(point.y, 100)

    def test_wrap_left_edge(self) -> None:
        """Отрицательная координата X переносится на правую сторону."""
        point = Vector2(-15, 50).wrap(WIDTH, HEIGHT)
        self.assertAlmostEqual(point.x, WIDTH - 15)

    def test_toroidal_distance_across_edge(self) -> None:
        """Расстояние через край короче, чем «напрямую» через поле."""
        left = Vector2(10, 100)
        right = Vector2(WIDTH - 10, 100)
        distance = left.toroidal_distance(right, WIDTH, HEIGHT)
        self.assertAlmostEqual(distance, 20)


class TestCollisions(unittest.TestCase):
    """Круговые хитбоксы на торе."""

    def test_overlap(self) -> None:
        """Два объекта рядом считаются столкнувшимися."""
        first = Sprite(Vector2(100, 100), Vector2(), 0, 0, radius=20)
        second = Sprite(Vector2(130, 100), Vector2(), 0, 0, radius=20)
        self.assertTrue(first.collide(second))

    def test_no_overlap(self) -> None:
        """Далеко стоящие объекты не сталкиваются."""
        first = Sprite(Vector2(100, 100), Vector2(), 0, 0, radius=20)
        second = Sprite(Vector2(400, 400), Vector2(), 0, 0, radius=20)
        self.assertFalse(first.collide(second))


class TestMissile(unittest.TestCase):
    """Ракеты не должны пересекать поле по короткой стороне."""

    def test_lifetime_shorter_than_short_side(self) -> None:
        """Путь за время жизни меньше HEIGHT."""
        max_travel = MISSILE_LIFETIME * MISSILE_SPEED
        self.assertLess(max_travel, min(WIDTH, HEIGHT))

    def test_missile_dies_off_screen(self) -> None:
        """Ракета, улетевшая за край, помечается мёртвой."""
        missile = Missile(Vector2(WIDTH - 1, 10), Vector2(20, 0), 0)
        missile.update()
        self.assertFalse(missile.alive)


class TestShip(unittest.TestCase):
    """Базовое поведение корабля."""

    def test_shoot_spawns_ahead(self) -> None:
        """Ракета появляется впереди носа, не в центре корабля."""
        ship = Ship(Vector2(400, 300))
        ship.angle = 0
        missile = ship.shoot()
        # Угол 0 — вверх (спрайт корабля), ракета появляется выше центра.
        self.assertLess(missile.position.y, ship.position.y)

    def test_thrust_increases_speed(self) -> None:
        """При включённом двигателе скорость растёт."""
        ship = Ship(Vector2(400, 300))
        ship.set_thrust(True)
        ship.update()
        self.assertGreater(ship.velocity.length(), 0)

    def test_forward_unit_length(self) -> None:
        """Направление носа — единичный вектор."""
        ship = Ship(Vector2(0, 0))
        ship.angle = math.pi / 2
        forward = ship.forward()
        self.assertAlmostEqual(forward.length(), 1.0, places=5)


if __name__ == "__main__":
    unittest.main()
