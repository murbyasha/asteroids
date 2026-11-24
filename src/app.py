"""Окно pygame и главный цикл: ввод, обновление модели, отрисовка."""

from __future__ import annotations

import pygame

from src.assets import Images
from src.config import FPS, SHIP_ANGLE_VEL, WIDTH, HEIGHT, WINDOW_TITLE
from src.models.game_model import GameModel
from src.renderers.renderer import Renderer


class App:
    """Приложение: создаёт окно, крутит цикл, раздаёт события модели."""

    def __init__(self) -> None:
        """Инициализировать pygame, загрузить ресурсы и создать модель."""
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.images = Images()
        self.model = GameModel()
        self.renderer = Renderer(self.screen, self.images)
        self._running = True

    def run(self) -> None:
        """Запустить главный цикл, пока окно не закроют."""
        while self._running:
            dt_ms = self.clock.tick(FPS)
            self._handle_events()
            self._poll_hold_keys()
            self.model.update(dt_ms)
            self.renderer.draw(self.model)
            pygame.display.flip()
        pygame.quit()

    def _handle_events(self) -> None:
        """Клавиатура и мышь. Клик вне заставки на стартовом экране игнорируется."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.model.shoot()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.model.started and self.renderer.splash.contains(
                    event.pos
                ):
                    self.model.start()

    def _poll_hold_keys(self) -> None:
        """Поворот и тяга читаются из зажатых клавиш каждый кадр."""
        if not self.model.started:
            self.model.ship.set_angle_vel(0.0)
            self.model.ship.set_thrust(False)
            return
        pressed = pygame.key.get_pressed()
        angle_vel = 0.0
        if pressed[pygame.K_LEFT]:
            angle_vel -= SHIP_ANGLE_VEL
        if pressed[pygame.K_RIGHT]:
            angle_vel += SHIP_ANGLE_VEL
        self.model.ship.set_angle_vel(angle_vel)
        self.model.ship.set_thrust(bool(pressed[pygame.K_UP]))
