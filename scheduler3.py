"""
"""

from collections import deque
from itertools import combinations
from math import atan2, pi, sqrt
from sys import maxsize


from scheduler import Scheduler


class Scheduler3(Scheduler):
    """

    This scheduler presents the following problems:
    - This scheduler uses a greedy approach to batch the packages in the queue,
    the problem with this is that heavy packages might be added to a batch,
    rather batching light packages in the same area. This could be solved with
    a clustering approach and then queue the packages ordered by weight.
    """

    def __init__(self, deliveries, weights):
        super(Scheduler3, self).__init__('Scheduler3')
        self.__weights = weights
        self.__drones_queue, self.__cyclists_queue = self._create_queues(
            deliveries, weights)
        self.__cyclists_queue = self.__sort_by_angle(self.__cyclists_queue)

    def __balance_queues(self):
        """
        If the packages queue for the drones is bigger than the packages queue
        for the cyclists half of the former queue is popped and appended to the
        latter one.
        This measure attacks the bottleneck that a low number of drones can
        cause.

        Returns whether a re-balancing happened or not.
        """
        n, m = len(self.__drones_queue), len(self.__cyclists_queue)
        if  n > m:
            for _ in range(int((n + 1) / 2)):
                self.__cyclists_queue.append(self.__drones_queue.popleft())
            return True
        return False

    @staticmethod
    def __sort_by_angle(packages):
        """
        Sorts all the packages by the angle between the X axis and their
        position vector.
        """
        sorted_list = sorted(packages, key = lambda p: atan2(p[0][1], p[0][0]))
        return deque(sorted_list)

    def get_route_for_drone(self):
        """
        Returns the a route for the next package in the drones queue.
        """
        if self.__drones_queue:
            destination, product = self.__drones_queue.popleft()
            route_stop = (destination, (product, ))
            route = deque((route_stop, ))
            return route
        return None

    def get_route_for_cyclist(self):
        """
        """
        if self.__balance_queues():
            self.__cyclists_queue = self.__sort_by_angle(self.__cyclists_queue)
        total_weight = 0
        route_stops = []
        while self.__cyclists_queue:
            destination, product = self.__cyclists_queue[0]
            total_weight += self.__weights[product]
            if len(route_stops) < 4 and total_weight <= 50:
                route_stop = (destination, (product, ))
                route_stops.append(route_stop)
                self.__cyclists_queue.popleft()
            else:
                return self.__create_best_route(route_stops)
        # After all elements in the queue have been consumed we may have a
        # valid route.
        if route_stops:
            return self.__create_best_route(route_stops)
        return None

    @staticmethod
    def __create_best_route(route_stops):
        """
        TPS
        """
        routes = combinations(route_stops, len(route_stops))
        min_kms, best_route = maxsize, None
        for route in routes:
            kms = Scheduler3.__calculate_route_distance(route)
            if kms < min_kms:
                min_kms, best_route = kms, route
        return deque(route)

    @staticmethod
    def __calculate_route_distance(route):
        """
        """
        previous_destination = (0, 0)
        kms = 0
        for route_stop in route:
            destination, _ = route_stop
            kms += sqrt(
                pow(destination[0] - previous_destination[0], 2) +
                pow(destination[1] - previous_destination[1], 2))
            previous_destination = destination
        kms += sqrt(
            pow(previous_destination[0], 2) + pow(previous_destination[1], 2))
        return kms
