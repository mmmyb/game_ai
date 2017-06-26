# -*-coding:utf-8 -*-
import random
from environment import Action


class Agent(object):

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def set_position(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y


class Cat(Agent):

    def __init__(self, color, x, y):
        super(Cat, self).__init__(color, x, y)

    def update(self, target_cell, env):
        if target_cell.is_wall():
            return
        if target_cell.get_position() == self.get_position():
            return
        best_cell = env.get_cell(self.x, self.y)
        min_distance = (best_cell.x - target_cell.x) ** 2 + (best_cell.y - target_cell.y) ** 2
        if self.get_position() != target_cell.get_position():
            for direction in Action.action_delta_xy_mapping:
                next_cell = env.get_cell(self.x, self.y, direction)
                if next_cell.is_wall():
                    continue
                distance = (next_cell.x - target_cell.x) ** 2 + (next_cell.y - target_cell.y) ** 2
                if distance < min_distance:
                    min_distance = distance
                    best_cell = next_cell
        while best_cell.get_position() == self.get_position() or best_cell.is_wall():
            best_cell = env.get_cell(best_cell.x, best_cell.y, random.choice(Action.action_delta_xy_mapping.keys()))
        self.x, self.y = best_cell.get_position()


class Cheese(Agent):

    def __init__(self, color, x, y):
        super(Cheese, self).__init__(color, x, y)

    def update(self):
        pass


class Mouse(Agent):

    def __init__(self, color, x, y):
        super(Mouse, self).__init__(color, x, y)

    def update(self, action, env):
        cell = env.get_cell(self.x, self.y, action)
        if not cell.is_wall():
            self.set_position(cell.get_position())
