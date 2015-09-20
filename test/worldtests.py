import random
import unittest
from sim.world import Intersection, TrafficLight, GridIntersectionPool

__author__ = 'tangz'


class IntersectionTests(unittest.TestCase):
    def setUp(self):
        self.st1 = 'A'
        self.st2 = 'B'
        self.intersection = Intersection(self.st1, self.st2)

    # def test_should_swap_light(self):
    #     light1 = self.intersection.lightat(self.st1)
    #     light2 = self.intersection.lightat(self.st2)
    #     self.intersection.swaplight()
    #
    #     self.assertNotEqual(self.intersection.lightat(self.st1), light1)
    #     self.assertNotEqual(self.intersection.lightat(self.st2), light2)

    def test_should_go_if_green(self):
        light1 = self.intersection.lightat(self.st1)

        if light1 == TrafficLight.GREEN:
            self.assertTrue(self.intersection.go(self.st1))
            self.assertFalse(self.intersection.go(self.st2))
        else:
            self.assertTrue(self.intersection.go(self.st2))
            self.assertFalse(self.intersection.go(self.st1))

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

    def test_get_all_intersections(self):
        all_intersections = self.intersectionpool.all()
        self.assertEqual(len(all_intersections), len(self.sts_EW) * len(self.sts_NS))
        for i in range(5):
            self.assertIn(self._random_intersection(), all_intersections)

# TODO: add test for getting intersection that does not existZ
    def test_get_one_intersection(self):
        intersection_returned = self.intersectionpool.getat('B', '2')
        intersection_expected = Intersection('B', '2')
        self.assertEqual(intersection_expected, intersection_returned)

    def test_filter_intersection(self):
        filtered = self.intersectionpool.filter_street('B')
        expected_dict = {'1': Intersection('B', '1'), '2': Intersection('B', '2'), '3': Intersection('B', '3')}
        self.assertDictEqual(filtered, expected_dict)

