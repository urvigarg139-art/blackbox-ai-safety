import random

class QAgent:
    def __init__(self):
        self.q = {}
        self.lr = 0.2
        self.gamma = 0.9
        self.epsilon = 0.7

    def get_q(self, s, a):
        return self.q.get((s,a),0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0,3)
        return max(range(4), key=lambda a:self.get_q(state,a))

    def learn(self, s,a,r,ns):
        best = max([self.get_q(ns,i) for i in range(4)])
        self.q[(s,a)] = self.get_q(s,a) + self.lr*(r+self.gamma*best-self.get_q(s,a))


