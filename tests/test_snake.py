import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import pygame  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for test environment
    pygame = types.ModuleType("pygame")

    class Rect:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def colliderect(self, other):
            return not (
                self.x + self.width <= other.x
                or other.x + other.width <= self.x
                or self.y + self.height <= other.y
                or other.y + other.height <= self.y
            )

    def init():
        return None

    def quit():
        return None

    pygame.Rect = Rect
    pygame.init = init
    pygame.quit = quit
    pygame.display = types.SimpleNamespace(set_mode=lambda size: size)
    pygame.draw = types.SimpleNamespace(rect=lambda *args, **kwargs: None)

    sys.modules["pygame"] = pygame

try:
    import neat  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for test environment
    neat = types.ModuleType("neat")

    class DefaultGenome:
        def __init__(self, key):
            self.key = key

        def configure_new(self, config):
            return None

        def configure_crossover(self, genome1, genome2, config):
            return None

        def mutate(self, config):
            return None

        def distance(self, other, config):
            return 0

    class _DummyNetwork:
        def activate(self, inputs):
            return (0.0, 0.0)

    neat.DefaultGenome = DefaultGenome
    neat.nn = types.SimpleNamespace(
        FeedForwardNetwork=types.SimpleNamespace(create=lambda genome, config: _DummyNetwork())
    )

    sys.modules["neat"] = neat

import pytest

from src.Config import Config
from src.Snake import Snake


@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()


class DummyObstacle:
    def __init__(self, x_pos, y_pos=0):
        self._x_pos = x_pos
        self._y_pos = y_pos

    def get_width_coord(self):
        return self._x_pos

    def get_height_coord(self):
        return self._y_pos


def test_snake_move_stops_at_left_boundary():
    snake = Snake(1)
    snake.x_pos = 50

    snake.move(-Config['snake']['speed'])

    assert snake.get_width_coord() == 50


def test_snake_move_stops_at_right_boundary():
    snake = Snake(2)
    snake.x_pos = 450

    snake.move(Config['snake']['speed'])

    assert snake.get_width_coord() == 450


def test_snake_move_changes_position_within_bounds():
    snake = Snake(3)
    snake.x_pos = 250

    snake.move(Config['snake']['speed'])

    assert snake.get_width_coord() == 270


def test_snake_obstacle_direction_values():
    snake = Snake(4)
    snake.x_pos = 300

    obstacle_left = DummyObstacle(200)
    obstacle_right = DummyObstacle(400)
    obstacle_center = DummyObstacle(300)

    assert snake.get_obstacle_direction(obstacle_left) == 1
    assert snake.get_obstacle_direction(obstacle_right) == 0
    assert snake.get_obstacle_direction(obstacle_center) == 0.5


def test_snake_width_change_calculation():
    snake = Snake(5)
    snake.x_pos = 300
    obstacle = DummyObstacle(500)

    assert snake.get_width_change(obstacle) == pytest.approx(1.0)
