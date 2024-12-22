from prettytable import PrettyTable as Table


def print_clients_table(table):
    t = Table(["Client ID", "Total Orders", "Completed (total)",
              "Completed (%)", "Dropped (total)", "Dropped (%)"])
    t.add_rows(sorted((i, t, c, "%.2f" % (100 * c / t), d, "%.2f" % (100 * d / t))
               for i, (t, c, d) in table))

    t_id, t_totl, t_comp, t_drop = (
        "Total",
        sum(i for _, (i, _, _) in table),
        sum(i for _, (_, i, _) in table),
        sum(i for _, (_, _, i) in table),
    )

    t.add_row((t_id, t_totl,
               t_comp, "%.2f" % (100 * t_comp / t_totl),
               t_drop, "%.2f" % (100 * t_drop / t_totl)
               ))

    t._dividers[len(table) - 1] = True
    print(f'Orders grouped by clients report\n{t}\n')


def print_lines_table(table, total_time):
    t = Table(["Production Line ID", "Total work time", "Load (%)"])
    t.add_rows(sorted((i, "%.2f" % l, "%.2f" % (100 * l / total_time))
                      for i, (l, _) in table))

    print(f'Production lines activity report\n{t}\n')
