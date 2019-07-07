"""
"""

from collections import deque

from scheduler import Scheduler


class Scheduler1(Scheduler):
    """
    Check deliveries in round-robin fashion and send if possible.
    """
    def __init__(self, deliveries, weights):
        """
        """
        super(Scheduler1, self).__init__('Scheduler1')
        self.__circular_queue = deque(deliveries)
        self.__weights = weights

    #def __create_circular_queue(self, deliveries):
    #    """
    #    """
    #    circular_queue = deque()
    #    for delivery in deliveries:
    #        deque.append(package, delivery.destination)
    #    return circular_queue

    def get_route_for_drone(self):
        """
        """
        for _ in range(len(self.__circular_queue)):
            delivery = self.__circular_queue[0]
            packages = delivery.packages
            if len(packages) == 1 and self.__weights[packages[0]] < 5:
                self.__circular_queue.popleft()
                return deque(((delivery.destination, packages), ))
            self.__circular_queue.rotate(-1)
        return None

    def get_route_for_cyclist(self):
        """
        """
        for _ in range(len(self.__circular_queue)):
            delivery = self.__circular_queue[0]
            packages = delivery.packages
            total_weight = sum(self.__weights[package] for package in packages)
            if total_weight < 50:
                self.__circular_queue.popleft()
                route = deque(((delivery.destination, packages), ))
                return route
            self.__circular_queue.rotate(-1)
        return None


