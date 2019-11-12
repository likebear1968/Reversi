import numpy as np

class Player():
    def __init__(self, color, epsilon=0.5):
        self.color, self.epsilon = color, epsilon
        self.count = 2

    def put(self, board, quantity, train=False):
        grids = board.availables(self.color)
        if len(grids) == 0: return 0
        keys = []
        stones = []
        q = []
        state = board.get_state()
        for k, v in grids.items():
            keys.append(k)
            q.append(quantity.get_q(state, k, len(v)))
            #q.append(quantity.get_q(state, k))
            v.insert(0, k)
            stones.append(v)
        idx = None
        if np.random.rand() < self.epsilon:
            p = q - np.max(q)
            p = np.exp(p)
            p /= np.sum(p)
            idx = np.random.choice(len(q), p=p)
        else:
            idx = np.argmax(q)
        self.count += board.flip(self.color, stones[idx])
        if train:
            quantity.update_q(state, keys[idx], q[idx])
        return self.count
