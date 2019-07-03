import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial


class Simulation(object):
    """
    """
    def __init__(self):
        plt.axis((-20, 20, -20, 20))
        plt.grid()
        self.__x = 0

    def setup(self, schedule):
        self.__points = ([1, 1], [2, 2], [3, 3], [4, 4])

    def start(self):
        ani = FuncAnimation(
            plt.gcf(), self.__update, init_func=self.__init_func, interval=10)
        plt.show()

    def __init_func(self):
        x_coords = []
        y_coords = []
        for point in self.__points:
            x_coords.append(point[0])
            y_coords.append(point[0])
        plt.plot(x_coords, y_coords, 'r.')

    def __update(self, frame):
        self.__updateVehicles()
        self.__plotVehicles()

    def __updateVehicles(self):
        for point in self.__points:
            point[1] += 0.5

    def __plotVehicles(self):
        x_coords = []
        y_coords = []
        for point in self.__points:
            x_coords.append(point[0])
            y_coords.append(point[1])
        plt.plot(x_coords, y_coords, 'r.')


if __name__ == '__main__':
    sim = Simulation()
    sim.setup(None)
    sim.start()

