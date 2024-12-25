from entities.buffer import Buffer
from entities.client import Client
from entities.order_manager import OrderManager
from entities.production_line import ProductionLine
from entities.production_manager import ProductionManager
from utility.stat_handlers.logger import Logger
from utility.order_generator import OrderGenerator
from utility.printer import print_clients_table, print_lines_table
from utility.random_generator import PoissonGenerator, UniformGenerator
from utility.runtime import simulated_runtime
from utility.stat_handlers.stat_collector import StatCollector
from utility.stat_handlers.stat_handler import AggregateStatHandler
from utility.substitutes import TrackedLine


async def main(clients: int, lines: int, buffer_capacity: int, lam: int,
               a: int, b: int, max_orders: int, verbose: bool):
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
    max_orders : int
        Total order count
    verbose : bool
        Should be simulation runtime events logged
    """

    poisson_gen = PoissonGenerator(lam)
    client_list = []
    uniform_gen = UniformGenerator(a, b)
    production_list = []
    buffer = Buffer(buffer_capacity)

    for i in range(1, clients + 1):
        c = Client(i)
        client_list.append(c)

    stat_collector = StatCollector()
    stat_handler = AggregateStatHandler([stat_collector])

    for i in range(1, lines + 1):
        # Create line, set its handler and assign to production manager
        p = TrackedLine(
            ProductionLine(i, uniform_gen),
            lambda l: stat_handler.handle_line_free(l)
        )
        production_list.append(p)

    production_mgr = ProductionManager(production_list)
    order_mgr = OrderManager(buffer, production_mgr)
    order_gen = OrderGenerator(poisson_gen, stat_handler, max_orders)

    if verbose:
        stat_handler.add_handler(Logger(client_list, buffer, production_mgr))

    for c in client_list:
        order_gen.run(c, order_mgr)

    start_timestamp = simulated_runtime.timestamp
    await order_gen.wait_all_orders()
    end_timestamp = simulated_runtime.timestamp

    print_clients_table(stat_collector.get_clients_table())
    print_lines_table(
        stat_collector.get_lines_table(end_timestamp - start_timestamp))


if __name__ == "__main__":
    clients = 4
    lines = 5
    buffer_capacity = 10
    lam = 0.14
    a = 8
    b = 10
    max_orders = 2500
    verbose = False

    simulated_runtime.create_task(
        main(clients, lines, buffer_capacity, lam, a, b, max_orders, verbose)
    )
    simulated_runtime.run()
