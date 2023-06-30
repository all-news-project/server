import itertools


def get_cartesian_product(input_list: list) -> list:
    """
    input: [[1,2,3],[11,22,33],[111,222], [1111]]
    output: [
        [(1,11),(1,22),(1,33),(2,11)...],
         ...,
         [(1, 1111), (2, 1111), (3, 1111)],
         [(11,111), (11,222), (22,111)]...,
         [(11, 1111), (22, 1111), (33, 1111)],
         [(111, 1111), (222, 1111)],
    ]

    a:b, a:c, a:d, .... b:d
    :param input_list:
    :return:
    """

    return_list = []
    for a, b in itertools.combinations(input_list, 2):
        return_list.extend(list(itertools.product(a, b)))
    return return_list


def get_permutations(input_list: list) -> list[tuple]:
    """
    input: [[1,2,3],[11,22,33],[111,222]]
    output: [
        (1,2),(1,3),(2,3),
        ...
        ,(111, 222)
    ]
    :param input_list:
    :return:
    """
    output = []
    for v in input_list:
        if len(v) < 2:
            continue
        for a, b in itertools.permutations(v, 2):
            if (b, a) in output:
                continue
            else:
                output.append((a, b))
    return output
