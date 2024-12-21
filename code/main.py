from entities.buffer import Buffer
from entities.client import Client
from entities.order_manager import OrderManager
from entities.production_line import ProductionLine
from entities.production_manager import ProductionManager
from utility.order_generator import OrderGenerator
from utility.random_generator import PoissonGenerator, UniformGenerator
from utility.runtime import simulated_runtime, yield_task, sleep
from utility.statistics_handler import StatCollector


async def main(clients: int, lines: int, buffer_capacity: int, lam: int,
               a: int, b: int, duration: float):
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
    """

    poisson_gen = PoissonGenerator(lam)
    uniform_gen = UniformGenerator(a, b)
    production_list = []
    stat_collector = StatCollector()

    for i in range(1, lines + 1):
        # Create line, set its handler and assign to production manager
        p = ProductionLine(
            i,
            uniform_gen,
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

    await sleep(duration)
    await order_gen.wait_all_orders()

    stat_collector.get_clients_table()
    stat_collector.get_lines_table()
    print(simulated_runtime.timestamp)

if __name__ == "__main__":
    clients = 5
    lines = 3
    buffer_capacity = 100
    lam = 0.14
    a = 5
    b = 10
    duration = 1000

    simulated_runtime.create_task(
        main(clients, lines, buffer_capacity, lam, a, b, duration)
    )
    simulated_runtime.run()
