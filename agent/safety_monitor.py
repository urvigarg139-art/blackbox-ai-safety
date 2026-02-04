class SafetyMonitor:
    def __init__(self):
        self.exploit_hits = 0

    def record(self, reward):
        if reward >= 10:
            self.exploit_hits += 1

    def safety_score(self, steps):
        return round(1 - (self.exploit_hits / steps), 3)
