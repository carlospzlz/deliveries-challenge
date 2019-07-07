"""
"""

from collections import namedtuple


Delivery = namedtuple('Delivery', 'packages destination')


class Scheduler(object):
    """
    """
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def _get_route_for_drone(self):
        """
        """
        return None

    def _get_route_for_cyclist(self):
        """
        """
        return None
