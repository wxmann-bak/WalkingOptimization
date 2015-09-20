import random
import unittest
from sim.world import Intersection, TrafficLight, GridIntersectionPool, StreetGrid

__author__ = 'tangz'


class IntersectionTests(unittest.TestCase):
    def setUp(self):
        self.st1 = 'A'
        self.st2 = 'B'
        self.intersection = Intersection(self.st1, self.st2)

    def test_should_go_if_green(self):
        light1 = self.intersection.lightat(self.st1)

        if light1 == TrafficLight.GREEN:
            self.assertTrue(self.intersection.green(self.st1))
            self.assertFalse(self.intersection.green(self.st2))
        else:
            self.assertTrue(self.intersection.green(self.st2))
            self.assertFalse(self.intersection.green(self.st1))

    def test_should_be_equal(self):
        test_intersection = Intersection(self.st1, self.st2)
        test_intersection_swap = Intersection(self.st2, self.st1)
        self.assertEqual(test_intersection, self.intersection)
        self.assertEqual(test_intersection_swap, test_intersection)


class IntersectionPoolTests(unittest.TestCase):
    def setUp(self):
        self.sts_EW = ('A', 'B', 'C', 'D')
        self.sts_NS = ('1', '2', '3')
        self.intersectionpool = GridIntersectionPool(self.sts_NS, self.sts_EW)

    def _random_intersection(self):
        st1 = random.choice(self.sts_NS)
        st2 = random.choice(self.sts_EW)
        return Intersection(st1, st2)

# TODO: add test for getting intersection that does not existZ
    def test_get_one_intersection(self):
        intersection_returned = self.intersectionpool.getat('B', '2')
        intersection_expected = Intersection('B', '2')
        self.assertEqual(intersection_expected, intersection_returned)


class StreetGridTests(unittest.TestCase):
    def setUp(self):
        self.sts_EW_1 = ['A', 'B', 'C']
        self.sts_NS_1 = ['1', '2', '3', '4']
        self.grid_from_sts = StreetGrid(self.sts_NS_1, self.sts_EW_1)

        self.height = 5
        self.width = 3
        self.grid_from_static = StreetGrid.with_dimensions(self.width, self.height)

    def test_should_get_height_width(self):
        self.assertEqual(self.grid_from_sts.height(), 3)
        self.assertEqual(self.grid_from_sts.width(), 4)

        self.assertEqual(self.grid_from_static.height(), self.height)
        self.assertEqual(self.grid_from_static.width(), self.width)

    def test_should_get_intersection(self):
        intersection = self.grid_from_sts.get_intersection(2, 1)
        self.assertEquals(intersection, Intersection('B','1'))

# TODO: add negative cases for get
    def test_should_get_street(self):
        st1 = self.grid_from_sts.get_EW_st(2)
        st2 = self.grid_from_sts.get_NS_st(3)
        self.assertEqual(st1, 'B')
        self.assertEqual(st2, '3')

