from entities.order import Order, Status
from utility.random_generator import RandomGenerator
from utility.runtime import sleep


class ProductionLine:
    # id: int
    # free: bool

    def __init__(self, id: int, rng: RandomGenerator, free_update_handler=None):
        self._id = id
        self._free_update_handler = free_update_handler
        self._free_ = True
        self._rng = rng

    @property
    def free_update_handler(self):
        return self._free_update_handler

    @free_update_handler.setter
    def free_update_handler(self, value):
        self._free_update_handler = value

    def is_free(self):
        return self._free_

    @property
    def _free(self):
        return self._free_

    @_free.setter
    def _free(self, value):
        self._free_ = value

        if self.free_update_handler != None:
            self.free_update_handler(self)

    @property
    def id(self):
        return self._id

    async def _process_internal(self):
        time = self._rng.generate()
        await sleep(time)

    async def process_request(self, order: Order) -> Order:
        if not self._free:
            raise Exception("Attempt to load nonfree line")

        self._free = False
        order.status = Status.PROCESSING
        await self._process_internal()
        self._free = True
        order.status = Status.COMPLETED

        return order
