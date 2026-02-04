def log_episode(ep, score):
    with open("logs/training_log.txt", "a") as f:
        f.write(f"Episode {ep}, Score {score}\n")
