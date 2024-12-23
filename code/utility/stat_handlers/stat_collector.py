from entities.order import Status
from utility.runtime import simulated_runtime
from utility.stat_handlers.stat_handler import StatHandler
from utility.substitutes import TrackedLine, TrackedOrder


class StatCollector(StatHandler):
    def __init__(self):
        super().__init__()

        self._lines = {}
        self._clients = {}
        self._orders = []

    def handle_order_status(self, order: TrackedOrder):
        client_id = order.issuer.id

        # Stats : (total, completed, dropped)
        stats = self._clients.get(client_id, (0, 0, 0))

        if order.status == Status.CREATED:
            stats = (stats[0] + 1, stats[1], stats[2])
            order.created_at = simulated_runtime.timestamp
            order.extracted_at = simulated_runtime.timestamp
            self._orders.append(order)

        elif order.status == Status.QUEUED:
            order.was_bufferized = True

        elif order.status == Status.PROCESSING:
            if order.was_bufferized:
                order.extracted_at = simulated_runtime.timestamp

        elif order.status == Status.COMPLETED:
            stats = (stats[0], stats[1] + 1, stats[2])
            order.finalized_at = simulated_runtime.timestamp

        elif order.status == Status.DROPPED:
            stats = (stats[0], stats[1], stats[2] + 1)
            order.finalized_at = simulated_runtime.timestamp

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

    def get_lines_table(self, total_time):
        table = []

        for k, v in self._lines.items():
            table.append([str(k), v[0], 100 * v[0] / total_time])

        return table

    def get_clients_table(self):
        table = []

        for k, v in self._clients.items():
            row = [
                str(k), v[0],
                v[1], 100 * v[1] / v[0],
                v[2], 100 * v[2] / v[0],
                0, 0,
                0, 0,
                0, 0
            ]

            client_orders = list(
                filter(lambda o: o.issuer.id == k and o.status ==
                       Status.COMPLETED, self._orders)
            )

            row[6], row[7] = self.get_avg_and_disp(
                map(lambda o: o.finalized_at - o.created_at, client_orders)
            )

            row[8], row[9] = self.get_avg_and_disp(
                map(lambda o: o.extracted_at - o.created_at, client_orders)
            )

            row[10], row[11] = self.get_avg_and_disp(
                map(lambda o: o.finalized_at - o.extracted_at, client_orders)
            )

            table.append(row)

        t_totl, t_comp, t_drop = (
            sum(i for _, (i, _, _) in self._clients.items()),
            sum(i for _, (_, i, _) in self._clients.items()),
            sum(i for _, (_, _, i) in self._clients.items()),
        )

        row = [
            "System", t_totl,
            t_comp, 100 * t_comp / t_totl,
            t_drop, 100 * t_drop / t_totl,
            0, 0,
            0, 0,
            0, 0
        ]

        completed_orders = list(
            filter(lambda o: o.status == Status.COMPLETED, self._orders)
        )

        row[6], row[7] = self.get_avg_and_disp(
            map(lambda o: o.finalized_at - o.created_at, completed_orders)
        )

        row[8], row[9] = self.get_avg_and_disp(
            map(lambda o: o.extracted_at - o.created_at, completed_orders)
        )

        row[10], row[11] = self.get_avg_and_disp(
            map(lambda o: o.finalized_at - o.extracted_at, completed_orders)
        )

        table.append(row)
        return table

    def get_avg_and_disp(self, sequence):
        count = 0
        summ = 0
        summ2 = 0

        for item in sequence:
            count += 1
            summ += item
            summ2 += item * item

        avg = summ / count
        avg2 = summ2 / count
        return avg, avg2 - avg*avg
