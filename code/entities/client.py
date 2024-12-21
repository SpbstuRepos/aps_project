from entities.order import Order


class Client:
    # id: int

    def __init__(self, id: int):
        self._id = id
        self._counter = 0

    @property
    def id(self):
        return self._id

    def create_order(self):
        return self.create_order(None)

    def create_order(self, status_update_handler):
        self._counter += 1
        order_id = self._counter * 100 + self._id
        return Order(order_id, self._id, self, status_update_handler)

    def notify_completed(self, order: Order):
        pass
