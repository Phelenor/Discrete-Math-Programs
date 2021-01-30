import numpy as np
from operator import itemgetter

EDGES = []
CYCLES = []
LENGTH_LIST = []
SIZE = 0


def read_file():
    matrix = []

    with open(input("Unesite ime datoteke: ")) as f:
        size = int(f.readline())
        f.readline()  # skipping an empty line

        for i in range(size):
            matrix.append([int(x) for x in f.readline().rstrip().split(sep=" ")])

    return matrix


def reduce_matrix(matrix):
    reducible = True

    while reducible:
        reducible = False

        for row in range(len(matrix)):
            if (len(matrix)) >= row:
                break
            elif np.sum(matrix[row]) <= 1:
                reducible = True
                matrix = np.delete(matrix, row, 0)
                matrix = np.delete(matrix, row, 1)

    return matrix


def edge_list(adj_matrix):
    global EDGES

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                EDGES.append(sorted((i + 1, j + 1)))

    EDGES = list(set(tuple(e) for e in EDGES))
    return EDGES


# Checking cycle - can remove
def cycle_to_list(path):
    global CYCLES
    n = path.index(min(path))   # Cycle starts from the smallest vertex
    p1 = path[n:] + path[:n]

    p2 = list(p1)[::-1]         # Invert the vertex - checking that we didn't count
    n = p2.index(min(p2))       # it from both angles
    p2 = p2[n:] + p2[:n]

    if (p1 not in CYCLES) and (p2 not in CYCLES):
        CYCLES.append(p1)


def find_cycles(path):
    global EDGES
    global LENGTH_LIST
    global SIZE

    start_v = path[0]

    for edge in EDGES:
        v1, v2 = edge

        if start_v in edge:
            next_v = v2 if (start_v == v1) else v1  # Next vertex on the path

            if next_v not in path:  # Checking if we are returning
                sub_path = [next_v]  # to origin vertex
                sub_path.extend(path)
                find_cycles(sub_path)
            elif len(path) > 2 and next_v == path[-1]:  # Stop when sub-path returns to it's
                LENGTH_LIST.append(len(path))           # origin => cycle

                cycle_to_list(path)

                if len(path) == SIZE:
                    return                      # Stop the search if we find a Hamilton cycle


def find_longest_cycle():
    global EDGES
    checked = []

    for edge in EDGES:
        for vertex in edge:
            if vertex not in checked:
                checked.append(vertex)
                find_cycles([vertex])

    return max(LENGTH_LIST) if len(LENGTH_LIST) != 0 else 0


def main():
    global EDGES
    global SIZE
    global CYCLES

    adj_matrix = np.array(read_file())  # Reading the adjacency matrix from text file
    adj_matrix = reduce_matrix(adj_matrix)  # Removing the vertices than can't make up cycles (deg(v) <= 1)
    SIZE = len(adj_matrix)

    EDGES = sorted(edge_list(adj_matrix), key=itemgetter(0))  # Converting the graph to edge list form

    print(find_longest_cycle())

    CYCLES.sort(key=len, reverse=True)
    if len(CYCLES) > 0:
        print(CYCLES[0])       # Print the longest cycle


if __name__ == '__main__':
    main()
