from entities.buffer import Buffer
from entities.client import Client
from entities.order_manager import OrderManager
from entities.production_line import ProductionLine
from entities.production_manager import ProductionManager
from utility.order_generator import OrderGenerator
from utility.printer import print_clients_table, print_lines_table
from utility.random_generator import PoissonGenerator, UniformGenerator
from utility.runtime import simulated_runtime, yield_task, sleep
from utility.statistics_handler import StatCollector
from utility.substitutes import TrackedLine


async def main(clients: int, lines: int, buffer_capacity: int, lam: int,
               a: int, b: int, duration: float, verbose: bool):
    """Simulates ordering system

    Parameters
    ---
    clients : int
        Total number of clients
    lines : int
        Total number of production lines
    buffer_capacity : int
        Order buffer capacity
    lam : int
        lambda parameter in poisson distribution
    a : int
        lower bound (inclusive) of uniform distribution
    b : int
        higher bound (exclusive) of uniform distribution
    duration : float
        Simulation duration
    verbose : bool
        Should be simulation runtime events logged
    """

    poisson_gen = PoissonGenerator(lam)
    uniform_gen = UniformGenerator(a, b)
    production_list = []
    stat_collector = StatCollector()

    for i in range(1, lines + 1):
        # Create line, set its handler and assign to production manager
        p = TrackedLine(
            ProductionLine(i, uniform_gen),
            lambda l: stat_collector.handle_line_free(l)
        )
        production_list.append(p)

    buffer = Buffer(buffer_capacity)
    production_mgr = ProductionManager(production_list)
    order_mgr = OrderManager(buffer, production_mgr)
    order_gen = OrderGenerator(poisson_gen, stat_collector, duration)

    for i in range(1, clients + 1):
        c = Client(i)
        order_gen.run(c, order_mgr)

    start_timestamp = simulated_runtime.timestamp
    await sleep(duration)
    await order_gen.wait_all_orders()
    end_timestamp = simulated_runtime.timestamp

    print_clients_table(stat_collector.get_clients_table())
    print_lines_table(stat_collector.get_lines_table(),
                      end_timestamp - start_timestamp)


if __name__ == "__main__":
    clients = 5
    lines = 3
    buffer_capacity = 100
    lam = 0.14
    a = 7
    b = 10
    duration = 400
    verbose = False

    simulated_runtime.create_task(
        main(clients, lines, buffer_capacity, lam, a, b, duration, verbose)
    )
    simulated_runtime.run()
