def knapsack(items, s):
    items_len = len(items)
    x_values = [0] * items_len

    for index in reversed(range(items_len)):
        if s >= items[index]:
            x_values[index] = 1
            s = s - items[index]

    return x_values