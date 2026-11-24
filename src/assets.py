"""Загрузка изображений с диска."""

from __future__ import annotations

from pathlib import Path

import pygame

from src.config import (
    HEIGHT,
    IMAGE_ASTEROID,
    IMAGE_DEBRIS,
    IMAGE_EXPLOSION,
    IMAGE_MISSILE,
    IMAGE_NEBULA,
    IMAGE_SHIP,
    IMAGE_SPLASH,
    WIDTH,
)


def load_image(path: Path, convert_alpha: bool = True) -> pygame.Surface:
    """Загрузить PNG. ``convert_alpha`` сохраняет прозрачность."""
    if not path.exists():
        raise FileNotFoundError(f"Не найден ресурс: {path}")
    image = pygame.image.load(str(path))
    if convert_alpha:
        return image.convert_alpha()
    return image.convert()


class Images:
    """Набор всех спрайтов, загружается один раз при старте приложения."""

    def __init__(self) -> None:
        """Прочитать фон, корабль, астероид, ракету, взрыв и заставку."""
        nebula = load_image(IMAGE_NEBULA, convert_alpha=False)
        debris = load_image(IMAGE_DEBRIS)
        self.nebula = pygame.transform.smoothscale(nebula, (WIDTH, HEIGHT))
        self.debris = pygame.transform.smoothscale(debris, (WIDTH, HEIGHT))
        self.asteroid = load_image(IMAGE_ASTEROID)
        self.ship_sheet = load_image(IMAGE_SHIP)
        self.missile = load_image(IMAGE_MISSILE)
        self.explosion_sheet = load_image(IMAGE_EXPLOSION)
        self.splash = load_image(IMAGE_SPLASH)
        # double_ship.png: слева обычный корабль, справа — с огнём двигателя.
        sheet_w, sheet_h = self.ship_sheet.get_size()
        half = sheet_h // 2
        self.ship_idle = self.ship_sheet.subsurface((0, 0, sheet_w, half)).copy()
        self.ship_thrust = self.ship_sheet.subsurface(
            (0, half, sheet_w, half)
        ).copy()
