"""
This module contains a more sofisticated scheduling approach that, in addition
to use two queues, uses techniques such as the Sweep Algorithm to improve the
cyclists' routes and a mechanism to leverage the work of the drones when they
are too overloaded.
"""

from collections import deque
from itertools import permutations
from math import atan2, sqrt
from sys import maxsize


from scheduler import Scheduler


class Scheduler3(Scheduler):
    """
    This scheduler also distributes all the packages in the drones queue and
    the cyclists queue. It uses the Sweep Algorithm to optimize the routes for
    the cyclists. This consists on sorting the packages using a rotating ray
    centered at the depot, and then solving the Travelling Salesman Problem
    for every batch. As cyclists can batch up to 4 packages as maximum, we use
    a brute force approach, checking which one of the permutations of the
    packages to be delivered produces the optimal route.

    This scheduler presents the following problems:
    - This scheduler uses a greedy approach to batch the packages in the queue,
    the problem with this is that packages used to form a route might no the
    be the ones that are closest to each other. This could be solved by
    sweeping the whole angular spectrum, using the caterpillar movement, to
    calculate the best route possible. It could also be improved using applying
    more advanced clustering techniques.
    - We also have some room for improvement in the balacing process. Unloading
    the drones on the cyclists may add new routes in areas that they have
    already visited. A way to tackle this could be to take into account the
    angular position of when adding the packages from the drones queue to the
    cyclists queue.
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
        latter one. This measure attacks the bottleneck that a low number of
        drones can cause.

        Returns whether a re-balancing happened or not.
        """
        n, m = len(self.__drones_queue), len(self.__cyclists_queue)
        if n > m:
            for _ in range(int((n + 1) / 2)):
                self.__cyclists_queue.append(self.__drones_queue.popleft())
            return True
        return False

    @staticmethod
    def __sort_by_angle(packages):
        """
        Sorts all the packages by the angle between the X axis and their
        position vector. It goes from -PI to PI. This simulates the rotating
        ray centered at the depot.
        """
        sorted_list = sorted(packages, key=lambda p: atan2(p[0][1], p[0][0]))
        return deque(sorted_list)

    def get_route_for_drone(self):
        """
        Returns a route for the next package in the drones queue.
        """
        if self.__drones_queue:
            destination, product = self.__drones_queue.popleft()
            route_stop = (destination, (product, ))
            route = deque((route_stop, ))
            return route
        return None

    def get_route_for_cyclist(self):
        """
        Returns a route batching the maximum number of packages and trying
        to provide an optimal route.
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
                if route_stops:
                    return self.__create_best_route(route_stops)
                return None
        # After all elements in the queue have been consumed we may have a
        # valid route.
        if route_stops:
            return self.__create_best_route(route_stops)
        return None

    @staticmethod
    def __create_best_route(route_stops):
        """
        Solves the TSP with the given route stops by brute force. This
        shouldn't have an impact in performance as we would expect 4 route
        stops as maximum.
        """
        routes = permutations(route_stops, len(route_stops))
        min_kms, best_route = maxsize, None
        for route in routes:
            kms = Scheduler3.__calculate_route_distance(route)
            if kms < min_kms:
                min_kms, best_route = kms, route
        return deque(best_route)

    @staticmethod
    def __calculate_route_distance(route):
        """
        Calculates the traveled distance in the given route.
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
