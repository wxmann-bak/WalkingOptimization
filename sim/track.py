from enum import Enum
import random

__author__ = 'tangz'


class WalkMode(Enum):
    NORTH = 0,
    EAST = 1


class RouteTracker(object):
    def __init__(self, grid):
        self._grid = grid
        self._n = 1
        self._e = 1
        self._cross_n = False
        self._cross_e = False
        self._walkmode = random.choice([WalkMode.NORTH, WalkMode.EAST])

    def going_north(self):
        return self._walkmode == WalkMode.NORTH

    def going_east(self):
        return self._walkmode == WalkMode.EAST

    def turn(self):
        self._walkmode = WalkMode.EAST if self.going_north() else WalkMode.NORTH

    def must_cross(self):
        return self._cross_n if self.going_north() else self._cross_e

    def green_light(self):
        intersectn = self._grid.get_intersection(self._n, self._e)
        if self.going_north():
            return intersectn.green(self._get_EW_st())
        else:
            return intersectn.green(self._get_NS_st())

    def cross(self):
        if self.going_north():
            self._cross_n = False
        else:
            self._cross_e = False

    def has_next_east(self):
        return self._e <= self._grid.width()

    def has_next_north(self):
        return self._n <= self._grid.height()

    def next_block(self):
        return self._next_north() if self.going_north() else self._next_east()

    def _next_east(self):
        if not self.has_next_east():
            raise StopIteration("End of Grid. Cannot go further east")
        st = self._get_EW_st()
        self._e += 1
        self._cross_e = True
        return st

    def _next_north(self):
        if not self.has_next_north():
            raise StopIteration("End of Grid. Cannot go further north")
        st = self._get_NS_st()
        self._n += 1
        self._cross_n = True
        return st

    def _get_NS_st(self):
        return self._grid.get_NS_st(self._e)

    def _get_EW_st(self):
        return self._grid.get_EW_st(self._n)


class TimeKeeper(object):

    def __init__(self, cross_street, cross_block, intersection_wait):
        self._time = 0
        self._cross_street = cross_street
        self._cross_block = cross_block
        self._intersection_wait = intersection_wait

    def track_wait(self):
        self._time += self._intersection_wait

    def track_cross(self):
        self._time += self._cross_street

    def track_walk_block(self):
        self._time += self._cross_block

    def output_time(self):
        return self._time
