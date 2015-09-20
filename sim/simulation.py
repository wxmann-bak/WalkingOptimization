__author__ = 'tangz'

def algorithm_ideal(routetracker, timekeeper):
    while True:
        caneast = routetracker.has_next_east()
        cannorth = routetracker.has_next_north()
        if not caneast and not cannorth:
            # done
            break
        elif caneast and cannorth:
            # we have free choice to cross or turn
            if routetracker.must_cross():
                # if green light, we go ahead and cross
                if routetracker.green_light():
                    routetracker.cross()
                    timekeeper.track_cross()
                # if red light, we turn and cross other street instead
                else:
                    routetracker.turn()
                    if routetracker.must_cross():
                        routetracker.cross()
                        timekeeper.track_cross()
        else:
            if not caneast and routetracker.going_east():
                routetracker.turn()
            elif not cannorth and routetracker.going_north():
                routetracker.turn()

            if routetracker.must_cross():
                if not routetracker.green_light():
                    timekeeper.track_wait()
                routetracker.cross()
                timekeeper.track_cross()

        routetracker.next_block()
        timekeeper.track_walk_block()

    return timekeeper.output_time()


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
