from prettytable import PrettyTable as Table


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


def print_lines_table(table, total_time):
    t = Table(["Production Line ID", "Total work time", "Load (%)"])
    t.add_rows(sorted((i, "%.2f" % l, "%.2f" % (100 * l / total_time))
                      for i, (l, _) in table))

    print(f'Production lines activity report\n{t}\n')
