from entities.order import Order, Status
from utility.random_generator import RandomGenerator
from utility.runtime import sleep


class ProductionLine:
    # id: int
    # free: bool

    def __init__(self, id: int, rng: RandomGenerator):
        self._id = id
        self._free = True
        self._rng = rng

    def is_free(self):
        return self._free

    @property
    def id(self):
        return self._id

    async def _process_internal(self):
        time = self._rng.generate()
        await sleep(time)

    async def process_request(self, order: Order) -> Order:
        self._free = False
        order.status = Status.PROCESSING
        await self._process_internal()
        self._free = True
        order.status = Status.COMPLETED

        return order
