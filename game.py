import pygame
import numpy as np


class Game:
    def __init__(
        self, screen, rows, columns, square, border, radius, black, blue, red, yellow
    ):
        self.screen = screen
        self.game_over = False
        self.turn = 0
        self.rows = rows
        self.columns = columns
        self.square = square
        self.border = border
        self.radius = radius
        self.black = black
        self.blue = blue
        self.red = red
        self.yellow = yellow
        self.board = self.create_board()

    def create_board(self):
        # Creating a 2D array with all elements 0
        board = np.zeros((self.rows, self.columns))
        return board

    def check_if_valid(self, board, col):
        # Check if the selected column is not filled up, i.e., the topmost cell is still 0
        return board[0][col - 1] == 0

    def drop_token(self, board, col, player_number):
        # Drop the token of the current player into the selected column
        for row in range(self.rows - 1, -1, -1):
            if board[row][col - 1] == 0:
                board[row][col - 1] = player_number
                break

    def check_if_winner(self, board):
        # Check all possible directions for a win (4 in a row)
        directions = [(1, -1), (1, 0), (1, 1), (0, 1)]

        for row in range(self.rows):
            for col in range(self.columns):
                for dr, dc in directions:
                    try:
                        if (
                            board[row][col]
                            == board[row + dr][col + dc]
                            == board[row + dr * 2][col + dc * 2]
                            == board[row + dr * 3][col + dc * 3]
                            != 0
                        ):
                            return True
                    except IndexError:
                        pass
        return False

    def draw(self):
        # Draw the game board and the pieces
        for row in range(self.rows):
            for col in range(self.columns):
                # Draw the squares of the game board
                pygame.draw.rect(
                    self.screen,
                    self.blue,
                    (
                        self.border + col * self.square,
                        self.border + row * self.square,
                        self.square,
                        self.square,
                    ),
                )
                # Draw the pieces
                color = (
                    self.black
                    if self.board[row][col] == 0
                    else self.red
                    if self.board[row][col] == 1
                    else self.yellow
                )
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        int(self.border + col * self.square + self.square / 2),
                        int(row * self.square + self.square + self.square / 2),
                    ),
                    self.radius,
                )
                pygame.display.update()

    def draw_player_move(self, event):
        # Draw the potential move of the current player
        col_x = event.pos[0]
        if self.square + self.radius < col_x < self.square * 8 - self.radius:
            pygame.draw.rect(
                self.screen, self.black, (0, 0, self.screen.get_width(), self.square)
            )
            color = self.red if self.turn == 0 else self.yellow
            pygame.draw.circle(
                self.screen, color, (col_x, self.border / 2), self.radius
            )
            pygame.display.update()

    def player_move(self, event):
        # Execute the move of the current player
        pygame.draw.rect(
            self.screen, self.black, (0, 0, self.screen.get_width(), self.square)
        )
        col = event.pos[0] // 100
        if 0 < col < 8 and self.check_if_valid(self.board, col):
            self.drop_token(self.board, col, self.turn + 1)

        if self.check_if_winner(self.board):
            # If the current player wins, display the message and end the game
            font = pygame.font.Font(None, 100)
            text = font.render(f"PLAYER {self.turn + 1} WINS", 1, (255, 255, 255))
            self.screen.blit(
                text,
                (
                    self.screen.get_width() / 2 - text.get_rect().width / 2,
                    self.square / 2 - text.get_rect().height / 2,
                ),
            )
            self.game_over = True

        # Switch to the other player
        self.turn += 1
        self.turn %= 2

    def new_game(self):
        # Reset the game for a new round
        self.board = self.create_board()
        self.turn = 0
        self.game_over = False
