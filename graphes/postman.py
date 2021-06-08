
import random
import numpy as np

def can_euler(matrix, s):
    for line in matrix:
        if sum(list(map(lambda n: n[0], line))) <= s / 2: return False
    return True

def random_graphe(size):
    b = np.random.choice((True, False), size=(size,size), p=[0.4, 0.6])
    b_symm = np.logical_or(b, b.T)
    matrix = b_symm.astype(int)
    matrix = list(map(lambda line: list(map((lambda n: [0,0] if n == 0 else [1,0]), line)), matrix))
    for k, line in enumerate(matrix):
        for j, col in enumerate(line):
            if col != [1,0]: continue
            number = random.randint(1,15)
            matrix[k][j] = [1,number]
            matrix[j][k] = [1,number]
    return matrix

def operation_on_matrix(matrix, current, index, operation):
    if current == index:
        matrix[current][index][0] += operation
    else:
        matrix[current][index][0] += operation
        matrix[index][current][0] += operation
    return matrix

def euler_cycle(matrix, stack, current, passed):
    print(len(stack), " - ", len(passed))
    print('test')
    for i in range(len(matrix)):
        if matrix[current][i][0] >= 1:
            stack.append(current)
            matrix = operation_on_matrix(matrix, current, i, -1)
            if current not in passed and sum(list(map(lambda n: n[0], matrix[current]))) == 0 : passed.append(current)
            if i not in passed and len(passed) == len(matrix) - 1 and sum(list(map(lambda n: n[0], matrix[i]))) == 0 :
                passed.append(i)
                stack.append(i)
            #print("index : ", i, " | curr : ", current)
            #print("passed : ", passed)
            print('test2')
            if euler_cycle(matrix, stack, i, passed):
                print('test25')
                return stack
            else:
                print('test27')
                matrix = operation_on_matrix(matrix, i, stack[-1], 1)
                if current in passed: passed.remove(current)
                current = stack[-1]
                del stack[-1]
    print('test3')
    if len(passed) != len(matrix): return False
    return stack

def to_euler(matrix):
    #for line in matrix: print(line)
    not_pair = []
    for index, line in enumerate(matrix):
        nodes,weights = zip(*line)
        if (sum(nodes) + nodes[index]) % 2 != 0:
            not_pair.append(index)
    for index in range(0, len(not_pair), 2):
        print("\n", not_pair[index], " - ", not_pair[index + 1], "\n")
        path = dijkstra(matrix, not_pair[index], not_pair[index + 1], [], {})
        print(path, "\n")
        current = not_pair[index + 1]
        while current != not_pair[index]:
            matrix = operation_on_matrix(matrix, current, path[current][0], 1)
            current = path[current][0]
    #for line in matrix: print(line)



def dijkstra(matrix, node_a, node_b, links, total):
    """
    :param matrix: la matrice
    :param node_a: le noeud actuel
    :param node_b: le noeud final
    :param links: les liens
    :param total: les liens "valides"
    :return: le chemin
    """

    for link in links:
        if link[1] in total:
             links.remove(link)

    for index, node in enumerate(matrix[node_a]):
        if node[0] >= 1 and index != node_a:
            if node_a in total:
                if index == total[node_a][0]:
                    continue
                links.append([node_a, index, node[1] + total[node_a][1]])
            else:
                #print("node : ",node_a, "index : ",index, "noeud :", node)
                links.append([node_a, index, node[1]])

    fr,to,we = zip(*links)
    min_link = links[we.index(min(we))]
    #print("links : ", len(links), " total : ", len(total))
    total[min_link[1]] = [min_link[0], min_link[2]]
    if node_b not in total:
        total = dijkstra(matrix, min_link[1], node_b, links, total)
    return total


if __name__ == "__main__":
    # execute only if run as a script
    size = 100

    m = random_graphe(size)
    while not can_euler(m, size):
        m = random_graphe(size)
    to_euler(m)

    print('DEBUT EULER.')
    r = euler_cycle(m, [], 0, [])
    print(r)
    print('FIN EULER.')




