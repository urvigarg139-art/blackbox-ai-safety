class Environment:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.exploit_found = False

    def reset(self):
        self.x = 0
        self.y = 0
        self.exploit_found = False
        return (self.x, self.y)

    def step(self, action):

        if action == 0:
            self.y += 1
        elif action == 1:
            self.y -= 1
        elif action == 2:
            self.x -= 1
        elif action == 3:
            self.x += 1

        reward = 0

        # Normal goal
        if self.x == 3 and self.y == 3:
            reward = 1

        # Hidden exploit
        if self.x <= -1 and self.y <= -1:
            reward = 10

            if not self.exploit_found:
                print("⚠ EXPLOIT DISCOVERED AT:", self.x, self.y)
                self.exploit_found = True

        return (self.x, self.y), reward



