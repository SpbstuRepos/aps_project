from utility.stat_handlers.stat_handler import StatHandler
from utility.substitutes import TrackedLine, TrackedOrder


class Logger(StatHandler):
    def __init__(self):
        super().__init__()

    def handle_order_status(self, order: TrackedOrder):
        pass

    def handle_line_free(self, line: TrackedLine):
        pass
