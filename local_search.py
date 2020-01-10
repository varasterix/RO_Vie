import random
import copy
from ordonnancement import Ordonnancement


def local_search(flowshop, sched, iteration):
    nb_local_search_methods = 2
    ls_sched = copy.copy(sched)

    order_of_local_search = [index_method for index_method in range(nb_local_search_methods)]
    random.shuffle(order_of_local_search)

    for index_method in order_of_local_search:
        if index_method == 0:
            ls_sched = local_search_swap(flowshop, ls_sched, iteration)
        elif index_method == 1:
            ls_sched = local_search_insert(flowshop, ls_sched, iteration)
    return ls_sched


def swap(i, j, sched):
    sequence = sched.sequence().copy()
    sequence[i], sequence[j] = sequence[j], sequence[i]
    new_sched = Ordonnancement(sched.nb_machines)
    new_sched.ordonnancer_liste_job(sequence)
    return new_sched

def local_search_swap(flowshop, sched, iteration):
    """
    Returns a new population after local search on an instance of the flowshop population (swap method)
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :return: the population after local search
    """
    nb_jobs = flowshop.nombre_jobs()

    candidate = copy.copy(sched)
    duration = sched.duree()
    duration_candidate = candidate.duree()

    for a in range(0, iteration):
        for i in range(0, nb_jobs - 1):
            for j in range(i + 1, nb_jobs):
                temp = copy.copy(sched)
                ls_swap = swap(i,j,temp)
                duration_temp = ls_swap.duree()
                if (duration_temp < duration_candidate):
                    duration_candidate = duration_temp
                    candidate = ls_swap
        if (duration > duration_candidate):
            sched = candidate
            duration = duration_candidate
        else:
            break
    return sched


def local_search_insert(flowshop, population, iteration):
    """
    Returns a new population after local search on an instance of the flowshop population (insert method)
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :return: the population after local search
    """
    nb_jobs = flowshop.nombre_jobs()
    mutated_population = []

    return population
