# -*- coding: UTF-8 -*-

from numpy.ma import sqrt


class Line(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = sqrt((self.start[0]-self.end[0])**2 + (self.start[1]-self.end[1])**2)
        self.path = 0
        try:
            self.m = (self.end[1]-self.start[1])/(self.end[0]-self.start[0])
        except ZeroDivisionError:
            self.m = None

    def __str__(self):
        return str(self.start)+' to '+str(self.end)+' with a length of '+str(self.length)+' and m = '+str(self.m)


class Corner(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = (self.x, self.y)
        self.reached_minimum = None
