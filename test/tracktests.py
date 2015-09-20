import unittest
from sim.track import TimeKeeper, RouteTracker, WalkMode
from sim.world import StreetGrid

__author__ = 'tangz'

class RouteTrackerTests(unittest.TestCase):
    def setUp(self):
        self.grid = StreetGrid.with_dimensions(5, 5)

    def test_turn(self):
        routetracker = RouteTracker(self.grid, walkmode=WalkMode.NORTH)
        routetracker.turn()
        self.assertFalse(routetracker.going_north())
        routetracker.turn()
        self.assertTrue(routetracker.going_north())

    def test_no_cross(self):
        routetracker = RouteTracker(self.grid, cross_e=False, cross_n=False)
        self.assertFalse(routetracker.must_cross())
        routetracker.turn()
        self.assertFalse(routetracker.must_cross())

    def test_next_block(self):
        routetracker = RouteTracker(self.grid, cross_e=False, walkmode=WalkMode.EAST)
        routetracker.next_block()
        self.assertEqual(routetracker.get_NS_at(), self.grid.get_NS_st(2))

    def test_cross(self):
        routetracker = RouteTracker(self.grid, cross_e=True, walkmode=WalkMode.EAST)
        self.assertTrue(routetracker.must_cross())
        routetracker.cross()
        self.assertFalse(routetracker.must_cross())
        self.assertEqual(routetracker.get_NS_at(), self.grid.get_NS_st(1))

    def test_composite_walk(self):
        routetracker = RouteTracker(self.grid, cross_e=False, cross_n=False, walkmode=WalkMode.EAST)
        routetracker.next_block()
        routetracker.turn()
        routetracker.next_block()
        routetracker.cross()

        self.assertEqual(routetracker.get_NS_at(), self.grid.get_NS_st(2))
        self.assertEqual(routetracker.get_EW_at(), self.grid.get_EW_st(2))
        self.assertFalse(routetracker.must_cross())

    def test_has_next_street(self):
        routetracker = RouteTracker(self.grid, cross_e=False, cross_n=False, walkmode=WalkMode.EAST)
        for i in range(self.grid.width() - 1):
            self.assertTrue(routetracker.has_next_east())
            routetracker.next_block()
            routetracker.cross()
        self.assertFalse(routetracker.has_next_east())
        routetracker.turn()
        for i in range(self.grid.height() - 1):
            self.assertTrue(routetracker.has_next_north())
            routetracker.next_block()
            routetracker.cross()

        self.assertFalse(routetracker.has_next_north())
        self.assertFalse(routetracker.has_next_east())


class TimeKeeperTests(unittest.TestCase):
    def setUp(self):
        self.cross_street = 2.5
        self.cross_block = 10
        self.wait_intersection = 5
        self.timekeeper = TimeKeeper(self.cross_street, self.cross_block, self.wait_intersection)

    def test_add_cross_street_time(self):
        orig_time = self.timekeeper.output_time()
        self.timekeeper.track_cross()
        new_time = self.timekeeper.output_time()
        self.assertEqual(new_time, orig_time + self.cross_street)

    def test_add_cross_block_time(self):
        orig_time = self.timekeeper.output_time()
        self.timekeeper.track_walk_block()
        new_time = self.timekeeper.output_time()
        self.assertEqual(new_time, orig_time + self.cross_block)

    def test_add_wait_intersection_time(self):
        orig_time = self.timekeeper.output_time()
        self.timekeeper.track_wait()
        new_time = self.timekeeper.output_time()
        self.assertEqual(new_time, orig_time + self.wait_intersection)