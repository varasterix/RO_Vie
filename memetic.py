# The four stages are:
#   - initial population generation
#   - solution crossing
#   - mutation
#   - local search
#   - selection
# The 3 last stages are iterated several times

import time
from ordonnancement import Ordonnancement
import initial_population
import solution_crossover
import mutation
import local_search


def find_best_ordo_in_list(list_ordo):
    """
    Finds the Ordonnancement object in the given list that has the lowest duration
    :param list_ordo: list of Ordonnancement objects
    :return: the Ordonnancement object with the lowest duration
    """
    best_ordo = list_ordo[0]
    for ordo in list_ordo:
        if ordo.duree() < best_ordo.duree():
            best_ordo = ordo
    return best_ordo


def memetic_heuristic(flowshop):
    start_time = time.time()
    best_ordo = Ordonnancement(flowshop.nombre_machines())
    population = initial_population.random_initial_pop(flowshop)
    iteration_time = 0
    while time.time() - start_time + iteration_time < 60 * 10:
        start_time_iteration = time.time()
        population = solution_crossover.crossover(flowshop, population)
        population = mutation.mutation(flowshop, population)
        population = local_search.local_search(population)
        best_ordo = find_best_ordo_in_list(population)
        iteration_time = time.time() - start_time_iteration
    return best_ordo
