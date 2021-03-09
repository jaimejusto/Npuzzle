# Author: Jaime Justo
# Date: 3/2/21

import random


class PuzzleBoard:
    def __init__(self, tiles_given=None):
        self.rows = 3
        self.cols = 3
        self.empty_space_row = None
        self.empty_space_col = None
        self.board = self.new_board(tiles_given)

    def new_board(self, tile_order=None):
        # player's board
        board = [[0] * self.cols for i in range(self.rows)]

        # assign randomized tiles to board if none provided
        if tile_order is None:
            tile_order = random.sample(range(9), 9)
            # ensure the randomized order is not already solved
            while tile_order == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
                tile_order = random.sample(range(9), 9)

        # current tile
        tile = 0
        # initialize board with tiles
        for row in range(self.rows):
            for col in range(self.cols):
                # store empty space tile position
                if tile_order[tile] == 0:
                    self.empty_space_row = row
                    self.empty_space_col = col
                board[row][col] = tile_order[tile]
                tile += 1

        return board

    def update_board(self, tile_row, tile_col):
        tile_number = self.board[tile_row][tile_col]

        # swap tile and empty space on the board
        self.board[self.empty_space_row][self.empty_space_col] = tile_number
        self.board[tile_row][tile_col] = 0

        # update empty space position
        self.empty_space_row = tile_row
        self.empty_space_col = tile_col

    def check_board(self, solution_board):
        # iterates all the player's tiles to see if they match the solution
        rows = self.rows
        cols = self.cols

        for row in range(rows):
            for col in range(cols):
                if solution_board[row][col] != self.board[row][col]:
                    return False
        return True


class PuzzleGame:
    def __init__(self):
        self.game_board = PuzzleBoard()
        self.solved_board = PuzzleBoard([1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.game_state = 'Not Solved'

    def get_game_board(self):
        return self.game_board.board

    def new_game(self):
        self.game_board = PuzzleBoard()
        self.game_state = 'Not Solved'

    def get_move(self, tile):
        row_tile, col_tile = [int(x) for x in tile]

        return row_tile, col_tile

    def verify_move(self, tile_row, tile_col):
        if tile_row < 0 or tile_row > 2:
            return False
        if tile_col < 0 or tile_col > 2:
            return False

        # tiles around empty space
        empty_down_row = self.game_board.empty_space_row + 1
        empty_center_row = self.game_board.empty_space_row
        empty_up_row = self.game_board.empty_space_row - 1
        empty_center_col = self.game_board.empty_space_col
        empty_left_col = self.game_board.empty_space_col - 1
        empty_right_col = self.game_board.empty_space_col + 1

        # check if tile selected is next to the empty space
        if (tile_row == empty_up_row and tile_col == empty_center_col) or \
            (tile_row == empty_center_row and tile_col == empty_right_col) or \
            (tile_row == empty_down_row and tile_col == empty_center_col) or \
                (tile_row == empty_center_row and tile_col == empty_left_col):
            return True

        return False

    def make_move(self, tile_row, tile_col):
        # swap numbered tile and empty tile positions
        self.game_board.update_board(tile_row, tile_col)

    def verify_certificate(self, certificate=None):
        # checks board during gameplay
        if certificate is None:
            # player's board is the certificate
            certificate = self.solved_board
            result = self.game_board.check_board(certificate.board)
            return result

        # checks board with tile order provided
        else:
            # given tile order is the certificate
            certificate = PuzzleBoard(certificate)
            result = self.solved_board.check_board(certificate.board)

            if result is False:
                return "Not Solved, Try Again!"
            else:
                return "Solved!"


if __name__ == '__main__':
    cert = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    g = PuzzleGame()
    g.verify_certificate(cert)
