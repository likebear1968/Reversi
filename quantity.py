import numpy as np

class Quantity:
    def __init__(self, size, alpha=0.1, gamma=0.9, init=1.0):
        self.size, self.alpha, self.gamma, self.init = size, alpha, gamma, init
        self.Q = {}
        self.last_q = 0

    def reset(self):
        self.last_q = 0

    def init_row(self):
        #return np.random.rand(self.size * self.size)
        center = np.zeros((2, 2))
        pad = (self.size - 2) // 2
        q = np.pad(center, [(pad, pad), (pad, pad)], 'constant', constant_values=self.init)
        return q.flatten()

    def to_idx(self, pos):
        y, x = pos[0], pos[1]
        return y * self.size + x

    def to_pos(self, idx):
        return divmod(idx, self.size)

    def latest_q(self, state, action):
        if state not in self.Q:
            self.Q[state] = self.init_row()
        return self.Q[state][self.to_idx(action)]

    def get_q(self, state, action, reward=0):
        q = self.latest_q(state, action)
        return self.alpha * (reward + self.gamma * q - self.last_q)
        #return self.alpha * self.gamma * (reward - q)

    def update_q(self, state, action, q):
        self.last_q = q
        self.Q[state][self.to_idx(action)] += q
