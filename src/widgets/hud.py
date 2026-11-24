"""Индикаторы жизней и очков в верхней части экрана."""

from __future__ import annotations

import pygame

from src.config import COLOR_HUD, COLOR_HUD_SHADOW, WIDTH


class HUD:
    """Текстовые счётчики Lives / Score, видимые и на заставке."""

    def __init__(self) -> None:
        """Подготовить шрифт HUD."""
        self.font = pygame.font.SysFont("arial", 28, bold=True)

    def draw(self, surface: pygame.Surface, lives: int, score: int) -> None:
        """Нарисовать жизни слева и очки справа."""
        self._blit_text(surface, f"Lives: {lives}", (40, 24))
        score_text = f"Score: {score}"
        text_width, _ = self.font.size(score_text)
        self._blit_text(surface, score_text, (WIDTH - 40 - text_width, 24))

    def _blit_text(
        self,
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
    ) -> None:
        """Текст с тенью, чтобы он читался на ярком фоне."""
        shadow = self.font.render(text, True, COLOR_HUD_SHADOW)
        label = self.font.render(text, True, COLOR_HUD)
        surface.blit(shadow, (position[0] + 2, position[1] + 2))
        surface.blit(label, position)
