"""
This module contains a scheduler based on two queues, one with packages to be
delivered by drones and other with packages to be delivered by cyclists.
This scheduler also implements some basic batching for the packages for the
cyclists.
"""

from collections import deque

from scheduler import Scheduler


class Scheduler2(Scheduler):
    """
    This scheduler distributes all the packages in two queues, one for the
    drones and other for the cyclists. In addition, it tries to batch packages
    for a single cyclist.

    This scheduler presents the following problems:
    - Due to the fact that we treat packages independently the routes for the
    cyclists are very inefficient.
    - The number of drones could be a bottleneck.
    """

    def __init__(self, deliveries, weights):
        super(Scheduler2, self).__init__('Scheduler2')
        self.__weights = weights
        self.__drones_queue, self.__cyclists_queue = self.__create_queues(
            deliveries, weights)

    @staticmethod
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
        Returns a route batching the maximum number of packages from the queue
        up to 4 or 50kg.
        """
        route = deque()
        total_weight = 0
        while self.__cyclists_queue:
            destination, product = self.__cyclists_queue[0]
            total_weight += self.__weights[product]
            if len(route) < 4 and total_weight <= 50:
                route_stop = (destination, (product, ))
                route.append(route_stop)
                self.__cyclists_queue.popleft()
            else:
                return route
        # After all elements in the queue have been consumed we may have a
        # valid route.
        if route:
            return route
        return None
