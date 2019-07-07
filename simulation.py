"""
This module contains a convenience class Simulation to test and visualize
results with different combinations of number of drones, cyclists and specific
schedulers.
"""

import numpy
from matplotlib import animation
from matplotlib import pyplot


# Drawing context.
FIGURE_SIZE = (480, 480)
MAX_AXIS = 20
FRAME_DELAY = 10 # Delay between frames in milliseconds.

# Object drawing.
DRONE_MARKER = 'X'
DRONE_COLOR = 'royalblue'
CYCLIST_MARKER = 'o'
CYCLIST_COLOR = 'orange'
TRAIL_MARKER = '.'
DELIVERY_MARKER = 's'
PENDING_DELIVERY_COLOR = 'r'
DONE_DELIVERY_COLOR = 'lime'

# Point comparison.
RELATIVE_TOLERANCE = 0
ABSOLUTE_TOLERANCE = 0.5


class Simulation(object):
    """
    Class responsible to draw the fleet of drones and cyclists delivering the
    packages following the routes generated by a specific scheduler.
    This is a very visual way to observe the routes drones and cyclists take
    and to identify how that affects to the time and total kms needed to
    perform all deliveries.
    """
    def __init__(self, deliveries, drones, cyclists, scheduler):
        """
        Constructs the simulation.
        """
        self.__deliveries, self.__delivered = self.__create_deliveries(
            deliveries)
        self.__drones = self.__create_vehicles_array(drones)
        self.__cyclists = self.__create_vehicles_array(cyclists)
        self.__routes = {}
        self.__scheduler = scheduler
        self.__deliveries_scatter = {}
        self.__drones_scatter = None
        self.__cyclists_scatter = None
        self.__tick = 0
        self.__time = '0h 0s'
        self.__total_kms = 0
        self.__hud = None

    def __create_deliveries(self, deliveries):
        """
        Creates needed structures to track state of deliveries.
        """
        indexed_deliveries, indexed_delivered = {}, {}
        for delivery in deliveries:
            indexed_deliveries[delivery.destination] = set(delivery.packages)
            indexed_delivered[delivery.destination] = set()
        return indexed_deliveries, indexed_delivered

    def __create_vehicles_array(self, vehicles):
        """
        Creates a numpy array with data about the given vehicles to simulate
        their behaviour.
        """
        array = numpy.zeros(
            len(vehicles), dtype=[
                ('position', float, 2),
                ('destination', float, 2),
                ('delta', float, 2),
                ('id', str, 6),
            ]
        )
        array['id'] = vehicles
        return array

    def start(self):
        """
        Starts the simulation.
        """
        ani = animation.FuncAnimation(
            pyplot.gcf(), self.__update, init_func=self.__init_func,
            interval=FRAME_DELAY)
        pyplot.show()

    def __init_func(self):
        """
        Initializes the first frame of the simulation.
        """
        figure = pyplot.gcf()
        dpi = figure.get_dpi()
        figure.set_size_inches(
            FIGURE_SIZE[0]/float(dpi), FIGURE_SIZE[1]/float(dpi))
        figure.canvas.set_window_title('Simulation')
        title = '{} drones, {} cyclists and {}'.format(
            len(self.__drones), len(self.__cyclists), self.__scheduler.name)
        pyplot.suptitle(title, fontweight='bold')
        pyplot.axis((-MAX_AXIS, MAX_AXIS, -MAX_AXIS, MAX_AXIS))
        pyplot.grid(zorder=0)
        self.__initialize_deliveries()
        self.__initialize_vehicles()
        self.__initialize_hud()

    def __initialize_deliveries(self):
        """
        Initializes a point scatter per delivery to show their state.
        """
        for destination in self.__deliveries.keys():
            x, y = destination
            self.__deliveries_scatter[destination] = pyplot.scatter(
                (x, ), (y, ), marker=DELIVERY_MARKER,
                color='k', facecolors=PENDING_DELIVERY_COLOR, zorder=20)

    def __initialize_vehicles(self):
        """
        Initializes a point scatter per vehicle type.
        """
        self.__drones_scatter = self.__create_vehicles_scatter(
            self.__drones, DRONE_MARKER, DRONE_COLOR, 40)
        self.__cyclists_scatter = self.__create_vehicles_scatter(
            self.__cyclists, CYCLIST_MARKER, CYCLIST_COLOR, 30)
        pyplot.legend(
            (self.__drones_scatter, self.__cyclists_scatter),
            ('Drones', 'Cyclists'))

    def __create_vehicles_scatter(self, vehicles, marker, color, zorder):
        """
        Initializes a point scatter to draw a specific type of vehicles with
        the given characteristics.
        """
        n = len(vehicles)
        scatter = pyplot.scatter(
            numpy.zeros(n), numpy.zeros(n), marker=marker, color=color,
            zorder=zorder)
        return scatter

    def __initialize_hud(self):
        """
        Initializes extra information displayed on top of the graph.
        """
        self.__hud = pyplot.text(
            MAX_AXIS - 9, 2 - MAX_AXIS, '0 ticks\n0 kms',
            bbox=dict(facecolor='white'))

    def __update(self, frame):
        """
        Update function called in every tick to update the 'world'.
        """
        self.__update_hud(frame)
        self.__update_vehicles()
        self.__plot_vehicles()

    def __update_hud(self, frame):
        """
        Updates the extra information displayed on top of the graph.
        This includes the current tick, the elapsed time and the tolal kms.
        """
        if self.__deliveries != self.__delivered:
            self.__tick = frame
            # Each tick is 2 minutes.
            minutes = self.__tick * 2
            self.__time = '{}h {}m'.format(int(minutes / 60), minutes % 60)
        text = 'Tick:  {}\nTime: {}\nKms:  {}'.format(
            self.__tick, self.__time, self.__total_kms)
        self.__hud.set_text(text)

    def __update_vehicles(self):
        """
        Updates all vehicles in the fleet.
        """
        self.__update_drones()
        self.__update_cyclists()

    def __update_drones(self):
        """
        Updates drones.

        There are three possible situations:
        - The drone is at the depot, hence it requests a new route.
        - The drones has arrived at its detination, hence it comes back to
        depot.
        - The drone is flying.
        """
        for drone in numpy.nditer(
                self.__drones, flags=['zerosize_ok'], op_flags=['readwrite']):
            id_ = str(drone['id'])
            if self.__vehicle_is_at_depot(drone):
                route = self.__scheduler.get_route_for_drone()
                if route:
                    print('Drone {} got route: {}'.format(id_, route))
                    self.__routes[id_] = route
                    destination, _ = route[0]
                    drone['destination'] = destination
                    length = numpy.sqrt((drone['destination'] ** 2).sum())
                    # Drones move at a speed of 1km/tick (1km/2minutes)
                    drone['delta'] = drone['destination'] / length
            elif self.__vehicle_is_at_destination(drone):
                destination, packages = self.__routes[id_].pop()
                self.__deliver_packages(id_, 'drone', destination, packages)
                drone['destination'] = numpy.zeros(2)
                drone['delta'] = -drone['delta']
            else:
                drone['position'] += drone['delta']
                self.__total_kms += 1

    def __update_cyclists(self):
        """
        Updates cyclists.

        There are three possible situations:
        - The cyclist is at the depot, hence it requests a new route.
        - The cyclist has arrived at its detination, hence it heads to the new
        destination in the route.
        - The cyclist is cycling.
        """
        for cyclist in numpy.nditer(
                self.__cyclists, flags=['zerosize_ok'],
                op_flags=['readwrite']):
            id_ = str(cyclist['id'])
            if self.__vehicle_is_at_depot(cyclist):
                route = self.__scheduler.get_route_for_cyclist()
                if route:
                    print('Cyclist {} got route: {}'.format(id_, route))
                    self.__routes[id_] = route
                    destination, _ = route[0]
                    cyclist['destination'] = destination
            elif self.__vehicle_is_at_destination(cyclist):
                route = self.__routes[id_]
                destination, packages = route.pop()
                self.__deliver_packages(id_, 'cyclist', destination, packages)
                if route:
                    destination, _ = route[0]
                    cyclist['destination'] = destination
                else:
                    cyclist['destination'] = numpy.zeros(2)
            else:
                # Cyclists move at a speed of 0.5km/tick (0.5km/2minutes)
                self.__update_cyclist_delta(cyclist)
                cyclist['position'] += cyclist['delta']
                self.__total_kms += 0.5

    def __update_cyclist_delta(self, cyclist):
        """
        Updating the given cyclist delta according to its current position and
        destination.
        """
        aim = cyclist['destination'] - cyclist['position']
        if abs(aim[0]) > abs(aim[1]):
            x = 0.5 * numpy.sign(aim[0])
            cyclist['delta'] = numpy.array((x, 0))
        else:
            y = 0.5 * numpy.sign(aim[1])
            cyclist['delta'] = numpy.array((0, y))

    def __vehicle_is_at_depot(self, vehicle):
        """
        Returns whether the given vehicle is at the depot.
        """
        return (self.__are_close(vehicle['destination'], numpy.zeros(2)) and
                self.__are_close(vehicle['position'], numpy.zeros(2)))


    def __vehicle_is_at_destination(self, vehicle):
        """
        Returns whether the given vehicle is at its destination.
        """
        return self.__are_close(vehicle['position'], vehicle['destination'])

    def __are_close(self, array1, array2):
        """
        Returns if two points are close to each other.
        """
        return numpy.allclose(
            array1, array2, rtol=RELATIVE_TOLERANCE, atol=ABSOLUTE_TOLERANCE)

    def __deliver_packages(self, id_, type_, destination, packages):
        """
        The vehicle with the id `id_` has delivered the given packages to the
        given destination.
        """
        print('{} {} delivered to {} packages: {}'.format(
            type_.capitalize(), id_, destination, packages))
        self.__delivered[destination].update(packages)
        if self.__delivered[destination] == self.__deliveries[destination]:
            self.__deliveries_scatter[destination].set_facecolor(
                DONE_DELIVERY_COLOR)

    def __plot_vehicles(self):
        """
        Draws the vehicles in the graph.
        """
        self.__drones_scatter.set_offsets(self.__drones['position'])
        self.__cyclists_scatter.set_offsets(self.__cyclists['position'])
        trail = (
            (self.__drones, DRONE_COLOR), (self.__cyclists, CYCLIST_COLOR))
        for vehicles, color in trail:
            x = vehicles['position'][:, 0]
            y = vehicles['position'][:, 1]
            pyplot.plot(
                x, y, marker=TRAIL_MARKER, linestyle='', color=color,
                zorder=10)
