"""
This modules contains unit-tests for the Scheduler3
"""

from collections import deque
from unittest import TestCase

from scheduler import Delivery
from scheduler3 import Scheduler3


class TestScheduler3(TestCase):
    """
    Tests for the Scheduler3
    """

    def test_get_route_for_drone_package_less_than_five_kg(self):
        """
        A package of weight less than 5 kg can be given to a drone.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0' : 2}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_drone()
        self.assertEqual(result, expected)

    def test_get_route_for_drone_package_equal_to_five_kg(self):
        """
        A package of weight equal to 5 kg can be given to a drone.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 5}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_drone()
        self.assertEqual(result, expected)

    def test_get_route_for_drone_package_greater_than_five_kg(self):
        """
        A package of weight greater than 5 kg cannot be given to a drone.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 6}
        scheduler = Scheduler3(deliveries, weights)
        expected = None
        result = scheduler.get_route_for_drone()
        self.assertEqual(result, expected)

    def test_get_route_for_drone_from_delivery(self):
        """
        A package from a delivery can be given to a drone.
        """
        deliveries = (
            Delivery(('product0', 'product1', 'product2'), (4, 2)),
        )
        weights = {'product0': 6, 'product1':10, 'product2':5}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product2', )),
        ))
        result = scheduler.get_route_for_drone()
        self.assertEqual(result, expected)

    def test_get_route_for_drone_delivery_fully_delivered_by_drones(self):
        """
        All packages from a delivery can be given to drones.
        """
        deliveries = (
            Delivery(('product0', 'product1', 'product2', 'product3'), (4, 2)),
        )
        weights = {'product0': 5, 'product1': 5, 'product2': 5, 'product3': 5}
        scheduler = Scheduler3(deliveries, weights)

        for product in deliveries[0].packages:
            expected = deque((
                ((4, 2), (product, )),
            ))
            result = scheduler.get_route_for_drone()
            self.assertEqual(result, expected)

    def test_get_route_for_cyclist_package_less_than_five_kg(self):
        """
        A package of weight less than 5 kg can be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 2}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_package_equal_to_five_kg(self):
        """
        A package of weight equal to 5 kg can be given to a drone.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 5}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_package_greater_than_five_kg(self):
        """
        A package of weight greater than 5 kg can be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 6}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_package_equal_fifty_kg(self):
        """
        A package of weight equal to 50 kg can be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 50}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_package_greater_than_fifty_kg(self):
        """
        A package of weight greater than 50 kg cannot be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', ), (4, 2)),
        )
        weights = {'product0': 51}
        scheduler = Scheduler3(deliveries, weights)
        expected = None
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_from_delivery_batch_several(self):
        """
        Several packages from a delivery can be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', 'product1', 'product2'), (4, 2)),
        )
        weights = {'product0': 6, 'product1':10, 'product2': 5}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((4, 2), ('product0', )),
            ((4, 2), ('product1', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_batch_packages_different_deliveries(self):
        """
        Packages from several deliveries can be given to a cyclist.
        """
        deliveries = (
            Delivery(('product0', 'product1'), (1, 0)),
            Delivery(('product2', 'product3'), (0, 1)),
        )
        weights = {'product0': 7, 'product1': 7, 'product2': 7, 'product3': 7}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((1, 0), ('product0', )),
            ((1, 0), ('product1', )),
            ((0, 1), ('product2', )),
            ((0, 1), ('product3', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_batch_packages_up_to_four(self):
        """
        Cyclists can batch packages up o 4 packages.
        """
        deliveries = (
            Delivery(('product0', 'product1', 'product2'), (1, 0)),
            Delivery(('product3', 'product4'), (0, 1)),
        )
        weights = {
            'product0': 7, 'product1': 7, 'product2': 7, 'product3': 7,
            'product4': 7
        }
        scheduler = Scheduler3(deliveries, weights)

        # First cyclist.
        expected = deque((
            ((1, 0), ('product0', )),
            ((1, 0), ('product1', )),
            ((1, 0), ('product2', )),
            ((0, 1), ('product3', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

        # Second cyclist.
        expected = deque((
            ((0, 1), ('product4', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)


    def test_get_route_for_cyclist_batch_packages_up_to_fifty_kg(self):
        """
        Cyclists can batch packages up to 50 kg.
        """
        deliveries = (
            Delivery(('product0', 'product1'), (1, 0)),
            Delivery(('product2', 'product3'), (0, 1)),
        )
        weights = {'product0': 7, 'product1': 7, 'product2': 7, 'product3': 49}
        scheduler = Scheduler3(deliveries, weights)

        # First cyclist.
        expected = deque((
            ((1, 0), ('product0', )),
            ((1, 0), ('product1', )),
            ((0, 1), ('product2', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

        # Second cyclist.
        expected = deque((
            ((0, 1), ('product3', )),
        ))
        result = scheduler.get_route_for_cyclist()
        self.assertEqual(result, expected)

    def test_get_route_for_cyclist_best_route_is_given(self):
        """
        Cyclists are given an optimal route.
        """
        deliveries = (
            Delivery(('product0', ), (2, 3)),
            Delivery(('product1', ), (1, 1)),
            Delivery(('product2', ), (2, 1)),
        )
        weights = {'product0': 7, 'product1': 7, 'product2': 7}
        scheduler = Scheduler3(deliveries, weights)
        expected = deque((
            ((1, 0), ('product0', )),
            ((1, 0), ('product1', )),
            ((0, 1), ('product2', )),
        ))
        result = scheduler.get_route_for_cyclist()
        print(result)
        self.assertEqual(result, expected)

    # packages of different deliveries can given to the same cyclist

    # the best route is given to cyclist
