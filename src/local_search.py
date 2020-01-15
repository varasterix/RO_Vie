import copy
import random
from src.ordonnancement import Ordonnancement


def local_search(flowshop, population, maximum_nb_iterations, max_neighbors_nb, local_search_swap_prob, local_search_insert_prob):
    """
    Generates a new population by improving each scheduling with a local search method during the given maximum number
    of iterations
    :param flowshop: a Flowshop object
    :param population: population of schedulings to improve with local search
    :param maximum_nb_iterations: maximum number of iterations (explorations of a neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :param local_search_swap_prob: probability of using the swap local search for a scheduling in the population
    :param local_search_insert_prob: probability of using the insert local search for a scheduling in the population
    :return: new population after local search improvements
    """
    sum_prob = local_search_swap_prob + local_search_insert_prob
    local_search_swap_prob /= sum_prob
    local_search_insert_prob /= sum_prob
    new_population = []
    for scheduling in population:
        method_random = random.random()
        new_scheduling = local_search_swap(flowshop, scheduling, maximum_nb_iterations, max_neighbors_nb) \
            if method_random < local_search_swap_prob \
            else local_search_insert(flowshop, scheduling, maximum_nb_iterations, max_neighbors_nb)
        new_population.append(new_scheduling)
    return new_population


def swap(i, j, scheduling):
    sequence = scheduling.sequence().copy()
    sequence[i], sequence[j] = sequence[j], sequence[i]
    new_scheduling = Ordonnancement(scheduling.nb_machines)
    new_scheduling.ordonnancer_liste_job(sequence)
    return new_scheduling


def local_search_swap(flowshop, scheduling, iteration, max_neighbors_nb):
    """
    Returns a (new) scheduling after local search on the given initial scheduling during the maximum number of
    iterations given to find a minimum local, given an instance of the flowshop population (swap neighborhood)
    An iteration is an exploration of all the swap neighborhood of the current best scheduling
    :param flowshop: a Flowshop object
    :param scheduling: a scheduling (Ordonnancement object)
    :param iteration: maximum number of iterations (explorations of the swap neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :return: the scheduling after the given number of iteration of local search
    """
    nb_jobs = flowshop.nombre_jobs()

    candidate = copy.copy(scheduling)
    duration = scheduling.duree()
    duration_candidate = candidate.duree()
    neighbors = []
    for i in range(nb_jobs-1):
        for j in range(i, nb_jobs):
            neighbors.append([i, j])
    if max_neighbors_nb > len(neighbors):
        max_neighbors_nb = len(neighbors)

    for a in range(0, iteration):
        visited_neighbors = neighbors.copy()
        random.shuffle(visited_neighbors)
        for k in range(max_neighbors_nb):
            i, j = visited_neighbors[k][0], visited_neighbors[k][1]
            temp = copy.copy(scheduling)
            ls_swap = swap(i, j, temp)
            duration_temp = ls_swap.duree()
            if duration_temp < duration_candidate:
                duration_candidate = duration_temp
                candidate = ls_swap
        if duration > duration_candidate:
            scheduling = candidate
            duration = duration_candidate
        else:
            break
    return scheduling


def local_search_insert(flowshop, scheduling, iteration, max_neighbors_nb):
    """
    Returns a (new) scheduling after local search on the given initial scheduling during the maximum number of
    iterations given to find a minimum local, given an instance of the flowshop population (insert neighborhood)
    An iteration is an exploration of all the insert neighborhood of the current best scheduling
    :param flowshop: a Flowshop object
    :param scheduling: a scheduling (Ordonnancement object)
    :param iteration: maximum number of iterations (explorations of the insert neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :return: the scheduling after the given number of iteration of local search
    """
    nb_jobs = flowshop.nombre_jobs()

    candidate = copy.copy(scheduling)
    duration = scheduling.duree()
    duration_candidate = candidate.duree()
    neighbors = []
    for i in range(nb_jobs-1):
        for j in range(i+1, nb_jobs):
            neighbors.append([i, j])
    if max_neighbors_nb > len(neighbors):
        max_neighbors_nb = len(neighbors)

    for a in range(0, iteration):
        visited_neighbors = neighbors.copy()
        random.shuffle(visited_neighbors)
        for k in range(max_neighbors_nb):
            i, j = visited_neighbors[k][0], visited_neighbors[k][1]
            if j != i and (j != i-1 or i == 0):
                temp = copy.copy(scheduling)
                sequence = temp.sequence().copy()
                ls_insert = sequence[i]
                sequence.remove(ls_insert)
                sequence.insert(j, ls_insert)
                new_scheduling = Ordonnancement(temp.nb_machines)
                new_scheduling.ordonnancer_liste_job(sequence)
                duration_temp = new_scheduling.duree()
                if duration_temp < duration_candidate:
                    duration_candidate = duration_temp
                    candidate = new_scheduling
        if duration > duration_candidate:
            scheduling = candidate
            duration = duration_candidate
        else:
            break
    return scheduling
