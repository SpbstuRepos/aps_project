from entities.order import Order, Status


class ProductionLine:
    # id: int
    # free: bool

    def __init__(self, id: int):
        self._id = id
        self._free = True

    def is_free(self):
        return self._free

    @property
    def id(self):
        return self._id

    def process_request(self, order: Order) -> Order:
        self._free = False
        order.status = Status.PROCESSING
        # TODO: Wait
        self._free = True
        order.status = Status.COMPLETED

        return order
