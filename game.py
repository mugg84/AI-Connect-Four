import pygame
import time
import numpy as np


class GameInformation:
    def __init__(self, winner, invalid_moves, total_turns):
        self.winner = winner
        self.invalid_moves = invalid_moves
        self.total_turns = total_turns


class Game:
    ROWS = 6
    COLUMS = 7
    SQUARE = BORDER = 100
    RADIUS = int(SQUARE / 2 - 10)
    BLACK = 0, 0, 0
    BLUE = 0, 0, 255
    RED = 255, 0, 0
    YELLOW = 255, 215, 0

    def __init__(
        self,
        screen,
    ):
        self.screen = screen
        self.game_over = False
        self.turn = 0
        self.invalid_moves = 0
        self.total_turns = 0
        self.board = self.create_board()

    def create_board(self):
        # Creating a 2D array with all elements 0
        board = np.zeros((self.ROWS, self.COLUMS))
        return board

    def check_if_valid(self, board, col):
        # Check if the selected column is not filled up, i.e., the topmost cell is still 0
        return board[0][col - 1] == 0

    def drop_token(self, board, col, player_number):
        # Drop the token of the current player into the selected column
        for row in range(self.ROWS - 1, -1, -1):
            if board[row][col - 1] == 0:
                board[row][col - 1] = player_number
                break

    def check_if_winner(self, board):
        # Check all possible directions for a win (4 in a row)
        directions = [(1, -1), (1, 0), (1, 1), (0, 1)]

        for row in range(self.ROWS):
            for col in range(self.COLUMS):
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

    def is_board_full(self, board):
        return np.count_nonzero(board) == board.size

    def draw(self):
        # Draw the game board and the pieces
        for row in range(self.ROWS):
            for col in range(self.COLUMS):
                # Draw the squares of the game board
                pygame.draw.rect(
                    self.screen,
                    self.BLUE,
                    (
                        self.BORDER + col * self.SQUARE,
                        self.BORDER + row * self.SQUARE,
                        self.SQUARE,
                        self.SQUARE,
                    ),
                )
                # Draw the pieces
                color = (
                    self.BLACK
                    if self.board[row][col] == 0
                    else self.RED
                    if self.board[row][col] == 1
                    else self.YELLOW
                )
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        int(self.BORDER + col * self.SQUARE + self.SQUARE / 2),
                        int(row * self.SQUARE + self.SQUARE + self.SQUARE / 2),
                    ),
                    self.RADIUS,
                )
                pygame.display.update()

    def draw_player_move(self, event):
        # Draw the potential move of the current player
        col_x = event.pos[0]
        if self.SQUARE + self.RADIUS < col_x < self.SQUARE * 8 - self.RADIUS:
            pygame.draw.rect(
                self.screen, self.BLACK, (0, 0, self.screen.get_width(), self.SQUARE)
            )
            color = self.RED if self.turn == 0 else self.YELLOW
            pygame.draw.circle(
                self.screen, color, (col_x, self.BORDER / 2), self.RADIUS
            )
            pygame.display.update()

    def display_winner(self):
        # If the current player wins, display the message and end the game
        font = pygame.font.Font(None, 100)
        text = font.render(f"PLAYER {self.turn + 1} WINS", 1, (255, 255, 255))
        self.screen.blit(
            text,
            (
                self.screen.get_width() / 2 - text.get_rect().width / 2,
                self.SQUARE / 2 - text.get_rect().height / 2,
            ),
        )
        self.game_over = True

    def player_move(self, event):
        # Execute the move of the current player
        pygame.draw.rect(
            self.screen, self.BLACK, (0, 0, self.screen.get_width(), self.SQUARE)
        )
        col = event.pos[0] // 100
        if 0 < col < 8 and self.check_if_valid(self.board, col):
            self.drop_token(self.board, col, self.turn + 1)

        if self.check_if_winner(self.board):
            self.display_winner()

        # Switch to the other player
        self.turn += 1
        self.turn %= 2

    def ai_move(self, net, genome, board):
        flat_board = board.flatten()
        output = net.activate(flat_board)
        decision = output.index(max(output))
        self.total_turns += 1
        if self.check_if_valid(board, decision):
            self.drop_token(self.board, decision, self.turn + 1)

        else:
            self.invalid_moves += 1
            genome.fitness -= 0.5

        game_info = GameInformation(False, self.invalid_moves, self.total_turns)
        if self.is_board_full(board):
            self.game_over = True
        elif self.check_if_winner(board):
            genome.fitness += 1
            game_info.winner = True
            self.game_over = True

        elif self.check_if_valid(board, decision):
            # Switch to the other player
            self.turn += 1
            self.turn %= 2

        return game_info

    def new_game(self):
        # Reset the game for a new round
        self.board = self.create_board()
        self.turn = 0
        self.game_over = False
