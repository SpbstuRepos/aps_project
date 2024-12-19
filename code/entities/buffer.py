from entities.order import Order, Status


class Buffer:
    # capacity: int
    # count: int
    # orders: list[Order]
    # place_index: int

    def __init__(self, capacity: int):
        assert capacity >= 0
        self._capacity = capacity
        self._count = 0
        self._orders = [None] * capacity
        self._place_index = 0

    def is_empty(self):
        return self._count == 0

    def __is_full(self):
        return self._count == self._capacity

    def __pop(self, index):
        item = self._orders[index]
        self._orders[index] = None

        if item != None:
            self._count -= 1

        return item

    def remove_under_cursor(self):
        order = self.__pop(self._place_index)

        if order != None:
            order.status = Status.DROPPED

    def add_request(self, order):
        if self.__is_full():
            self.remove_under_cursor()

        while True:
            if self._orders[self._place_index] == None:
                self._orders[self._place_index] = order
                break

            self._place_index += 1

        order.status = Status.QUEUED
        self._place_index += 1

    def take_request(self) -> Order:
        best_index = 0

        for i in range(1, self._orders):
            order = self._orders[i]
            best_order = self._orders[best_index]

            if best_order == None:
                best_index = i
            elif order != None and order.priority < best_order.priority:
                best_index = i

        return self.__pop(best_index)
