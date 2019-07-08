"""
This module contains interface that schedulers should implement.
"""

from abc import ABC, abstractmethod
from collections import namedtuple


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
