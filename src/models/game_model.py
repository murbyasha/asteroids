"""Состояние партии: заставка, игра, столкновения, жизни и очки."""

from __future__ import annotations

from typing import List

from src.config import (
    ASTEROID_SAFE_DISTANCE,
    ASTEROID_SPAWN_INTERVAL_MS,
    HEIGHT,
    MAX_ASTEROIDS,
    START_LIVES,
    START_SCORE,
    WIDTH,
)
from src.models.game_objects import Asteroid, Explosion, Missile, Ship
from src.models.vector import Vector2


class GameModel:
    """Модель данных игры без привязки к отрисовке.

    Хранит корабль, списки астероидов/ракет/взрывов, счёт и жизни.
    Пока ``started`` ложно, на экране должна быть заставка.
    """

    def __init__(self) -> None:
        """Создать начальное состояние: 3 жизни, 0 очков, заставка."""
        self.lives = START_LIVES
        self.score = START_SCORE
        self.started = False
        self.game_over = False
        self.ship = Ship(Vector2(WIDTH / 2, HEIGHT / 2))
        self.asteroids: List[Asteroid] = []
        self.missiles: List[Missile] = []
        self.explosions: List[Explosion] = []
        self._spawn_accumulator_ms = 0.0

    def start(self) -> None:
        """Начать или перезапустить партию после клика по заставке."""
        if self.started:
            return
        self.started = True
        self.game_over = False
        if self.lives <= 0:
            self.lives = START_LIVES
            self.score = START_SCORE
        self.ship.reset()
        self.asteroids.clear()
        self.missiles.clear()
        self.explosions.clear()
        # Сразу создать первый астероид, дальше — по таймеру.
        self._spawn_accumulator_ms = ASTEROID_SPAWN_INTERVAL_MS

    def shoot(self) -> None:
        """Выстрелить, если партия идёт."""
        if not self.started:
            return
        self.missiles.append(self.ship.shoot())

    def update(self, dt_ms: float) -> None:
        """Продвинуть физику на ``dt_ms`` миллисекунд.

        Спавн астероидов привязан к реальному времени, движение —
        к кадрам (один вызов = один кадр).
        """
        if not self.started:
            return

        self.ship.update()
        for asteroid in self.asteroids:
            asteroid.update()
        for missile in self.missiles:
            missile.update()
        for explosion in self.explosions:
            explosion.update()

        self._handle_collisions()
        self._prune()
        self._spawn_asteroids(dt_ms)

        if self.lives <= 0:
            self._end_game()

    def _handle_collisions(self) -> None:
        """Обработать попадания ракет и столкновения корабля с камнями."""
        for missile in self.missiles:
            if not missile.alive:
                continue
            for asteroid in self.asteroids:
                if asteroid.alive and missile.collide(asteroid):
                    missile.alive = False
                    asteroid.alive = False
                    self.explosions.append(Explosion(asteroid.position))
                    self.score += 1
                    break

        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.collide(asteroid):
                asteroid.alive = False
                self.explosions.append(Explosion(asteroid.position))
                self.lives -= 1
                self.ship.reset()
                # Один удар за кадр, иначе камни у центра снимут несколько жизней.
                break

    def _prune(self) -> None:
        """Удалить уничтоженные и истёкшие объекты."""
        self.asteroids = [item for item in self.asteroids if item.alive]
        self.missiles = [item for item in self.missiles if item.alive]
        self.explosions = [item for item in self.explosions if item.alive]

    def _spawn_asteroids(self, dt_ms: float) -> None:
        """Периодически добавлять астероид, пока их меньше лимита."""
        self._spawn_accumulator_ms += dt_ms
        if self._spawn_accumulator_ms < ASTEROID_SPAWN_INTERVAL_MS:
            return
        self._spawn_accumulator_ms = 0.0
        if len(self.asteroids) >= MAX_ASTEROIDS:
            return
        self.asteroids.append(
            Asteroid.random_away_from(self.ship, ASTEROID_SAFE_DISTANCE)
        )

    def _end_game(self) -> None:
        """Остановить партию и снова показать заставку."""
        self.started = False
        self.game_over = True
        self.asteroids.clear()
        self.missiles.clear()
        self.ship.thrusting = False
        self.ship.set_angle_vel(0.0)
