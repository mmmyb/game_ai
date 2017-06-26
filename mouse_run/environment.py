#-*- encoding: utf-8 -*-
import random


class Cell:
    def __init__(self, data, x, y):
        self.wall = (data == "X")
        self.color = 'black' if self.wall else 'white'
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def is_wall(self):
        return self.wall

    def get_color(self):
        return self.color


class Action:

    action_delta_xy_mapping = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
        "up_right": (1, -1),
        "up_left": (-1, -1),
        "down_right": (1, 1),
        "down_left": (-1, 1)
    }

    @classmethod
    def get_actions(cls):
        return cls.action_delta_xy_mapping.keys()

    @staticmethod
    def get_sideling_actions():
        return ["up_right", "up_left", "down_right", "down_left"]

    @staticmethod
    def get_straight_actions():
        return ["up", "down", "left", "right"]


class Environment:
    def __init__(self, map_file_name):
        self.env, self.width, self.height = {}, None, 0
        with open(map_file_name) as f:
            for lines in f.readlines():
                lines = lines.strip()
                if self.width is None or len(lines) == self.width:
                    self.width = len(lines)
                    for i, data in enumerate(lines):
                        self.env[(i, self.height)] = Cell(data, i, self.height)
                    self.height += 1

    def get_cell(self, x, y, action=None):
        if action is None:
            return self.env[(x, y)]
        dx, dy = Action.action_delta_xy_mapping[action]
        rx, ry = x + dx, y + dy
        # 地图边界联通
        if rx < 0:
            rx += self.width
        elif rx >= self.width:
            rx -= self.width
        if ry < 0:
            ry += self.height
        elif ry >= self.height:
            ry -= self.height

        return self.env[(rx, ry)]

    def get_all_cells(self):
        return self.env.values()

    def get_random_cell(self):
        return self.get_cell(random.randrange(self.width), random.randrange(self.height))






