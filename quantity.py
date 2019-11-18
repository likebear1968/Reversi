import numpy as np
import itertools

class Quantity:
    def __init__(self, size, alpha=0.1, gamma=0.9, init=1.0):
        self.size, self.alpha, self.gamma, self.init = size, alpha, gamma, init
        self.Q = {}
        self.last_q = 0
        self.corners = [(a, b) for a, b in itertools.product([0, size - 1], repeat=2)]
        self.arround = {}
        for r, c in self.corners:
            self.arround[(r, c)] = [(a, b) for a, b in itertools.product(np.abs([r, r-1]), np.abs([c, c-1])) if (a, b) != (r, c)]

    def reset(self):
        self.last_q = 0

    def init_row(self):
        return np.random.rand(self.size * self.size) * 0.1
        #center = np.zeros((2, 2))
        #pad = (self.size - 2) // 2
        #q = np.pad(center, [(pad, pad), (pad, pad)], 'constant', constant_values=self.init)
        #return q.flatten()

    def to_idx(self, pos):
        y, x = pos[0], pos[1]
        return y * self.size + x

    def to_pos(self, idx):
        return divmod(idx, self.size)

    def latest_q(self, state, action):
        if state not in self.Q:
            self.Q[state] = self.init_row()
        return self.Q[state][self.to_idx(action)]

    def get_q(self, state, action, reward=0, next_Q=None):
        q = self.latest_q(state, action)
        alpha = self.alpha
        if action in self.corners: alpha += 1
        for k, v in self.arround.items():
            if state[self.to_idx(k)] == '0' and action in v: alpha *= 0.1
        if next_Q is None:
            return alpha * (reward + self.gamma * q - self.last_q)
        return alpha * (reward + self.gamma * next_Q - q)

    def update_q(self, state, action, q):
        self.last_q = q
        self.Q[state][self.to_idx(action)] += q
