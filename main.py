from env.simple_env import Environment
from agent.q_agent import QAgent
from agent.safety_monitor import SafetyMonitor

env = Environment()
agent = QAgent()
monitor = SafetyMonitor()

for ep in range(30):
    s = env.reset()
    total = 0

    for i in range(300):
        a = agent.choose_action(s)
        ns,r = env.step(a)
        agent.learn(s,a,r,ns)
        monitor.record(r)
        s = ns
        total += r

    score = monitor.safety_score(300)

    print(f"Episode {ep} | Reward {total} | Safety Score {score}")




