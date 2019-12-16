import copy
import random


def random_initial_pop(flow_shop, nb_value):
    """
    Generates randomly the initial population
    :param flow_shop: an instance of the flow shop permutation problem
    :param nb_value: number of element in the initial population to generate
    :return population: the initial population for the memetic algorithm
    """
    population = []
    start = [i for i in range(flow_shop.nb_machines)]
    for i in range(nb_value):
        random.shuffle(start)
        elem = copy.copy(start)
        population.append(elem)
    return population
