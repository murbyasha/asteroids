"""Заставка RiceRocks: игра стартует только по клику в её прямоугольник."""

from __future__ import annotations

from typing import Tuple

import pygame

from src.config import HEIGHT, WIDTH


class Splash:
    """Центральная заставка и проверка клика по её области."""

    def __init__(self, image: pygame.Surface) -> None:
        """Сохранить изображение и вычислить прямоугольник по центру экрана."""
        self.image = image
        self.rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def contains(self, point: Tuple[int, int]) -> bool:
        """True, если ``point`` попал в прямоугольник заставки."""
        return self.rect.collidepoint(point)

    def draw(self, surface: pygame.Surface) -> None:
        """Нарисовать заставку по центру."""
        surface.blit(self.image, self.rect)
