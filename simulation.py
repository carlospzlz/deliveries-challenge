import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
        self.__drones_scatter = plt.scatter([0], [0], marker='^')
        self.__cyclists_scatter = plt.scatter([0], [0], marker='o')
        plt.legend(
            (self.__drones_scatter, self.__cyclists_scatter),
            ('Drones', 'Cyclists'))

    def __update(self, frame):
        #self.__updateVehicles()
        #self.__plotVehicles()
        self.__drones['position'][0] += (1, 1)
        self.__cyclists['position'][0] += (-1, 1)
        self.__drones_scatter.set_offsets(self.__drones['position'])
        self.__cyclists_scatter.set_offsets(self.__cyclists['position'])

    def __updateVehicles(self):
        #for point in self.__points:
        #    point[1] += 0.5
        pass

    def __plotVehicles(self):
        #x_coords = []
        #y_coords = []
        #for point in self.__points:
        #    x_coords.append(point[0])
        #    y_coords.append(point[1])
        #plt.plot(x_coords, y_coords, 'r.')
        pass


if __name__ == '__main__':
    sim = Simulation(None, 1, 1)
    sim.start()

