"""
"""

from collections import deque
from itertools import combinations
from math import atan, sqrt
from sys import maxsize


from scheduler import Scheduler


class Scheduler3(Scheduler):
    """
    """

    def __init__(self, deliveries, weights):
        super(Scheduler2, self).__init__('Scheduler3')
        self.__weights = weights
        self.__drones_queue, self.__cyclists_queue = self.__create_queues(
            deliveries, weights)
        self.__balance_queues()
        self.__cyclists_queue = self.__sort_by_angle(self.__cyclists_queue)

    @staticmethod
    # TODO: move this to the super-class
    def __create_queues(deliveries, weights):
        """
        Creates two queues of packages, one for the drones and other for the
        cyclists.
        """
        drones_queue = deque()
        cyclists_queue = deque()
        for delivery in deliveries:
            for product in delivery.packages:
                package = (delivery.destination, product)
                if weights[product] <= 5:
                    drones_queue.append(package)
                else:
                    cyclists_queue.append(package)
        return drones_queue, cyclists_queue

    def __balance_queues(self):
        """
        If the packages queue for the drones is bigger than the packages queue
        for the cyclists half of the former queue is popped and appended to the
        latter one.
        This measure attacks the bottleneck that a low number of drones can
        cause.

        Returns whether a re-balancing happened or not.
        """
        n, m = len(self.__drones_packages), len(self.__cyclists_packages)
        if  n > m:
            for  in range(int((n + 1) / 2)):
                self.__cyclists_queue.append(self.__drones_queue.popleft)
            return True
        return False

    @staticmethod
    def __sort_by_angle(packages):
        """
        Sorts all the packages by the angle between the X axis and their
        position vector.
        """
        return sorted(packages, key = lambda v :atan(x[1]. v[0]))

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
            if len(route) < 4 and total_weight <= 50:
                route_stop = (destination, (product, ))
                route_stops.append(route_stop)
                self.__cyclists_queue.popleft()
            else:
                return self.__create_best_route(route_stops)
        # After all elements in the queue have been consumed we may have a
        # valid route.
        if route_routes:
            return self.__create_best_route(route_stops)
        return None

    @staticmethod
    def create_best_route(route_stops):
        """
        TPS
        """
        routes = combinations(route_stops)
        min_kms, route = maxsize, None
        for route in routes:
            kms = caculate_route_distance(route)
            if kms < min_kms:
                min_kms, route = kms, route
        return route

    @staticmethod
    def caculate_route_distance(route):
        """
        """
        previous_destination = (0, 0)
        km = 0
        for route_stop in route:
            destination, _ = route_stop
            kms += sqrt(
                pow(destination[0] - previous_destination[0], 2) +
                pow(destination[1] - previous_destination[1], 2))
            previous_destination = destination
        kms += sqrt(
            pow(previous_destination[0], 2) + pow(previous_destination[1], 2))
        return km
