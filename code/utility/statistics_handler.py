from entities.order import Status
from utility.runtime import simulated_runtime
from utility.substitutes import TrackedLine, TrackedOrder


class StatCollector:
    def __init__(self):
        self._lines = {}
        self._clients = {}

    def handle_order_status(self, order: TrackedOrder):
        client_id = order.issuer.id

        # Stats : (total, completed, dropped)
        stats = self._clients.get(client_id, (0, 0, 0))

        if order.status == Status.CREATED:
            stats = (stats[0] + 1, stats[1], stats[2])
        elif order.status == Status.COMPLETED:
            stats = (stats[0], stats[1] + 1, stats[2])
        elif order.status == Status.DROPPED:
            stats = (stats[0], stats[1], stats[2] + 1)

        self._clients[client_id] = stats

    def handle_line_free(self, line: TrackedLine):
        line_id = line.id

        # Line stat: (total load time, last busy call time)
        stats = self._lines.get(line_id, (0, None))
        now = simulated_runtime.timestamp

        if line.is_free() and stats[1] != None:
            busy_time = now - stats[1]
            stats = (stats[0] + busy_time, stats[1])
        elif not line.is_free():
            stats = (stats[0], now)

        self._lines[line_id] = stats

    def get_lines_table(self):
        return self._lines.items()

    def get_clients_table(self):
        return self._clients.items()
