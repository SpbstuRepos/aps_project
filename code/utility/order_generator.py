from entities.client import Client
from entities.order import Status
from entities.order_manager import OrderManager
from utility.random_generator import RandomGenerator
from utility.runtime import long_wait, sleep
from utility.runtime import simulated_runtime
from utility.statistics_handler import StatCollector


class OrderGenerator:
    def __init__(self, rng: RandomGenerator, stat_collector: StatCollector, max_timestamp: float):
        self._rng = rng
        self._loop = True
        self._stat_collector = stat_collector
        self._orders = []
        self._max_timestamp = max_timestamp

    async def _generate(self, client: Client, order_manager: OrderManager):
        while self._loop:
            time = self._rng.generate()
            await sleep(time)

            if simulated_runtime.timestamp >= self._max_timestamp:
                break

            order = client.create_order(
                lambda o: self._stat_collector.handle_order_status(o)
            )

            self._orders.append(order)
            simulated_runtime.create_task(order_manager.process_request(order))

    def run(self, client: Client, order_manager: OrderManager):
        self._loop = True
        simulated_runtime.create_task(self._generate(client, order_manager))

    async def wait_all_orders(self):
        success = False

        while not success:
            success = True

            for order in self._orders:
                if order.status not in [Status.DROPPED, Status.COMPLETED]:
                    success = False

            await long_wait()
