import collections

import numpy
from matplotlib import animation
from matplotlib import pyplot


DRONE_MARKER = 'X'
DRONE_COLOR = 'royalblue'
CYCLIST_MARKER = 'o'
CYCLIST_COLOR = 'orange'
TRAIL_MARKER = '.'
DELIVERY_MARKER = 's'
DELIVERY_COLOR = 'r'


class Simulation(object):
    """
    """
    def __init__(self, deliveries, n_drones, n_cyclists, schedule):
        self.__deliveries = deliveries
        self.__drones = numpy.zeros(n_drones, dtype=[('position', float, 2)])
        self.__cyclists = numpy.zeros(
            n_cyclists, dtype=[('position', float, 2)])
        self.__drones_scatter = None
        self.__cyclists_scatter = None

    def start(self):
        ani = animation.FuncAnimation(
            pyplot.gcf(), self.__update, init_func=self.__init_func,
            interval=10)
        pyplot.show()

    def __init_func(self):
        pyplot.axis((-20, 20, -20, 20))
        pyplot.grid(zorder=0)
        self.__plotDeliveries()
        self.__initializeVehicles()

    def __plotDeliveries(self):
        x_coords = [delivery.destination[0] for delivery in deliveries]
        y_coords = [delivery.destination[1] for delivery in deliveries]
        pyplot.scatter(
            x_coords, y_coords, marker=DELIVERY_MARKER, color=DELIVERY_COLOR,
            zorder=20)

    def __initializeVehicles(self):
        self.__drones_scatter = pyplot.scatter(
            [0], [0], marker=DRONE_MARKER, color=DRONE_COLOR, zorder=40)
        self.__cyclists_scatter = pyplot.scatter(
            [0], [0], marker=CYCLIST_MARKER, color=CYCLIST_COLOR, zorder=30)
        pyplot.legend(
            (self.__drones_scatter, self.__cyclists_scatter),
            ('Drones', 'Cyclists'))

    def __update(self, frame):
        self.__updateVehicles()
        self.__plotVehicles()

    def __updateVehicles(self):
        self.__drones['position'][0] += (1, 1)
        self.__cyclists['position'][0] += (-0.5, 0.5)

    def __plotVehicles(self):
        self.__drones_scatter.set_offsets(self.__drones['position'])
        self.__cyclists_scatter.set_offsets(self.__cyclists['position'])
        trail = (
            (self.__drones, DRONE_COLOR), (self.__cyclists, CYCLIST_COLOR))
        for vehicles, color in trail:
            x = vehicles['position'][:, 0]
            y = vehicles['position'][:, 1]
            pyplot.plot(x, y, marker=TRAIL_MARKER, color=color, zorder=10)


if __name__ == '__main__':
    Delivery = collections.namedtuple('Delivery', 'packages destination')
    deliveries = [
        Delivery(('product0', 'product1', 'product2'), (5, 4)),
        Delivery(('product3'), (15, 9)),
        Delivery(('product4'), (6, 7)),
        Delivery(('product5'), (7, 7)),
    ]

    sim = Simulation(deliveries, 1, 1, None)
    sim.start()

