# AP CSP Creative Task
# Code related to the pygame GUI was inspired by 'https://github.com/KeithGalli/Connect4-Python'.
# This project is a full game of Connect 4 against an AI agent.
# You click on the GUI to make your move and the agent will make its move.

# Imports
import pygame
import sys
import math

# Board Consts
ROWS = 6
COLS = 7

# GUI Consts
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

WINDOW_WIDTH = COLS * SQUARE_SIZE
WINDOW_HEIGHT = (ROWS + 1) * SQUARE_SIZE
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Engine Consts
INF = math.inf
NEG_INF = -math.inf

PLAYER_1 = 1
PLAYER_2 = -1

EVAL_TABLE = [[3, 4, 5, 7, 5, 4, 3],
              [4, 6, 8, 10, 8, 6, 4],
              [5, 8, 11, 13, 11, 8, 5],
              [5, 8, 11, 13, 11, 8, 5],
              [4, 6, 8, 10, 8, 6, 4],
              [3, 4, 5, 7, 5, 4, 3]]


# Class that represents a board and its associated functions.
class Board:
    def __init__(self, data):
        self.data = data

    # Returns a completely empty board.
    @staticmethod
    def empty():
        data = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]

        return Board(data)

    # Displays the board into the terminal
    def print(self):
        for y in range(ROWS):
            print(f"  {self.data[y][0]}   {self.data[y][1]}   {self.data[y][2]}   {self.data[y][3]}   {self.data[y][4]}   {self.data[y][5]}")
        print()

    # Drops a piece onto the board at a specific column
    def drop_piece(self, x, player):
        best_row = 0
        if self.data[0][x] == 0:
            for y in range(ROWS):
                if self.data[y][x] == 0:
                    best_row = y
                else:
                    break

            self.data[best_row][x] = player

    # Removes the most recently dropped piece in a column
    def undrop_piece(self, x):
        for y in range(ROWS):
            if self.data[y][x] != 0:
                self.data[y][x] = 0
                break


# Returns a list of all the open columns on a board
def open_cols(board):
    open_cols = []

    for x in range(COLS):
        if board.data[0][x] == 0:
            open_cols.append(x)

    return open_cols


# Checks if a player has won or if there is a tie on a board
def gameover(board):
    for player in [1, -1]:
        # Check horizontal lines
        for x in range(COLS):
            for y in range(ROWS - 3):
                if board.data[y][x] == player and board.data[y + 1][x] == player and board.data[y + 2][x] == player and board.data[y + 3][x] == player:
                    return player

        # Check vertical lines
        for y in range(ROWS):
            for x in range(COLS - 3):
                if board.data[y][x] == player and board.data[y][x + 1] == player and board.data[y][x + 2] == player and board.data[y][x + 3] == player:
                    return player

        # Check / diagonal lines
        for y in range(ROWS - 3):
            for x in range(3, COLS):
                if board.data[y][x] == player and board.data[y + 1][x - 1] == player and board.data[y + 2][x - 2] == player and board.data[y + 3][x - 3] == player:
                    return player

        # Check \ diagonal lines
        for y in range(ROWS - 3):
            for x in range(COLS - 3):
                if board.data[y][x] == player and board.data[y + 1][x + 1] == player and board.data[y + 2][x + 2] == player and board.data[y + 3][x + 3] == player:
                    return player

    open_spaces = 0
    for x in range(COLS):
        for y in range(ROWS):
            if board.data[y][x] == 0:
                open_spaces += 1

    if open_spaces == 0:
        return 0
    else:
        return None


# Heuristic evaluation of the board
def evaluate(board):
    p1_score = 0
    p2_score = 0
    for y in range(ROWS):
        for x in range(COLS):
            if board.data[y][x] == PLAYER_1:
                p1_score += EVAL_TABLE[y][x]

            elif board.data[y][x] == PLAYER_2:
                p2_score += EVAL_TABLE[y][x]

    return p1_score - p2_score


# Class that stores the data about a search and has all searching functions
class Engine:
    def __init__(self):
        self.search_data = []

    # Resets all engine data
    def reset(self):
        self.search_data.clear()

    # Searches a board to a specific depth
    def search(self, board, alpha, beta, depth, player, root):
        if depth == 0 or gameover(board) is not None:
            if gameover(board) == player:
                return INF
            elif gameover(board) == -player:
                return NEG_INF

            return player * evaluate(board)

        moves = open_cols(board)

        best_score = NEG_INF
        for mv in moves:
            board.drop_piece(mv, player)

            score = -self.search(board, -beta, -alpha, depth - 1, -player, False)

            board.undrop_piece(mv)

            if root:
                self.search_data.append((mv, score))

            if score > best_score:
                best_score = score

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                break

        if root:
            self.search_data.sort(key=lambda x: x[1], reverse=True)

        return alpha


# Draws the board onto the pygame window
def draw_board(board):
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, GRAY, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for r in range(ROWS):
        for c in range(COLS):
            flipped_r = ROWS - r - 1

            if board.data[r][c] == PLAYER_1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), WINDOW_HEIGHT - int(flipped_r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            elif board.data[r][c] == PLAYER_2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), WINDOW_HEIGHT - int(flipped_r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()


# Init Globals
board = Board.empty()
searcher = Engine()
turn = PLAYER_1

# Init Pygame
pygame.init()
pygame.display.set_caption("CONNECT 4 MINIMAX")
pygame_font = pygame.font.Font(pygame.font.get_default_font(), 36)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Draw the starting frame
screen.fill(GRAY)
draw_board(board)

# Main game loop
while gameover(board) is None:
    for event in pygame.event.get():
        # Check for pygame quit event
        if event.type == pygame.QUIT:
            sys.exit()

        # Check for pygame mouse movement event
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == PLAYER_1:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

        # Update pygame window
        pygame.display.update()

        # Check for pygame mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, SQUARE_SIZE))

            # Player 1 turn
            if turn == PLAYER_1:
                mouse_x = event.pos[0]

                best_col = None
                closest_distance = 100000
                for x in range(COLS):
                    if board.data[0][x] == 0:
                        real_x = (x * SQUARE_SIZE) + RADIUS

                        dist = math.dist((mouse_x, 0), (real_x, 0))
                        if dist < closest_distance:
                            closest_distance = dist
                            best_col = x

                if best_col is not None:
                    board.drop_piece(best_col, PLAYER_1)

                    draw_board(board)

                    turn *= -1

    # Player 2 turn
    if turn == PLAYER_2 and gameover(board) is None:
        searcher.reset()
        searcher.search(board, NEG_INF, INF, 7, PLAYER_2, True)
        best_move = searcher.search_data[0]

        board.drop_piece(best_move[0], PLAYER_2)

        draw_board(board)

        turn *= -1

    # If the game is over then wait 5 seconds before quiting
    winner = gameover(board)
    if winner is not None:
        if winner == PLAYER_1:
            winner_text = "YOU WON :)"
        elif winner == PLAYER_2:
            winner_text = "YOU LOST :("
        else:
            winner_text = "ITS A TIE :|"
        rendered = pygame_font.render(winner_text, True, BLACK)
        screen.blit(rendered, ((WINDOW_WIDTH / 2) - (rendered.get_width() / 2), 25))
        pygame.display.update()

        pygame.time.wait(5000)
