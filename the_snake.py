from random import randint

import pygame
import sys
import time

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


def game_over_screen():
    """Отображение экрана окончания игры"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Если пользователь нажимает клавишу 'r', игра начинается заново
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    main()
            # Отображение надписи Game Over,
        # вы можете изменить шрифт, размер, цвет и т.д.
        font = pygame.font.SysFont(None, 90)
        text = font.render("Game Over", True, (123, 221, 43))
        screen.blit(text, (SCREEN_WIDTH // 4.2, SCREEN_HEIGHT // 4))
        pygame.display.flip()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, body_color=(255, 255, 255)):
        """Инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=(255, 0, 0)):
        """Инициализирует яблоко с заданным цветом и случайно позицией"""
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

    # Метод draw класса Apple
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
        self.length = 12
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в заданном направлении."""
        self.update_direction()
        x, y = self.get_head_position()  # голова змейки
        dx, dy = self.direction  # направление движения
        # новое положение головы
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if len(self.positions) > self.length:  # если змейка не ест яблоко
            self.positions.pop()  # удаление хвоста
        # добавление новой головы в начало змейки
        self.positions.insert(0, new_head)

    # # Метод draw класса Snake
    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
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
        self.direction = RIGHT
        self.next_direction = None


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

        # Проверяем состояние клавиш, нет ли нажатых
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != DOWN:
            snake.next_direction = UP
        elif keys[pygame.K_DOWN] and snake.direction != UP:
            snake.next_direction = DOWN
        elif keys[pygame.K_LEFT] and snake.direction != RIGHT:
            snake.next_direction = LEFT
        elif keys[pygame.K_RIGHT] and snake.direction != LEFT:
            snake.next_direction = RIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.move()
        snake.update_direction()
        # Столкновение змейки с собой и завершение игры
        if snake.get_head_position() in snake.positions[1:]:
            game_over_screen()
            time.sleep(5)
            snake.reset()
            apple.randomize_position()
        pygame.display.flip()

        if snake.get_head_position() == apple.position:
            apple.move_to_new_position(snake.positions)
            snake.length += 1
        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
