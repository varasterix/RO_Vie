import math


def initialize_threshold(pop_init_size):
    if pop_init_size < 200:
        entropy_threshold = 5.7
    elif pop_init_size < 300:
        entropy_threshold = 7
    elif pop_init_size < 400:
        entropy_threshold = 7.8
    elif pop_init_size < 500:
        entropy_threshold = 8.4
    else:
        entropy_threshold = 8.7
    return entropy_threshold


def shannon_entropy(population):
    """
    calculates the shannon entropy of the population
    :param population: list of schedulings (Ordonnancement objects)
    :return: shannon entropy of the population
    """
    entropy = 0
    distinct_sched = []
    for sched in population:
        if sched not in distinct_sched:
            distinct_sched.append(sched)
            pi = population.count(sched) / len(population)
            entropy -= pi * math.log(pi, 2)
    return entropy


def is_convergent(population, threshold):
    """
    checks the convergence of the population
    :param population: list of schedulings (Ordonnancement objects)
    :param threshold: threshold of entropy
    :return: True if the entropy is lesser than the threshold and False if it is not
    """
    return shannon_entropy(population) < threshold

