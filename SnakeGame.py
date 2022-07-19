from email import header
import random
from time import time_ns
from Cell import Cell


class SnakeGame:
    high_score = 1

    def __init__(self, difficulty: str, grid_size: str):
        """
        Parameters
        ----------
        difficulty : str
            'easy' | 'medium' | 'hard'
        grid_size : str
            'small' | 'medium' | 'large'.
        """
        self.difficulty = difficulty
        if grid_size == 'small':
            self.grid_size = 21
        if grid_size == 'medium':
            self.grid_size = 31
        if grid_size == 'large':
            self.grid_size == 41

        # place the food at a random x and y within the grid
        self.food = Cell(x=random.randint(0, self.grid_size - 1), y=random.randint(0, self.grid_size - 1))

        # 'N' | 'S' | 'E' | 'W'
        self.direction = 'N'

        # internally, snake will be represented as a list of cells, acting like a queue
        # To move, we will append the next cell and pop the existing.
        # To grow, we will append and not pop the end cell.
        # last element in list is head, first is tail
        self.snake = [Cell(x=self.grid_size // 2, y=self.grid_size // 2, is_head=True)]
        if (self.difficulty == 'easy'):
            self.step_duration_ms = 500
        if (self.difficulty == 'medium'):
            self.step_duration_ms = 300
        if (self.difficulty == 'hard'):
            self.step_duration_ms = 200

        self.score = 1
        self.previous_iteration_time = self.get_millis()
        self.direction_change = None
        self.paused = False
        self.game_over = False

    def run_game(self):
        """
        Method to run the game. Checks the current time repeatedly,
        and will process a game loop if the current time has passed
        the previous run's time + interval.
        """
        while True:
            if not self.paused and not self.game_over and SnakeGame.get_millis() >= self.previous_iteration_time + self.step_duration_ms:
                self.process_events()
                self.step_game()
                self.previous_iteration_time = SnakeGame.get_millis()

    def step_game(self):
        """
        Handles one game step.
        1. Moves snake one cell
        2. Checks for any food
        3. Checks for death
        """
        head = self.snake[len(self.snake) - 1]

        # if Snake head is at food
        if head.x == self.food.x and head.y == self.food.y:
            self.food = Cell(x=random.randint(0, self.grid_size - 1), y=random.randint(0, self.grid_size - 1))
            self.score = self.score + 1
            if self.score > SnakeGame.high_score:
                SnakeGame.high_score = self.score

        # if Snake head is at Snake
        for cell in self.snake:
            if cell.is_head is False and cell.x == head.x and cell.y == head.y:
                self.game_over = True
                break

        # Move the snake by appending a new cell in the direction the snake is moving and popping the tail element
        if self.direction == 'N' and head.y != 0:
            self.snake.append(Cell(x=head.x, y=head.y - 1, is_head=True))
            self.snake.pop(0)
        if self.direction == 'S' and head.y != self.grid_size - 1:
            self.snake.append(Cell(x=head.x, y=head.y + 1, is_head=True))
            self.snake.pop(0)
        if self.direction == 'E' and head.x != self.grid_size - 1:
            self.snake.append(Cell(x=head.x + 1, y=head.y, is_head=True))
            self.snake.pop(0)
        if self.direction == 'W' and head.x != 0:
            self.snake.append(Cell(x=head.x - 1, y=head.y, is_head=True))
            self.snake.pop(0)

    # assume that all incoming directions will match 'N' | 'S' | 'E' | 'W'
    def process_events(self):
        """
        Processes any events that were passed into the game for changing direction
        """
        if self.direction_change is not None:
            self.direction = self.direction_change
            self.direction_change = None

    def restart(self):
        """
        Restarts the game.
        """
        self.food = Cell(x=random.randint(0, self.grid_size - 1), y=random.randint(0, self.grid_size - 1))
        self.direction = 'N'
        self.snake = [Cell(x=self.grid_size // 2, y=self.grid_size // 2)]
        self.score = 1
        self.game_over = False

    def resume(self):
        """
        Resumes the game.
        """
        self.paused = False

    def pause(self):
        """
        Pauses the game.
        """
        self.paused = True

    # assume this size is odd
    def set_size(self, size):
        """
        Update the grid size.
        """
        self.grid_size = size

    # assume difficulty matches # 'easy' | 'medium' | 'hard'
    def adjust_difficulty(self, difficulty):
        """
        Adjust the difficulty of the game.
        """
        self.difficulty = difficulty

    @classmethod
    def get_high_score(cls):
        """
        Return the SnakeGame high score.
        """
        return cls.high_score

    def get_score(self):
        """
        Get the current score.
        """
        return self.score

    def get_game_state(self):
        """
        Construct the matrix that represents the game state.
        E = Empty, F = Food, S = Snake
        """
        grid = [['E' for i in range(self.grid_size)] for i in range(self.grid_size)]
        grid[self.food.y][self.food.x] = 'F'
        for link in self.snake:
            grid[link.y][link.x] = 'S'
        return grid

    def print_game_state(self):
        """
        Turn the game state into a human readable string
        """
        for row in self.get_game_state():
            print('  '.join(row))

    @staticmethod
    def get_millis():
        """
        Static method to get the current epoch millis time
        """
        return time_ns() // 1000000

