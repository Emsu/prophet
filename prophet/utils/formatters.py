from six import iteritems


def dict_to_table(_dict):
    col_width_keys = max([len(key) for key in _dict.keys()])
    col_width_values = max([len(str(value)) for value in _dict.values()])
    table_end_str = ("+-" + (col_width_keys +
                             col_width_values + 3) * "-" + "-+")
    data_strs = []
    for key, value in iteritems(_dict):
        data_strs.append("| " + " | ".join([
            "{:{}}".format(key, col_width_keys),
            "{:{}}".format(value, col_width_values)]) + " |\n")
    return "%s\n%s%s" % (table_end_str, "".join(data_strs), table_end_str)
