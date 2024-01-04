from random import randint, choice

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, body_color=(255, 255, 255)):
        """Инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=(255, 0, 0)):
        """Инициализирует яблоко с заданным цветом и случайно позицией."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задает случайное положение яблоку."""
        self.position = (
            randint(0, GRID_WIDTH - 2) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 2) * GRID_SIZE
        )

    def move_to_new_position(self, snake_positions):
        """Отправляет яблоко в новую позицию, которая не внутри змейки."""
        while True:
            self.randomize_position()
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=(0, 255, 0)):
        """Инициализирует змейку."""
        super().__init__(body_color)
        self.last = None
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
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
        x, y = self.get_head_position()  # Голова змейки.
        dx, dy = self.direction  # Направление движения.
        # Новое положение головы.
        new_head_position = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                             (y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if len(self.positions) > self.length:  # Если змейка не ест яблоко.
            self.positions.pop()  # Удаление хвоста.
        # Добавление новой головы в начало змейки.
        self.positions.insert(0, new_head_position)

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки.
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущее положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки в начальное положение."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Случайное направление движения при сбросе игры
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и изменяет направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
