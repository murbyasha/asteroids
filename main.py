"""Точка входа в игру «Астероиды».

Запуск из корня проекта::

    python main.py
"""

from src.app import App


def main() -> None:
    """Создать приложение и запустить игровой цикл."""
    App().run()


if __name__ == "__main__":
    main()
