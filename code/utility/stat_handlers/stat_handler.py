from utility.substitutes import TrackedLine, TrackedOrder


class StatHandler:
    def handle_order_status(self, order: TrackedOrder):
        raise NotImplementedError()

    def handle_line_free(self, line: TrackedLine):
        raise NotImplementedError()


class AggregateStatHandler(StatHandler):
    def __init__(self, handlers: list[StatHandler]):
        super().__init__()
        self._handlers = list(handlers)

    def add_handler(self, handler: StatHandler):
        self._handlers.append(handler)

    def handle_order_status(self, order: TrackedOrder):
        for handler in self._handlers:
            handler.handle_order_status(order)

    def handle_line_free(self, line: TrackedLine):
        for handler in self._handlers:
            handler.handle_line_free(line)
