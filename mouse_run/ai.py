#-*- coding:utf-8 -*-
import random
import json
from collections import Counter
from environment import Action
from multiprocessing import Pool


def load_data(line):
    return json.loads(line.strip())


class AI:
    def __init__(self, epsilon=0.2, alpha=0.1, gamma=0.9):
        self.q = Counter()
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.action = Action()
        self.pool = Pool(5)

    def dump(self, file_name):
        with open(file_name, "w") as f:
            for k, v in self.q.iteritems():
                f.write(json.dumps({"key": k, "value": v}) + "\n")

    def load(self, file_name):
        with open(file_name) as f:
            lines = f.readlines()
        for i, data in enumerate(self.pool.imap(load_data, lines)):
            if i % 100000 == 0:
                print "load:", round(float(i) / len(lines) * 100, 2), "%,", "lines:", i
            self.q[(tuple(data["key"][0]), data["key"][1])] = data["value"]

    def learn_q(self, last_state, action, reward, now_state):
        max_state_value = max([self.q[(now_state, a)] for a in Action.get_actions()])
        # 全部使用reward初始化
        if (last_state, action) not in self.q:
            self.q[(last_state, action)] = reward
        self.q[(last_state, action)] += self.alpha * (
            reward + self.gamma * max_state_value - self.q[(last_state, action)])

    def choose_action(self, state):
        action2q = {a: self.q[(state, a)] for a in Action.get_actions()}
        if random.random() < self.epsilon:
            return random.choice(action2q.keys())
        max_q = max(action2q.values())
        best_actions = [a for a in action2q if action2q[a] == max_q]
        return random.choice(best_actions)

