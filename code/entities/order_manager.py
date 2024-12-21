from entities.buffer import Buffer
from entities.client import Client
from entities.order import Order
from entities.production_manager import ProductionManager
from utility.runtime import yield_task


class OrderManager:
    # buffer: Buffer
    # production_manager: ProductionManager

    def __init__(self, buffer: Buffer, production_manager: ProductionManager):
        self._buffer = buffer
        self._production_manager = production_manager
        self._is_processing_buffer = False

    async def process_request(self, order: Order):
        if self._production_manager.is_line_available():
            processed = await self._production_manager.process_request(order)
            self._notify_client(processed)
        else:
            self._buffer.add_request(order)
            await self.process_buffer()

    async def wait_line(self):
        while not self._production_manager.is_line_available():
            await yield_task()

    async def process_buffer(self):
        if self._is_processing_buffer == True:
            return

        self._is_processing_buffer = True

        while not self._buffer.is_empty():
            await self.wait_line()
            order = self._buffer.take_request()
            processed = await self._production_manager.process_request(order)
            self._notify_client(processed)

        self._is_processing_buffer = False

    def _notify_client(self, order: Order):
        client: Client = order.issuer
        client.notify_completed(order)
