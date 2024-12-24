from operator import attrgetter
from entities.order import Order
from entities.production_line import ProductionLine


class ProductionManager:
    # lines: list[ProductionLine]

    def __init__(self, lines: list[ProductionLine]):
        self._lines = list(sorted(lines, key=attrgetter('id')))

    def is_line_available(self):
        return any(map(lambda line: line.is_free(), self._lines))

    async def process_request(self, order: Order) -> Order:
        free_line = next(
            filter(lambda line: line.is_free(), self._lines),
            None
        )

        if free_line == None:
            raise Exception("No available production lines")

        return await free_line.process_request(order)
