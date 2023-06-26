import pygame
import numpy as np


class GameInformation:
    def __init__(
        self,
        winner,
        invalid_moves,
        turn,
        total_turns,
        total_three_liners,
        total_two_liners,
        block_four_liners,
    ):
        self.winner = winner
        self.invalid_moves = invalid_moves
        self.turn = turn
        self.total_turns = total_turns
        self.total_three_liners = total_three_liners
        self.total_two_liners = total_two_liners
        self.block_four_liners = block_four_liners


class Game:
    ROWS = 6
    COLUMNS = 7
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
        self.invalid_moves = [0, 0]
        self.total_two_liners = [set(), set()]
        self.total_three_liners = [set(), set()]
        self.winner = [0, 0]
        self.block_four_liners = [0, 0]
        self.total_turns = 0
        self.board = self.create_board()

    def create_board(self):
        # Creating a 2D array with all elements 0
        board = np.zeros((self.ROWS, self.COLUMNS))
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
            for col in range(self.COLUMNS):
                for dr, dc in directions:
                    try:
                        if (
                            board[row][col]
                            == board[row + dr][col + dc]
                            == board[row + dr * 2][col + dc * 2]
                            == board[row + dr * 3][col + dc * 3]
                            == self.turn + 1
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
            for col in range(self.COLUMNS):
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
            opponent_three_liners = self.check_if_line(self.board, self.turn)
            self.drop_token(self.board, col, self.turn + 1)
            new_oppponent_three_liners = self.check_if_line(self.board, self.turn)

            if opponent_three_liners > new_oppponent_three_liners:
                self.block_four_liners[self.turn] += 1

            if self.check_if_winner(self.board):
                self.display_winner()

            # Switch to the other player
            self.turn += 1
            self.turn %= 2

    def player_ai_move(self, col):
        if 0 < col < 8 and self.check_if_valid(self.board, col):
            self.drop_token(self.board, col, self.turn + 1)

        if self.check_if_winner(self.board):
            self.display_winner()

        # Switch to the other player
        self.turn += 1
        self.turn %= 2

    def check_if_line(self, board, turn):
        # Check all possible directions for a two-liners and three-liners

        current_three_liners = 0
        directions = [
            (1, 0),
            (1, 1),
            (1, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
        ]

        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                for dr, dc in directions:
                    if row == 5 and col == 4 and dr == 0 and dc == -1:
                        print(
                            board[row + dr * 3][col + dc * 3],
                        )
                    try:
                        if (
                            row + dr * 3 < self.ROWS
                            and col + dc * 3 < self.COLUMNS
                            and board[row + dr * 3][col + dc * 3] == 0
                            or row - dr >= 0
                            and col - dc >= 0
                            and board[row - dr][col - dc] == 0
                        ) and board[row][col] == board[row + dr][col + dc] == board[
                            row + dr * 2
                        ][
                            col + dc * 2
                        ] == self.turn + 1:
                            self.total_three_liners[turn].add((row, col))

                        if (
                            row + dr * 3 < self.ROWS
                            and col + dc * 3 < self.COLUMNS
                            and board[row + dr * 3][col + dc * 3] == 0
                            or row - dr >= 0
                            and col - dc >= 0
                            and board[row - dr][col - dc] == 0
                        ) and board[row][col] == board[row + dr][col + dc] == board[
                            row + dr * 2
                        ][
                            col + dc * 2
                        ] == 2 - self.turn:
                            current_three_liners += 1
                    except IndexError:
                        pass

        return current_three_liners

    def ai_move(self, net, board):
        self.total_turns += 1

        flat_board = board.flatten()
        output = net.activate(flat_board)
        decision = output.index(max(output))

        if self.check_if_valid(board, decision):
            opponent_three_liners = self.check_if_line(self.board, self.turn)
            self.drop_token(self.board, decision, self.turn + 1)
            new_oppponent_three_liners = self.check_if_line(self.board, self.turn)

            if opponent_three_liners > new_oppponent_three_liners:
                self.block_four_liners[self.turn] += 1

            # self.check_if_line(self.board, self.turn)

            if self.check_if_winner(board):
                self.winner[self.turn] += 0.2
                self.winner[1 - self.turn] -= 0.5
                self.game_over = True
            elif self.is_board_full(board):
                self.game_over = True
            else:
                self.turn += 1
                self.turn %= 2
        else:
            self.invalid_moves[1 - self.turn] += 1

    def get_info(self):
        game_info = GameInformation(
            self.winner,
            self.invalid_moves,
            self.turn,
            self.total_turns,
            self.total_three_liners,
            self.total_two_liners,
            self.block_four_liners,
        )
        return game_info

    def new_game(self):
        # Reset the game for a new round
        self.game_over = False
        self.turn = 0
        self.invalid_moves = [0, 0]
        self.three_liners = [set(), set()]
        self.total_two_liners = [set(), set()]
        self.winner = [0, 0]
        self.total_turns = 0
        self.board = self.create_board()
