from random import randint, choice

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
CYAN_COLOR = (93, 216, 228)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Словарь клавиш управления
TURNS = {
    (pygame.K_UP, DOWN): UP,
    (pygame.K_DOWN, UP): DOWN,
    (pygame.K_LEFT, RIGHT): LEFT,
    (pygame.K_RIGHT, LEFT): RIGHT,
}


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, body_color=WHITE_COLOR, position=SCREEN_CENTER):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, CYAN_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализирует яблоко с заданным цветом и случайно позицией."""
        super().__init__(body_color=RED_COLOR,
                         position=self.randomize_position())

    @staticmethod
    def randomize_position():
        """Задает случайное положение яблоку."""
        while True:
            _position = (
                randint(0, GRID_WIDTH - 2) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 2) * GRID_SIZE
            )
            if not _position == SCREEN_CENTER:
                break
        return _position

    def move_to_new_position(self, snake_positions):
        """Отправляет яблоко в новую позицию, которая не внутри змейки."""
        while True:
            _position = self.randomize_position()
            if _position not in snake_positions:
                self.position = _position
                break


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=GREEN_COLOR):
        """Инициализирует змейку."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в заданном направлении."""
        self.update_direction()
        snake_head_x, snake_head_y = self.get_head_position()
        direction_x, direction_y = self.direction  # Направление движения.
        # Новое положение головы.
        new_head_position = ((snake_head_x + direction_x * GRID_SIZE)
                             % SCREEN_WIDTH,
                             (snake_head_y + direction_y * GRID_SIZE)
                             % SCREEN_HEIGHT)

        if len(self.positions) > self.length:  # Если змейка не ест яблоко.
            self.positions.pop()  # Удаление хвоста.
        # Добавление новой головы в начало змейки.
        self.positions.insert(0, new_head_position)

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for self.position in self.positions[:-1]:
            super().draw(surface)

    def get_head_position(self):
        """Возвращает текущее положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки в начальное положение."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        # Случайное направление движения при сбросе игры
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция отвечающая за нажатие клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            for key in TURNS:
                if event.key == key[0] and game_object.direction != key[1]:
                    game_object.next_direction = TURNS[key]
            return game_object.next_direction


def main():
    """
    Основная функция игры "Змейка".
    Игра начинается с создания змейки и яблока на поле.
    Змейка движется в заданном направлении и ест яблоки,
    которые встречаются на ее пути.
    Каждый раз, когда змейка ест яблоко, её длина увеличивается.
    При столкновении змейки с самой собой игра перезапускается.
    Для выхода из игры пользователь может нажать на крестик окна игры.
    """
    snake = Snake()
    apple = Apple()
    game_status = True
    while game_status:
        clock.tick(SPEED)
        handle_keys(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.move_to_new_position(snake.positions)
            snake.length += 1

        # Столкновение змейки с собой и завершение игры.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.move_to_new_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
