from random import choice, randrange

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (245, 245, 245)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (220, 20, 60)
SNAKE_COLOR = (34, 139, 34)
STONE_COLOR = (105, 105, 105)

SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов, содержит общие атрибуты."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self) -> None:
        """Абстрактный метод, предназначенный для переопределения."""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        return self.position

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(Apple):
    """Класс описывающий камень и действия с ним."""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR


class Snake(GameObject):
    """
    Класс описывающий змейку и её поведение, движение, отрисовку,
    а также обрабатывает действия пользователя.
    """

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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

        if new_head_width > SCREEN_WIDTH:
            new_head_width = 0
        elif new_head_width < 0:
            new_head_width = SCREEN_WIDTH

        if new_head_height > SCREEN_HEIGHT:
            new_head_height = 0
        elif new_head_height < 0:
            new_head_height = SCREEN_HEIGHT

        new_head_position = (new_head_width, new_head_height)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, DOWN, LEFT, UP])


def handle_keys(game_object) -> None:
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Заупскает основной игровой цикл."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    apple = Apple()
    snake = Snake()
    stone = Stone()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        apple.draw()
        snake.draw()

        pygame.display.update()

        snake.update_direction()
        snake.move()

        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position()
            apple.draw()

        if apple.position == stone.position:
            apple.randomize_position()
            apple.draw()

        for position in snake.positions[1:]:
            if snake.positions[0] == position:
                snake.reset()

        if snake.length > 3:
            stone.draw()
        if stone.position == snake.positions[0]:
            snake.reset()
            stone.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
