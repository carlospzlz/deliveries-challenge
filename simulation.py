import collections

import numpy
from matplotlib import animation
from matplotlib import pyplot


MAX_AXIS = 20
DRONE_MARKER = 'X'
DRONE_COLOR = 'royalblue'
CYCLIST_MARKER = 'o'
CYCLIST_COLOR = 'orange'
TRAIL_MARKER = '.'
DELIVERY_MARKER = 's'
PENDING_DELIVERY_COLOR = 'r'
DONE_DELIVERY_COLOR = 'lime'
RELATIVE_TOLERANCE = 0
ABSOLUTE_TOLERANCE = 0.5


class Simulation(object):
    """
    """
    def __init__(self, deliveries, drones, cyclists, scheduler):
        self.__deliveries, self.__delivered = self.__create_deliveries(
            deliveries)
        self.__drones = self.__create_vehicles_array(drones)
        self.__cyclists = self.__create_vehicles_array(cyclists)
        self.__routes = {}
        self.__scheduler = scheduler
        self.__deliveries_scatter = {}
        self.__drones_scatter = None
        self.__cyclists_scatter = None
        self.__ticks = 0
        self.__total_kms = 0
        self.__hud = None

    def __create_deliveries(self, deliveries):
        """
        """
        indexed_deliveries, indexed_delivered = {}, {}
        for delivery in deliveries:
            indexed_deliveries[delivery.destination] = set(delivery.packages)
            indexed_delivered[delivery.destination] = set()
        return indexed_deliveries, indexed_delivered

    def __create_vehicles_array(self, vehicles):
        """
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
        ani = animation.FuncAnimation(
            pyplot.gcf(), self.__update, init_func=self.__init_func,
            interval=10)
        pyplot.show()

    def __init_func(self):
        pyplot.axis((-MAX_AXIS, MAX_AXIS, -MAX_AXIS, MAX_AXIS))
        pyplot.grid(zorder=0)
        self.__initialize_deliveries()
        self.__initialize_vehicles()
        self.__initialize_hud()

    def __initialize_deliveries(self):
        for destination in self.__deliveries.keys():
            x, y = destination
            self.__deliveries_scatter[destination] = pyplot.scatter(
                (x, ), (y, ), marker=DELIVERY_MARKER,
                color='k', facecolors=PENDING_DELIVERY_COLOR, zorder=20)

    def __initialize_vehicles(self):
        self.__drones_scatter = self.__create_vehicles_scatter(
            self.__drones, DRONE_MARKER, DRONE_COLOR, 40)
        self.__cyclists_scatter = self.__create_vehicles_scatter(
            self.__cyclists, CYCLIST_MARKER, CYCLIST_COLOR, 30)
        pyplot.legend(
            (self.__drones_scatter, self.__cyclists_scatter),
            ('Drones', 'Cyclists'))

    def __create_vehicles_scatter(self, vehicles, marker, color, zorder):
        """
        """
        n = len(vehicles)
        scatter = pyplot.scatter(
            numpy.zeros(n), numpy.zeros(n), marker=marker, color=color,
            zorder=zorder)
        return scatter

    def __initialize_hud(self):
        self.__hud = pyplot.text(
            MAX_AXIS - 6, 2 - MAX_AXIS, '0 ticks\n0 kms',
            bbox=dict(facecolor='white'))

    def __update(self, frame):
        self.__update_hud(frame)
        self.__update_vehicles()
        self.__plot_vehicles()

    def __update_hud(self, frame):
        if self.__deliveries != self.__delivered:
            self.__ticks = frame
        text = '{} ticks\n{} kms'.format(self.__ticks, self.__total_kms)
        self.__hud.set_text(text)

    def __update_vehicles(self):
        self.__update_drones()
        self.__update_cyclists()

    def __update_drones(self):
        for drone in numpy.nditer(
                self.__drones, flags=['zerosize_ok'], op_flags=['readwrite']):
            id_ = str(drone['id'])
            if self.__vehicle_is_at_depot(drone):
                route = self.__scheduler.get_route()
                if route:
                    self.__routes[id_] = route
                    destination, _ = route[0]
                    drone['destination'] = destination
                    length = numpy.sqrt((drone['destination'] ** 2).sum())
                    drone['delta'] = drone['destination'] / length
            elif self.__vehicle_is_at_destination(drone):
                _, package = self.__routes[id_].pop()
                destination = tuple(drone['destination'])
                self.__deliver_packages(id_, 'drone', destination, (package, ))
                drone['destination'] = numpy.zeros(2)
                drone['delta'] = -drone['delta']
            else:
                drone['position'] += drone['delta']
                self.__total_kms += 1

    def __update_cyclists(self):
        """
        """
        pass

    def __vehicle_is_at_depot(self, vehicle):
        """
        """
        return (self.__are_close(vehicle['destination'], numpy.zeros(2)) and
                self.__are_close(vehicle['position'], numpy.zeros(2)))


    def __vehicle_is_at_destination(self, vehicle):
        """
        """
        return self.__are_close(vehicle['position'], vehicle['destination'])

    def __are_close(self, array1, array2):
        """
        """
        return numpy.allclose(
            array1, array2, rtol=RELATIVE_TOLERANCE, atol=ABSOLUTE_TOLERANCE)

    def __deliver_packages(self, id_, type_, destination, packages):
        """
        """
        print('{} {} delivered to {} packages: {}'.format(
            type_.capitalize(), id_, destination, packages))
        self.__delivered[destination].update(packages)
        if self.__delivered[destination] == self.__deliveries[destination]:
            self.__deliveries_scatter[destination].set_facecolor(
                DONE_DELIVERY_COLOR)

    def __plot_vehicles(self):
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


class Scheduler(object):
    def __init__(self):
        self.__drones_routes = (
            collections.deque(
                (((5, 4), 'product0'), )),
            collections.deque(
                (((5, 4), 'product1'), )),
            collections.deque(
                (((5, 4), 'product2'), )),
            collections.deque(
                (((15, 9), 'product3'), )),
            collections.deque(
                (((6, 7), 'product4'), )),
        )
        self.__drones_routes_idx = 0

    def get_route(self):
        if self.__drones_routes_idx < len(self.__drones_routes):
            route = self.__drones_routes[self.__drones_routes_idx]
            self.__drones_routes_idx += 1
            return route
        return None


if __name__ == '__main__':
    Delivery = collections.namedtuple('Delivery', 'packages destination')
    deliveries = [
        Delivery(('product0', 'product1', 'product2'), (5, 4)),
        Delivery(('product3', ), (15, 9)),
        Delivery(('product4', ), (6, 7)),
    ]

    #drones = ('hey', 'hoy', 'hay')
    drones = ('hey', )
    cyclists = ('holi', )
    sim = Simulation(deliveries, drones, cyclists, Scheduler())
    sim.start()
