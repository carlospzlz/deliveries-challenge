import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


DRONE_MARKER = '^'
DRONE_COLOR = 'b'
CYCLIST_MARKER = 'o'
CYCLIST_COLOR = 'r'


class Simulation(object):
    """
    """
    def __init__(self, schedule, n_drones, n_cyclists):
        self.__drones = np.zeros(n_drones, dtype=[('position', float, 2)])
        self.__cyclists = np.zeros(n_cyclists, dtype=[('position', float, 2)])
        self.__drones_scatter = None
        self.__cyclists_scatter = None

    def start(self):
        ani = FuncAnimation(
            plt.gcf(), self.__update, init_func=self.__init_func, interval=10)
        plt.show()

    def __init_func(self):
        plt.axis((-20, 20, -20, 20))
        plt.grid()
        self.__drones_scatter = plt.scatter(
            [0], [0], marker=DRONE_MARKER, color=DRONE_COLOR)
        self.__cyclists_scatter = plt.scatter(
            [0], [0], marker=CYCLIST_MARKER, color=CYCLIST_COLOR)
        plt.legend(
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
            plt.plot(x, y, color + '.', zorder=0)


if __name__ == '__main__':
    sim = Simulation(None, 1, 1)
    sim.start()

