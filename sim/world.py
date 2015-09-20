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


class StreetGrid(object):
    @staticmethod
    def with_dimensions(width, height):
        sts_NS = ['North-South Rd. {}'.format(i+1) for i in range(width)]
        sts_EW = ['East-West Rd. {}'.format(i+1) for i in range(height)]
        return StreetGrid(sts_NS, sts_EW)

    def __init__(self, sts_NS, sts_EW):
        self.sts_NS = sts_NS
        self.sts_EW = sts_EW
        self.intersectionpool = GridIntersectionPool(self.sts_NS, self.sts_EW)

    def width(self):
        return len(self.sts_NS)

    def height(self):
        return len(self.sts_EW)

    def get_NS_st(self, n):
        if n > self.width():
            raise ValueError("Requested street {} greater than number of streets {}".format(n, self.width))
        return self.sts_NS[n-1]

    def get_EW_st(self, n):
        if n > self.height():
            raise ValueError("Requested street {} greater than number of streets {}".format(n, self.height))
        return self.sts_EW[n-1]

    def get_intersection(self, n, e):
        return self.intersectionpool.getat(self.get_EW_st(n), self.get_NS_st(e))
