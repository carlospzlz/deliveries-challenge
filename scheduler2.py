"""
"""

from collections import deque

from scheduler import Scheduler


class Scheduler2(Scheduler):
    """
    This maximizes the load of the cyclists.

    This scheduler presents the following problems:
    """
    def __init__(self, deliveries, weights):
        """
        """
        super(Scheduler2, self).__init__('Scheduler2')
        self.__weights = weights
        self.__drones_queue, self.__cyclists_queue = self.__create_queues(
            deliveries)

    def __create_queues(self, deliveries):
        """
        """
        drones_queue = deque()
        cyclists_queue = deque()
        for delivery in deliveries:
            for product in delivery.packages:
                package = (delivery.destination, product)
                if self.__weights[product] <= 5:
                    drones_queue.append(package)
                else:
                    cyclists_queue.append(package)
        return drones_queue, cyclists_queue

    def get_route_for_drone(self):
        """
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
        route = deque()
        total_weight = 0
        while self.__cyclists_queue:
            destination, product = self.__cyclists_queue[0]
            total_weight = self.__weights[product]
            if total_weight <= 50:
                route_stop = (destination, (product, ))
                route.append(route_stop)
                self.__cyclists_queue.popleft()
            else:
                return route
        if route:
            return route
        return None
