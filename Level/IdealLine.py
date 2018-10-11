# -*- coding: UTF-8 -*-


class Tile(object):

    def __init__(self, type, coordinates):
        self.type = type
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.shortest_way_to_goal = None
        self.start_connections = list()
        self.end_connections = list()

    def find_way(self, tiles):
        pass
