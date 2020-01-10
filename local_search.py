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
    sched.sequence()[i], sched.sequence()[j] = sched.sequence()[j], sched.sequence()[i]


def local_search_swap(flowshop, sched, iteration):
    """
    Returns a new population after local search on an instance of the flowshop population (swap method)
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :return: the population after local search
    """
    nb_jobs = flowshop.nombre_jobs()

    candidat = copy.copy(sched)
    duree = sched.duree()
    duree_candidat = candidat.duree()

    a = 0
    stop = False

    while stop == False or a < iteration:
        a = a + 1
        for i in range(0, nb_jobs - 2):
            for j in range(i + 1, nb_jobs - 1):
                provisoire = copy.copy(sched)
                swap(i, j, provisoire)
                duree_provisoire = provisoire.duree()
                if (duree_provisoire < duree_candidat):
                    duree_candidat = duree_provisoire
                    candidat = provisoire
        if (duree > duree_candidat):
            stop = False
            duree = duree_candidat
            sched = candidat
        else:
            stop = True
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
