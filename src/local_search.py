import copy
import random
from src.ordonnancement import Ordonnancement


def local_search(population, maximum_nb_iterations, max_neighbors_nb, local_search_swap_prob,
                 local_search_insert_prob, swap_neighbors, insert_neighbors, nb_sched):
    """
    Generates a new population by improving each scheduling with a local search method during the given maximum number
    of iterations
    :param population: population of schedulings to improve with local search
    :param maximum_nb_iterations: maximum number of iterations (explorations of a neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :param local_search_swap_prob: probability of using the swap local search for a scheduling in the population
    :param local_search_insert_prob: probability of using the insert local search for a scheduling in the population
    :param swap_neighbors: the list of neighbors for the swap method
    :param insert_neighbors: the list of neighbors for the insert method
    :param nb_sched: the number of schedulings over which to do a local search
    :return: new population after local search improvements
    """
    sum_prob = local_search_swap_prob + local_search_insert_prob
    local_search_swap_prob /= sum_prob
    local_search_insert_prob /= sum_prob
    new_population = []
    population = sorted(population, key=lambda sched: sched.duree(), reverse=False)
    index = 0
    for scheduling in population:
        if index < nb_sched:
            method_random = random.random()
            new_scheduling = local_search_swap(scheduling, maximum_nb_iterations, max_neighbors_nb, swap_neighbors) \
                if method_random < local_search_swap_prob \
                else local_search_insert(scheduling, maximum_nb_iterations, max_neighbors_nb, insert_neighbors)
            new_population.append(new_scheduling)
        else:
            new_population.append(scheduling)
    random.shuffle(new_population)
    return new_population


def swap(i, j, scheduling):
    sequence = scheduling.sequence().copy()
    sequence[i], sequence[j] = sequence[j], sequence[i]
    new_scheduling = Ordonnancement(scheduling.nb_machines)
    new_scheduling.ordonnancer_liste_job(sequence)
    return new_scheduling


def create_swap_neighbors(flowshop):
    """
    creates a list of neighbors for the swap local search method
    :param flowshop: instance of flowshop problem
    :return: the list of neighbors for the swap method
    """
    nb_jobs = flowshop.nombre_jobs()
    neighbors = []
    for i in range(nb_jobs-1):
        for j in range(i+1, nb_jobs):
            neighbors.append([i, j])
    return neighbors


def local_search_swap(scheduling, iteration, max_neighbors_nb, neighbors):
    """
    Returns a (new) scheduling after local search on the given initial scheduling during the maximum number of
    iterations given to find a minimum local, given an instance of the flowshop population (swap neighborhood)
    An iteration is an exploration of all the swap neighborhood of the current best scheduling
    :param scheduling: a scheduling (Ordonnancement object)
    :param iteration: maximum number of iterations (explorations of the swap neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :param neighbors: list of neighbors
    :return: the scheduling after the given number of iteration of local search
    """

    candidate = copy.copy(scheduling)
    duration = scheduling.duree()
    duration_candidate = candidate.duree()
    if max_neighbors_nb > len(neighbors):
        max_neighbors_nb = len(neighbors)

    for a in range(0, iteration):
        visited_neighbors = neighbors.copy()
        for k in range(max_neighbors_nb):
            index = random.randint(0, len(visited_neighbors) - 1)
            i, j = visited_neighbors[index][0], visited_neighbors[index][1]
            visited_neighbors.pop(index)
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


def create_insert_neighbors(flowshop):
    """
    creates a list of neighbors for the insert local search method
    :param flowshop: instance of flowshop problem
    :return: the list of neighbors
    """
    nb_jobs = flowshop.nombre_jobs()
    neighbors = []
    for i in range(nb_jobs):
        for j in range(nb_jobs):
            if j != i and (j != i - 1 or i == 0):
                neighbors.append([i, j])
    return neighbors


def local_search_insert(scheduling, iteration, max_neighbors_nb, neighbors):
    """
    Returns a (new) scheduling after local search on the given initial scheduling during the maximum number of
    iterations given to find a minimum local, given an instance of the flowshop population (insert neighborhood)
    An iteration is an exploration of all the insert neighborhood of the current best scheduling
    :param scheduling: a scheduling (Ordonnancement object)
    :param iteration: maximum number of iterations (explorations of the insert neighborhood) to find a minimum local
    :param max_neighbors_nb: number of neighbors to visit at each iteration
    :param neighbors: list of neighbors
    :return: the scheduling after the given number of iteration of local search
    """

    candidate = copy.copy(scheduling)
    duration = scheduling.duree()
    duration_candidate = candidate.duree()
    if max_neighbors_nb > len(neighbors):
        max_neighbors_nb = len(neighbors)

    for a in range(0, iteration):
        visited_neighbors = neighbors.copy()
        for k in range(max_neighbors_nb):
            index = random.randint(0, len(visited_neighbors) - 1)
            i, j = visited_neighbors[index][0], visited_neighbors[index][1]
            visited_neighbors.pop(index)
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
