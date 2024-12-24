from entities.order import Order
from entities.production_line import ProductionLine


class TrackedOrder(Order):
    def __init__(self, order: Order, status_update_handler=None):
        self.status_update_handler = status_update_handler
        self.created_at = 0.0
        self.was_bufferized = False
        self.extracted_at = 0.0
        self.finalized_at = 0.0

        super().__init__(order.id, order.priority, order.issuer)

    @Order.status.setter
    def status(self, value):
        Order.status.fset(self, value)

        if self.status_update_handler != None:
            self.status_update_handler(self)


class TrackedLine(ProductionLine):
    def __init__(self, line: ProductionLine, free_update_handler=None):
        self._free_update_handler = None
        super().__init__(line.id, line._rng)

        self._free_update_handler = free_update_handler

    @property
    def free_update_handler(self):
        return self._free_update_handler

    @free_update_handler.setter
    def free_update_handler(self, value):
        self._free_update_handler = value

    @ProductionLine._free.setter
    def _free(self, value):
        ProductionLine._free.fset(self, value)

        if self.free_update_handler != None:
            self.free_update_handler(self)
