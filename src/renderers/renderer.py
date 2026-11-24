"""Отрисовка фона, объектов и интерфейса."""

from __future__ import annotations

import math

import pygame

from src.assets import Images
from src.config import (
    DEBRIS_ALPHA,
    DEBRIS_SPEED,
    EXPLOSION_TILE,
    HEIGHT,
    WIDTH,
)
from src.models.game_model import GameModel
from src.models.sprite import Sprite
from src.widgets.hud import HUD
from src.widgets.splash import Splash


class Renderer:
    """Рисует один кадр по текущей модели.

    Динамический фон — полупрозрачный слой обломков, который сдвигается
    влево с постоянной скоростью. Два экземпляра стыкуются по горизонтали,
    чтобы движение было бесшовным.
    """

    def __init__(self, screen: pygame.Surface, images: Images) -> None:
        """Связать поверхность окна с загруженными картинками."""
        self.screen = screen
        self.images = images
        self.hud = HUD()
        self.splash = Splash(images.splash)
        self._debris_x = 0.0
        self._debris_layer = images.debris.copy()
        self._debris_layer.set_alpha(DEBRIS_ALPHA)

    def update_background(self) -> None:
        """Сдвинуть динамический фон влево на ``DEBRIS_SPEED`` пикселей."""
        self._debris_x = (self._debris_x - DEBRIS_SPEED) % WIDTH

    def draw(self, model: GameModel) -> None:
        """Нарисовать полный кадр: фон, объекты (если игра идёт), HUD."""
        self.update_background()
        self.screen.blit(self.images.nebula, (0, 0))
        self.screen.blit(self._debris_layer, (self._debris_x - WIDTH, 0))
        self.screen.blit(self._debris_layer, (self._debris_x, 0))

        if model.started:
            for asteroid in model.asteroids:
                self._blit_rotated(self.images.asteroid, asteroid)
            for missile in model.missiles:
                self._blit_rotated(self.images.missile, missile)
            ship_image = (
                self.images.ship_thrust
                if model.ship.thrusting
                else self.images.ship_idle
            )
            self._blit_rotated(ship_image, model.ship)
            for explosion in model.explosions:
                self._draw_explosion(explosion)

        if not model.started:
            self.splash.draw(self.screen)

        self.hud.draw(self.screen, model.lives, model.score)

    def _blit_rotated(self, image: pygame.Surface, sprite: Sprite) -> None:
        """Повернуть спрайт вокруг центра и нарисовать в позиции объекта.

        Спрайт смотрит вверх при угле 0. ``pygame.transform.rotate``
        крутит против часовой стрелки, поэтому берём отрицательные градусы.
        """
        degrees = -math.degrees(sprite.angle)
        rotated = pygame.transform.rotate(image, degrees)
        rect = rotated.get_rect(center=(sprite.position.x, sprite.position.y))
        self.screen.blit(rotated, rect)

    def _draw_explosion(self, explosion) -> None:
        """Вырезать текущий кадр из горизонтального спрайт-листа."""
        index = explosion.frame_index()
        clip = pygame.Rect(index * EXPLOSION_TILE, 0, EXPLOSION_TILE, EXPLOSION_TILE)
        frame = self.images.explosion_sheet.subsurface(clip)
        rect = frame.get_rect(
            center=(explosion.position.x, explosion.position.y)
        )
        self.screen.blit(frame, rect)
