import numpy as np
from board import Board

class Player():
    def __init__(self, color, epsilon=0.5):
        self.color, self.epsilon = color, epsilon
        self.count = 2
        self.opponent = Board.BLACK if color == Board.WHITE else Board.WHITE
        self.train = True

    def put(self, board, quantity):
        grids = board.availables(self.color)
        if len(grids) == 0: return 0
        keys = []
        stones = []
        q = []
        state = board.get_state()
        for k, v in grids.items():
            keys.append(k)
            stones.append(v)
            v.insert(0, k)
            q.append(quantity.get_q(state, k, len(v), self.next_Q(board, quantity, v)))
        idx = None
        if np.random.rand() < self.epsilon:
            p = q - np.max(q)
            p = np.exp(p)
            p /= np.sum(p)
            idx = np.random.choice(len(q), p=p)
        else:
            idx = np.argmax(q)
        self.count += board.flip(self.color, stones[idx])
        if self.train:
            quantity.update_q(state, keys[idx], q[idx])
        return self.count

    def next_Q(self, board, quantity, stones):
        tmp = board.board.copy()
        board.flip(self.color, stones, tmp)
        state = board.get_state(tmp)
        actions = []
        for k in board.availables(self.opponent, tmp).keys():
            actions.append(quantity.latest_q(state, k))
        if len(actions) == 0: return 1
        return np.max(actions)
