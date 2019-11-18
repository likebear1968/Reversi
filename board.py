import numpy as np

class Board:
    BLANK = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, size):
        self.size = size
        self.board = []
        self.mask = [True, True, True, True, False, True, True, True, True]
        self.reset()

    def reset(self):
        center = np.array([[Board.BLACK, Board.WHITE],[Board.WHITE, Board.BLACK]])
        pad = (self.size - 2) // 2
        self.board = np.pad(center, [(pad, pad), (pad, pad)], 'constant')

    def count(self, color, board=None):
        if board is None: board = self.board
        return np.count_nonzero(board == color)

    def get_state(self, board=None):
        if board is None: board = self.board
        return ''.join(map(str, board.flatten()))

    def get_vector(self, y, x, direction):
        if direction == 0:  #左上
            return [(i, j) for j, i in zip(reversed(range(x)), reversed(range(y)))]
        elif direction == 1: #上
            return [(i, x) for i in reversed(range(self.size)) if i < y]
        elif direction == 2: #右上
            return [(i, j) for j, i in zip(np.arange(x + 1, x + y + 1), reversed(range(y))) if i < self.size and j < self.size]
        elif direction == 3: #左
            return [(y, i) for i in reversed(range(self.size)) if i < x]
        elif direction == 4: #右
            return [(y, i) for i in range(self.size) if i > x]
        elif direction == 5: #左下
            return [(i, j) for j, i in zip(reversed(range(x)), range(y + 1, self.size))]
        elif direction == 6: #下
            return [(i, x) for i in range(self.size) if i > y]
        elif direction == 7: #右下
            return [(i, j) for j, i in zip(range(x, self.size), range(y, self.size)) if j != x and i != y]
        return []

    def check_vector(self, color, vector, board=None):
        if board is None: board = self.board
        grids = []
        flg = False
        for i, grid in enumerate(vector):
            if board[grid] == Board.BLANK:
                return []
            elif board[grid] == color:
                flg = True
                break
            grids.append(grid)
        if flg == False:
            return []
        return grids

    def check_arround(self, pboard, y, x):
        return pboard[y: y + 3, x: x + 3][np.array(self.mask).reshape(3, -1)]

    def availables(self, color, board=None):
        if board is None: board = self.board
        blank = np.where(board == Board.BLANK)
        pboard = np.pad(board, [(1, 1), (1, 1)], 'constant')
        #accept = []
        accept = {}
        for y, x in zip(blank[0], blank[1]):
            for i, v in enumerate(self.check_arround(pboard, y, x)):
                if v not in [Board.BLANK, color]:
                    grids = self.check_vector(color, self.get_vector(y, x, i), board)
                    if len(grids) > 0:
                        #grids.insert(0, (y, x))
                        #accept.append(grids)
                        if (y, x) in accept.keys():
                            accept[(y, x)].extend(grids)
                        else:
                            accept[(y, x)] = grids
        return accept

    def flip(self, color, grids, board=None):
        if board is None: board = self.board
        for grid in grids:
            board[grid] = color
        return self.count(color, board)
