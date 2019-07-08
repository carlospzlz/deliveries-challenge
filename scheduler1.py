"""
This module contains a very basic scheduler based on a queue.
"""

from collections import deque

from scheduler import Scheduler


class Scheduler1(Scheduler):
    """
    This is a very simple scheduler that just queues the deliveries in the same
    order they arrived and when a route is requested the next delivery is given
    if the vehicle can perform it.

    This scheduler presents the following problems:
    - The next delivery could be given to a cyclist, even if it was more
    efficient that a drone did it.
    - Cyclists do single deliveries even if the have capacity to batch some of
    them.
    """

    def __init__(self, deliveries, weights):
        """
        Constructs the scheduler.
        """
        super(Scheduler1, self).__init__('Scheduler1')
        self.__queue = deque(deliveries)
        self.__weights = weights

    def get_route_for_drone(self):
        """
        Returns the route for the following delivery if a drone can handle it.
        """
        if self.__queue:
            delivery = self.__queue[0]
            destination = delivery.destination
            packages = delivery.packages
            if len(packages) == 1 and self.__weights[packages[0]] <= 5:
                self.__queue.popleft()
                route_stop = (destination, packages)
                route = deque((route_stop, ))
                return route
        return None

    def get_route_for_cyclist(self):
        """
        Returns the route for the following delivery if a cyclist can handle
        it.
        """
        if self.__queue:
            delivery = self.__queue[0]
            packages = delivery.packages
            total_weight = sum(self.__weights[package] for package in packages)
            if total_weight <= 50:
                self.__queue.popleft()
                route_stop = (delivery.destination, packages)
                route = deque((route_stop, ))
                return route
        return None
