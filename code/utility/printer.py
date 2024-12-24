from prettytable import PrettyTable as Table
from entities.buffer import Buffer
from entities.order import Order
from entities.production_manager import ProductionManager


def print_clients_table(table):
    t = Table(["Client ID", "Total Orders", "Completed (total)",
              "Completed (%)", "Dropped (total)", "Dropped (%)",
               "Total time (avg)", "Total time (disp)",
               "Buffer time (avg)", "Buffer time (disp)",
               "Prod time (avg)", "Prod time (disp)"])

    t.add_rows(sorted((
        t_id, t_totl,
        t_comp, "%.2f" % t_comp2,
        t_drop, "%.2f" % t_drop2,
        "%.3f" % avg_time, "%.3f" % disp_time,
        "%.3f" % avg_buf, "%.3f" % disp_buf,
        "%.3f" % avg_prod, "%.3f" % disp_prods)
        for t_id, t_totl, t_comp, t_comp2,
        t_drop, t_drop2, avg_time, disp_time,
        avg_buf, disp_buf, avg_prod, disp_prods in table))

    t._dividers[len(table) - 2] = True
    print(f'Orders grouped by clients report\n{t}\n')


def print_lines_table(table):
    t = Table(["Production Line ID", "Total work time", "Load (%)"])
    t.add_rows(sorted((i, "%.2f" % l, "%.2f" % lf) for i, l, lf in table))
    print(f'Production lines activity report\n{t}\n')


def fmt_order(order: Order):
    if order != None:
        return f'(id={order.id} created by client #{order.issuer.id})'
    else:
        return '-----'


def fmt_buffer(buffer: Buffer):
    t = Table(["Index", "Order"])

    for i in range(len(buffer._orders)):
        index = str(i) if buffer._place_index != i else f'-> {i}'
        order = fmt_order(buffer._orders[i])
        t.add_row((index, order))

    return f'{t}'


def fmt_prod_manager(prod: ProductionManager):
    t = Table(["Line ID", "Order"])

    for line in prod._lines:
        index = line.id
        order = fmt_order(line._order)
        t.add_row((index, order))

    return f'{t}'


def fmt_clients(clients):
    t = Table(["Line ID", "Order count", "Dropped (%)"])

    for k, v in clients.items():
        index = k
        orders = v[0]
        dropped = '%.2f' % ((100 * v[1] / v[0]) if v[0] != 0 else 0.0)
        t.add_row((index, orders, dropped))

    return f'{t}'
