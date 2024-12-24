from entities.buffer import Buffer
from entities.client import Client
from entities.order import Status
from entities.production_manager import ProductionManager
from utility.printer import fmt_buffer, fmt_clients, fmt_order, fmt_prod_manager
from utility.stat_handlers.stat_handler import StatHandler
from utility.substitutes import TrackedLine, TrackedOrder
from utility.runtime import simulated_runtime


class Logger(StatHandler):
    def __init__(self, clients: list[Client], buffer: Buffer,
                 prod: ProductionManager):
        super().__init__()

        self._buffer = buffer
        self._prod = prod
        self._fill_clients(clients)

    def _fill_clients(self, clients: list[Client]):
        self._clients = {}

        for client in sorted(clients, key=lambda o: o.id):
            self._clients[client.id] = [0, 0.0]

    def handle_order_status(self, order: TrackedOrder):
        if order.status == Status.CREATED:
            # Заявка сгенерирована и отправлена на обработку
            self._clients[order.issuer.id][0] += 1
            self.log_created(order)
        elif order.status == Status.QUEUED:
            # Заявка отправлена в буфер
            self.log_buffered(order)
        elif order.status == Status.DROPPED:
            # Выбивание заявки из буфера
            self._clients[order.issuer.id][1] += 1
            self.log_dropped(order)
        elif order.status == Status.PROCESSING:
            # Заявка отправлена на прибор, возможно еще извлечена из буфера

            if order.was_bufferized:
                self.log_selected(order)

            self.log_started_processing(order)
        elif order.status == Status.COMPLETED:
            # Заявка обработана
            self.log_completed(order)

    def handle_line_free(self, line: TrackedLine):
        pass

    def log_created(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(
            f'[{t:.2f}] Order {fmt_order(order)} was created and sent to OrderManager')
        print(f'Client list:\n{fmt_clients(self._clients)}\n\n')

    def log_buffered(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(f'[{t:.2f}] Order {fmt_order(order)} was placed into Buffer')
        print(f'Buffer state:\n{fmt_buffer(self._buffer)}\n\n')

    def log_dropped(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(f'[{t:.2f}] Order {fmt_order(order)} was removed from Buffer')
        print(f'Buffer state:\n{fmt_buffer(self._buffer)}\n')
        print(f'Client list:\n{fmt_clients(self._clients)}\n\n')

    def log_selected(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(f'[{t:.2f}] Order {fmt_order(order)} was selected from Buffer')
        print(f'Buffer state:\n{fmt_buffer(self._buffer)}\n\n')

    def log_started_processing(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(f'[{t:.2f}] Order {fmt_order(order)} was passed to ProductionLine')
        print(f'Production lines state:\n{fmt_prod_manager(self._prod)}\n\n')

    def log_completed(self, order: TrackedOrder):
        t = simulated_runtime.timestamp
        print(f'[{t:.2f}] Order {fmt_order(order)} was completed')
        print(f'Production lines state:\n{fmt_prod_manager(self._prod)}\n\n')
