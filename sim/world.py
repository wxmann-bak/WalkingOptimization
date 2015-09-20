from enum import Enum
import random

__author__ = 'tangz'


class TrafficLight(Enum):
    GREEN = 0,
    RED = 1


def switchlight(light):
    return TrafficLight.GREEN if light is TrafficLight.RED else TrafficLight.RED

def randomlight():
    return random.choice([TrafficLight.RED, TrafficLight.GREEN])


class Intersection(object):
    def __init__(self, st1, st2):
        if st1 == st2:
            raise ValueError("Cannot have an intersection with two identical streets!")
        self.st1 = st1
        self.st2 = st2
        cross_st2 = randomlight()
        self._lights = {st1: switchlight(cross_st2), st2: cross_st2}

    # def swaplight(self):
    #     self._lights = {st: switchlight(light) for st, light in self._lights.items()}

    def green(self, st):
        return self.lightat(st) == TrafficLight.GREEN

    def lightat(self, st):
        return self._lights[st]

    def __eq__(self, other):
        if not isinstance(other, Intersection):
            return False
        elif self is other:
            return True
        else:
            # most common case: we want to be order invariant.
            # in other words: Intersection(A, B) == Intersection(B, A)
            sts = (self.st1, self.st2)
            return other.st1 in sts and other.st2 in sts and other.st1 != other.st2


class GridIntersectionPool(object):
    def __init__(self, sts_northsouth, sts_eastwest):
        self.intersections = {(st_NS, st_EW): Intersection(st_NS, st_EW) for st_NS in sts_northsouth
                              for st_EW in sts_eastwest}

    def getat(self, st1, st2):
        possible = self.intersections.get((st1, st2))
        if not possible:
            possible = self.intersections.get((st2, st1))
            if not possible:
                raise ValueError("Cannot find intersection for: {}, {}".format(st1, st2))
        return possible


class WalkMode(Enum):
    NORTH = 0,
    EAST = 1


class RouteTracker(object):
    def __init__(self, width, height):
        self.sts_NS = ['North-South Rd. {}'.format(i+1) for i in range(width)]
        self.sts_EW = ['East-West Rd. {}'.format(i+1) for i in range(height)]
        self.intersectionpool = GridIntersectionPool(self.sts_NS, self.sts_EW)
        self._n = 0
        self._e = 0
        self._n_max = height
        self._e_max = width
        self._cross_n = False
        self._cross_e = False
        self._walkmode = random.choice([WalkMode.NORTH, WalkMode.EAST])

    def intersection(self):
        return self.intersectionpool.getat(self._get_EW_st(), self._get_NS_st())

    def going_north(self):
        return self._walkmode == WalkMode.NORTH

    def going_east(self):
        return self._walkmode == WalkMode.EAST

    def turn(self):
        self._walkmode = WalkMode.EAST if self.going_north() else WalkMode.NORTH

    def must_cross(self):
        return self._cross_n if self.going_north() else self._cross_e

    def green_light(self):
        intersectn = self.intersection()
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
        return self._e < self._e_max

    def has_next_north(self):
        return self._n < self._n_max

    def next_block(self):
        return self._next_north() if self.going_north() else self._next_east()

    def _next_east(self):
        if not self.has_next_east():
            raise StopIteration("End of Grid. Cannot go further east")
        self._e += 1
        self._cross_e = True
        return self._get_EW_st()

    def _next_north(self):
        if not self.has_next_north():
            raise StopIteration("End of Grid. Cannot go further north")
        self._n += 1
        self._cross_n = True
        return self._get_NS_st()

    def _get_NS_st(self):
        return self.sts_NS[self._e]

    def _get_EW_st(self):
        return self.sts_EW[self._n]
