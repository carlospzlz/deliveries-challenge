"""
This module contains the interface that schedulers should implement.
"""

from abc import ABC, abstractmethod
from collections import namedtuple, deque


Delivery = namedtuple('Delivery', 'packages destination')


class Scheduler(ABC):
    """
    Base abstract class for schedulers.
    """

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        """
        Returns the name of the scheduler.
        """
        return self.__name

    @abstractmethod
    def get_route_for_drone(self):
        """
        Returns route for drone.
        """
        return None

    @abstractmethod
    def get_route_for_cyclist(self):
        """
        Returns route for cyclist.
        """
        return None

    @staticmethod
    def _create_queues(deliveries, weights):
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
