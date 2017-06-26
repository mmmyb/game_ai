#-*- coding:utf-8 -*-
from environment import Environment
from agent import Cat, Mouse, Cheese, Action
from ai import AI


class Game:
    def __init__(self, map_file_name):
        self.env = Environment(map_file_name)
        self.cat = Cat("orange", 0, 0)
        self.mouse = Mouse("gray", 0, 0)
        self.cheese = Cheese("yellow", 0, 0)
        self.init_agents_position()
        self.action = Action()
        self.feed = 0
        self.eaten = 0
        self.age = 0
        self.ai = AI()

    def pick_random_location(self, agent, other_agents):
        while True:
            cell = self.env.get_random_cell()
            for other_agent in other_agents:
                if other_agent.get_position() == cell.get_position():
                    break
            else:
                if not cell.is_wall():
                    agent.set_position(cell.get_position())
                    return

    def init_agents_position(self):
        agents = [self.cat, self.mouse, self.cheese]
        for cur_a in agents:
            self.pick_random_location(cur_a, [a for a in agents if a != cur_a])

    def get_state(self):
        """
        在现有规则下的所有可能状态
        1.墙里不能有其他东西
        2.cat,cheese,mouse可以在同一个格
        """
        around_cells = []
        for action in Action.get_straight_actions():
            cell1 = self.env.get_cell(self.mouse.x, self.mouse.y, action=action)
            cell2 = self.env.get_cell(cell1.x, cell1.y, action=action)
            around_cells.extend([cell1, cell2])

        for action in Action.get_sideling_actions():
            around_cells.append(self.env.get_cell(
                self.mouse.x, self.mouse.y, action=action))

        state = []
        cat_position = self.cat.get_position()
        cheese_position = self.cheese.get_position()
        mouse_position = self.mouse.get_position()
        for cell in around_cells:
            cell_position = cell.get_position()
            if cell.is_wall():
                state.append(1)
            elif cell_position == cat_position == cheese_position:
                state.append(2)
            elif cell_position == cat_position:
                state.append(3)
            elif cell_position == cheese_position:
                state.append(4)
            else:
                state.append(5)

        if mouse_position == cat_position == cheese_position:
            state.append(6)
        elif mouse_position == cat_position:
            state.append(7)
        elif mouse_position == cheese_position:
            state.append(8)
        else:
            state.append(9)

        return tuple(state)

    def get_full_state(self):
        """
        在现有规则下的所有可能状态
        1.墙里不能有其他东西
        2.cat,cheese,mouse可以在同一个格
        """
        state = []
        cat_position = self.cat.get_position()
        cheese_position = self.cheese.get_position()
        mouse_position = self.mouse.get_position()
        for cell in self.env.get_all_cells():
            cell_position = cell.get_position()
            if cell.is_wall():
                state.append(1)
            elif cell_position == mouse_position == cat_position == cheese_position:
                state.append(2)
            elif cell_position == mouse_position == cat_position:
                state.append(3)
            elif cell_position == mouse_position == cheese_position:
                state.append(4)
            elif cell_position == cat_position == cheese_position:
                state.append(5)
            elif cell_position == mouse_position:
                state.append(6)
            elif cell_position == cat_position:
                state.append(7)
            elif cell_position == cheese_position:
                state.append(8)
            else:
                state.append(9)

        return tuple(state)

    def get_reward(self):
        """
        这里假设猫在同一格里总是先发现和吃掉老鼠
        对于老鼠来说奔跑是需要体力的
        """
        if self.mouse.get_position() == self.cat.get_position():
            self.eaten += 1
            return -100
        elif self.mouse.get_position() == self.cheese.get_position():
            self.feed += 1
            return 50
        else:
            return -1

    def update(self):
        cur_state = self.get_full_state()
        reward = self.get_reward()
        self.ai.epsilon = self.age ** -0.2 if self.age > 0 else 0.5
        action = self.ai.choose_action(cur_state)
        self.cat.update(self.env.get_cell(self.mouse.x, self.mouse.y), self.env)
        if self.mouse.get_position() == self.cat.get_position():
            self.pick_random_location(self.mouse, [self.cat, self.cheese])
        elif self.mouse.get_position() == self.cheese.get_position():
            self.pick_random_location(self.cheese, [self.mouse, self.cat])
        else:
            self.mouse.update(action, self.env)
        next_state = self.get_full_state()
        self.ai.learn_q(cur_state, action, reward, next_state)
        self.age += 1
