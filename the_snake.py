from random import choice, randrange
from sys import exit
from typing import Optional, Union

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

WHITE_COLOR = (245, 245, 245)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (220, 20, 60)
GREEN_COLOR = (34, 139, 34)
GRAY_COLOR = (105, 105, 105)
YELLOW_COLOR = (255, 255, 0)

BOARD_BACKGROUND_COLOR = WHITE_COLOR
BORDER_COLOR = BLACK_COLOR
APPLE_COLOR = RED_COLOR
SNAKE_COLOR = GREEN_COLOR
STONE_COLOR = GRAY_COLOR
WRONG_FOOD_COLOR = YELLOW_COLOR

SPEED = 15

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты: body_color: tuple, position: tuple.
    Методы:
    draw() - абстрактный метод,
    create_rectangle() - создание экземпляра Rect и отрисовка ячейки.
    """

    def __init__(self,
                 body_color: tuple = BOARD_BACKGROUND_COLOR,
                 position: Optional[tuple] = START_POSITION) -> None:
        self.body_color = body_color
        self.position = position

    def draw(self) -> None:
        """Абстрактный метод, предназначенный для переопределения."""
        raise NotImplementedError(
            f'Данная функция в классе: {self.__class__.__name__} '
            'еще не определена')

    def create_rectangle(self,
                         position: tuple,
                         body_color: tuple,
                         border_color: Optional[tuple] = None) -> None:
        """Создание экземпляра Rect и отрисовка ячейки."""
        rectangle = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rectangle)
        if border_color:
            pg.draw.rect(screen, border_color, rectangle, 1)


class Apple(GameObject):
    """
    Класс описывающий яблоко и действия с ним.

    Атрибуты: body_color: tuple, occuped_positions: list.
    Методы:
    randomize_position(occuped_positions: list) - определяет положение яблока,
    draw() - отрисовывает яблоко.
    """

    def __init__(self,
                 body_color: tuple = APPLE_COLOR,
                 occuped_positions: Union[list, None] = None) -> None:
        if occuped_positions is None:
            occuped_positions = []
        super().__init__(body_color)
        self.randomize_position(occuped_positions)

    def randomize_position(self, occuped_positions: list) -> None:
        """
        Устанавливает случайное положение яблока на игровом поле.

        Параметр occuped_positions принимает список занятых ячеек.
        """
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        if self.position in occuped_positions:
            self.randomize_position(occuped_positions)

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        self.create_rectangle(self.position, self.body_color, BORDER_COLOR)


class Stone(Apple):
    """
    Класс описывающий камень и действия с ним.

    Атрибуты: body_color: tuple, occuped_positions: list.
    Методы:
    randomize_position(occuped_positions: list) - определяет положение камня,
    draw() - отрисовывает камень.
    """

    def __init__(self,
                 body_color: tuple = STONE_COLOR,
                 occuped_positions: Union[list, None] = None) -> None:
        super().__init__(body_color, occuped_positions)


class WrongFood(Apple):
    """
    Класс описывающий неправильную еду и действия с ней.

    Атрибуты: body_color: tuple, occuped_positions: list.
    Методы:
    randomize_position(occuped_positions: list) - определяет положение еды,
    draw() - отрисовывает еду.
    """

    def __init__(self,
                 body_color: tuple = WRONG_FOOD_COLOR,
                 occuped_positions: Union[list, None] = None) -> None:
        super().__init__(body_color, occuped_positions)


class Snake(GameObject):
    """
    Класс описывающий змейку и действия с ней.

    Атрибуты: body_color: tuple, position: tuple.
    Методы:
    get_head_position() - определяет положение головы,
    move() - обновляет позицию всей змейки,
    draw() - отрисовывает змейку,
    reset() - сбрасывает змейку в изначальное состояние.
    """

    def __init__(self,
                 body_color: tuple = SNAKE_COLOR,
                 position: tuple = START_POSITION) -> None:
        super().__init__(body_color, position)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def update_direction(self, direction) -> None:
        """Обновляет направление движения змейки."""
        self.direction = direction

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """
        Обновляет позицию всей змейки, добавляя новую голову в начало
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        new_head_width = (
            self.direction[0] * GRID_SIZE + self.get_head_position()[0])
        new_head_height = (
            self.direction[1] * GRID_SIZE + self.get_head_position()[1])

        new_head_position = (new_head_width % SCREEN_WIDTH,
                             new_head_height % SCREEN_HEIGHT)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле."""
        self.create_rectangle(self.get_head_position(),
                              self.body_color,
                              BORDER_COLOR)

        if self.last:
            self.create_rectangle(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, DOWN, LEFT, UP])


def handle_keys(game_object) -> None:
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                exit()


def main():
    """Заупскает основной игровой цикл."""
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()
    apple = Apple(occuped_positions=snake.positions)
    stone = Stone(occuped_positions=([*snake.positions, apple.position]))
    wrong_food = WrongFood(
        occuped_positions=[*snake.positions, apple.position, stone.position])

    flags = {
        'wrong_food': True,
    }

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.draw()
        apple.draw()
        stone.draw()

        pg.display.update()

        snake.move()

        if snake.length > 3 and flags.get('wrong_food'):
            wrong_food.randomize_position(
                [*snake.positions, apple.position, stone.position])
            wrong_food.draw()
            flags['wrong_food'] = False

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position([*snake.positions, stone.position])
            apple.draw()
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif stone.position == snake.get_head_position():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            stone.randomize_position([*snake.positions, apple.position])
            stone.draw()
        elif wrong_food.position == snake.get_head_position():
            snake.length -= 1
            snake.create_rectangle(snake.positions.pop(),
                                   BOARD_BACKGROUND_COLOR)
            flags['wrong_food'] = True
            wrong_food.position = ()

        pg.display.update()


if __name__ == '__main__':
    main()
