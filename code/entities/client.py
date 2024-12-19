from entities.order import Order


class Client:
    # id: int

    def __init__(self, id: int):
        self._id = id
        self._counter = 0

    def create_order(self):
        self._counter += 1
        order_id = self._counter * 100 + self._id
        return Order(order_id, self._id, self)

    def notify_completed(order: Order):
        pass  # TODO: Handle completed order
