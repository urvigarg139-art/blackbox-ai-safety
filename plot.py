import matplotlib.pyplot as plt

episodes = []
scores = []

with open("logs/training_log.txt") as f:
    for line in f:
        parts = line.strip().split(",")
        ep = int(parts[0].split()[1])
        sc = int(parts[1].split()[1])
        episodes.append(ep)
        scores.append(sc)

plt.plot(episodes, scores)
plt.xlabel("Episodes")
plt.ylabel("Score")
plt.title("AI Learning Curve")
plt.show()

