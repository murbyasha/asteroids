"""Глобальные параметры игры.

Все числовые константы собраны здесь, чтобы их было удобно
подбирать без правки игровой логики.
"""

from pathlib import Path

# --- Окно и цикл ---
# Размер игрового поля в пикселях (классический RiceRocks).
WIDTH = 800
HEIGHT = 600
# Частота кадров. От неё зависят «покадровые» скорости ниже.
FPS = 60
WINDOW_TITLE = "Asteroids"

# --- Старт партии ---
START_LIVES = 3  # начальное количество жизней
START_SCORE = 0  # начальное количество очков

# --- Корабль ---
# Радиус кругового хитбокса корабля (меньше спрайта, чтобы столкновения
# выглядели честно).
SHIP_RADIUS = 35
# Угловая скорость поворота при удержании стрелок, радианы за кадр.
SHIP_ANGLE_VEL = 0.09
# Ускорение при включённом двигателе, пиксели / кадр².
SHIP_THRUST = 0.15
# Коэффициент сопротивления среды: каждый кадр скорость умножается
# на (1 - FRICTION), поэтому корабль плавно останавливается.
FRICTION = 0.02
# Смещение носа относительно центра спрайта — отсюда вылетают ракеты.
SHIP_NOSE_OFFSET = 40

# --- Ракеты ---
# Скорость ракеты относительно корабля в момент выстрела.
MISSILE_SPEED = 8.0
MISSILE_RADIUS = 4
# Время жизни в кадрах: ракета не должна успеть пересечь поле
# даже по короткой стороне (HEIGHT) и «выйти» с другой стороны.
# lifetime = min_side / speed, с небольшим запасом 0.9.
MISSILE_LIFETIME = int(0.9 * min(WIDTH, HEIGHT) / MISSILE_SPEED)

# --- Астероиды ---
ASTEROID_RADIUS = 40
# Интервал попытки спавна, миллисекунды.
ASTEROID_SPAWN_INTERVAL_MS = 1000
MAX_ASTEROIDS = 12
# Случайная линейная скорость при появлении.
ASTEROID_MIN_VEL = 0.5
ASTEROID_MAX_VEL = 2.2
# Случайная угловая скорость (вращение камня вокруг центра).
ASTEROID_MAX_ANG_VEL = 0.08
# Не спавнить астероид слишком близко к кораблю.
ASTEROID_SAFE_DISTANCE = 150

# --- Фон ---
# Полупрозрачный «мусорный» слой движется влево с постоянной скоростью.
DEBRIS_SPEED = 1.2
DEBRIS_ALPHA = 140  # 0..255, полупрозрачность динамического фона

# --- Взрыв ---
# Лист explosion.png: 24 кадра по горизонтали, каждый 128×128.
EXPLOSION_FRAMES = 24
EXPLOSION_TILE = 128
EXPLOSION_FRAME_DURATION = 2  # сколько игровых кадров держать один тайл

# --- Пути к ресурсам ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "images"
IMAGE_NEBULA = ASSETS_DIR / "nebula.png"
IMAGE_DEBRIS = ASSETS_DIR / "debris.png"
IMAGE_ASTEROID = ASSETS_DIR / "asteroid.png"
IMAGE_SHIP = ASSETS_DIR / "ship.png"
IMAGE_MISSILE = ASSETS_DIR / "missile.png"
IMAGE_EXPLOSION = ASSETS_DIR / "explosion.png"
IMAGE_SPLASH = ASSETS_DIR / "splash.png"

# Цвета HUD (R, G, B).
COLOR_HUD = (255, 255, 255)
COLOR_HUD_SHADOW = (0, 0, 0)
