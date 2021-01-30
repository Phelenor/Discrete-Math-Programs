import math
import random
import sys
from operator import itemgetter
import numpy as np

ADJ_MATRIX = []     # Adjacency matrix


# Reading the file and forming an adjacency matrix
def read_file():
    global ADJ_MATRIX
    matrix = []

    with open(input("Unesite ime datoteke: ")) as f:
        size = int(f.readline())

        if size == 0:
            print("0")
            sys.exit()

        f.readline()  # skipping an empty line

        for i in range(size):
            matrix.append([int(x) for x in f.readline().rstrip().split(sep=" ")])

    ADJ_MATRIX = np.array(matrix)


# Removing the isolated vertices from the
# adjacency matrix - simplifying the search
def reduce_matrix():
    global ADJ_MATRIX
    reducible = True

    while reducible:
        reducible = False

        for row in range(len(ADJ_MATRIX)):
            if (len(ADJ_MATRIX)) <= row:
                break
            elif np.sum(ADJ_MATRIX[row]) == 0:
                reducible = True
                ADJ_MATRIX = np.delete(ADJ_MATRIX, row, 0)
                ADJ_MATRIX = np.delete(ADJ_MATRIX, row, 1)


# Finding the minimal number of colors to color the
# graph by starting the traversal from every vertex
# and continuing to it's adjacent vertices and so on
# until every vertex is colored
def find_chromatic_number_traversal():
    if len(ADJ_MATRIX) == 0:
        return 1

    chromatic_num = 99
    vertex_num = 0

    for i in range(len(ADJ_MATRIX)):
        color_list = np.array(np.zeros(len(ADJ_MATRIX), dtype=int))
        color_list[i] = 1
        last_colored = i
        vertex_counter = 0

        queue = []
        queue.extend(enqueue_adjacent(i, last_colored))

        while 0 in color_list:
            if len(queue) == 0:
                break
            vertex = queue.pop(0)
            if color_list[vertex] != 0:
                continue
            vertex_counter += 1
            colors_available = [int(i) for i in range(1, len(color_list) + 1)]
            for j in range(len(ADJ_MATRIX)):
                if vertex == j:
                    continue

                if ADJ_MATRIX[vertex][j] == 1 and color_list[j] != 0:
                    if color_list[j] in colors_available:
                        colors_available.remove(color_list[j])

            color_list[vertex] = min(colors_available)
            queue.extend(enqueue_adjacent(vertex, last_colored))
            last_colored = vertex

        if max(color_list) < chromatic_num and vertex_counter >= vertex_num:
            vertex_num = vertex_counter
            chromatic_num = max(color_list)

    return chromatic_num


# Creating the orders for the graph traversal
def make_orders():
    orders = []

    # Simple order: 0, 1, 2, 3, ... , n
    simple_order = [i for i in range(len(ADJ_MATRIX))]
    orders.append(simple_order)

    # Degree based order
    degree_list = sorted([[np.sum(ADJ_MATRIX[row]), row] for row in range(len(ADJ_MATRIX))], key=itemgetter(0))
    degree_list = [row[1] for row in degree_list]
    orders.append(degree_list)

    # Degree list shuffles
    for i in range(1, len(ADJ_MATRIX)):
        orders.append(list(degree_list[i:] + degree_list[:i]))

    # Adding the random orders
    for i in range(1000 * math.floor(math.sqrt(len(ADJ_MATRIX)))):
        simple_copy = list.copy(simple_order)
        degree_copy = list.copy(degree_list)
        random.shuffle(simple_copy)
        random.shuffle(degree_copy)
        orders.append(simple_copy)
        orders.append(degree_copy)

    return orders


# Finding the minimal number of colors to color the
# graph by visiting the vertices in certain orders
# -> random, simple and degree based shuffles
def find_chromatic_number_random():
    if len(ADJ_MATRIX) == 0:
        return 1

    chromatic_num = 99
    orders = make_orders()
    vertex_num = 0

    for order in orders:
        queue = order
        color_list = np.array(np.zeros(len(ADJ_MATRIX), dtype=int))
        color_list[queue.pop(0)] = 1
        vertex_counter = 0

        while 0 in color_list:
            vertex = queue.pop(0)
            if color_list[vertex] != 0:
                continue
            vertex_counter += 1
            colors_available = [int(i) for i in range(1, len(color_list) + 1)]
            for j in range(len(ADJ_MATRIX)):
                if vertex == j:
                    continue

                if ADJ_MATRIX[vertex][j] == 1 and color_list[j] != 0:
                    if color_list[j] in colors_available:
                        colors_available.remove(color_list[j])

            color_list[vertex] = min(colors_available)

        if max(color_list) < chromatic_num and vertex_counter >= vertex_num:
            vertex_num = vertex_counter
            chromatic_num = max(color_list)

    return chromatic_num


# Enqueuing the adjacent vertices for the traversal
def enqueue_adjacent(vertex, exclude):
    queue = []
    for j in range(len(ADJ_MATRIX)):
        if ADJ_MATRIX[vertex][j] == 1 and j != exclude:
            queue.append(j)
    return queue


def main():

    # Reading the adjacency matrix from text file
    read_file()
    reduce_matrix()
    # Choosing the minimal number of colors needed to color the graph
    chromatic_num = min(find_chromatic_number_traversal(), find_chromatic_number_random())
    print(chromatic_num)


if __name__ == '__main__':
    main()
