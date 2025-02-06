import pygame
import sys
import numpy as np
import copy

pygame.init
pygame.display.set_caption('Tictac')
screen = pygame.display.set_mode((320, 320))
screen.fill((88, 180, 106))


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        return move

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move


class Board:
    def __init__(self):
        self.squares = np.zeros((3, 3))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = (222, 216, 180) if self.squares[0][col] == 2 else (66, 66, 66)
                    iPos = (col * 320 // 3 + (320 // 3) // 2, 20)
                    fPos = (col * 320 // 3 + (320 // 3) // 2, 300)
                    pygame.draw.line(screen, color, iPos, fPos, 15)
                return self.squares[0][col]
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = (222, 216, 180) if self.squares[row][0] == 2 else (66, 66, 66)
                    iPos = (20, row * 320 // 3 + (320 // 3) // 2)
                    fPos = (300, row * 320 // 3 + (320 // 3) // 2)
                    pygame.draw.line(screen, color, iPos, fPos, 15)
                return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = (222, 216, 180) if self.squares[1][1] == 2 else (66, 66, 66)
                iPos = (20, 20)
                fPos = (300, 300)
                pygame.draw.line(screen, color, iPos, fPos, 15)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = (222, 216, 180) if self.squares[1][1] == 2 else (66, 66, 66)
                iPos = (20, 300)
                fPos = (300, 20)
                pygame.draw.line(screen, color, iPos, fPos, 15)
            return self.squares[1][1]
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(3):
            for col in range(3):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isEmpty(self):
        return self.marked_sqrs == 0


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.game_over = False
        self.show_lines()

    def make_move(self, row, col):
        if not self.game_over:
            self.board.mark_sqr(row, col, self.player)
            self.draw_fig(row, col)
            self.next_turn()
            if self.isover():
                self.game_over = True

    def show_lines(self):
        pygame.draw.line(screen, (40, 140, 150), (320 // 3, 0), (320 // 3, 320), 15)
        pygame.draw.line(screen, (40, 140, 150), (320 - 320 // 3, 0), (320 - 320 // 3, 320), 15)
        pygame.draw.line(screen, (40, 140, 150), (0, 320 // 3), (320, 320 // 3), 15)
        pygame.draw.line(screen, (40, 140, 150), (0, 320 - 320 // 3), (320, 320 - 320 // 3), 15)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * 320 // 3 + 80, row * 320 // 3 + 80)
            end_desc = (col * 320 // 3 + 320 // 3 - 80, row * 320 // 3 + 320 // 3 - 80)
            pygame.draw.line(screen, (239, 231, 200), start_desc, end_desc, 20)

            start_asc = (col * 320 // 3 + 80, row * 320 // 3 + 320 // 3 - 80)
            end_asc = (col * 320 // 3 + 320 // 3 - 80, row * 320 // 3 + 80)
            pygame.draw.line(screen, (239, 231, 200), start_asc, end_asc, 20)
        elif self.player == 2:
            center = (col * 320 // 3 + (320 // 3) // 2, row * 320 // 3 + (320 // 3) // 2)
            pygame.draw.circle(screen, (239, 231, 200), center, (320 // 3) // 4, 15)


def main():
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over:
                    pos = event.pos
                    row = pos[1] // (320 // 3)
                    col = pos[0] // (320 // 3)
                    if board.empty_sqr(row, col):
                        game.make_move(row, col)
                        if game.isover():
                            game.running = False
                            game.game_over = True

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isover():
                game.running = False

        pygame.display.update()


main()
