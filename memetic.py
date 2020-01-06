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


def memetic_heuristic(flowshop, parameters):
    """
        memetic heuristic for the flowshop problem
        :param flowshop: instance of flowshop
        :param parameters: dict of parameters used in the function.
            It must contain the following keys: 'population_size', 'swap_prob', 'insert_prob'
        :return: the Ordonnancement object with the lowest duration
        """
    start_time = time.time()
    population_size = parameters['population_size']
    best_ordo = Ordonnancement(flowshop.nombre_machines())
    population = initial_population.random_initial_pop(flowshop, nb_value=population_size)
    iteration_time = 0
    while time.time() - start_time + iteration_time < 60 * 10:
        start_time_iteration = time.time()
        population = solution_crossover.crossover(flowshop, population)
        population = mutation.mutation(flowshop, population, mutation_swap_probability=parameters['swap_prob'],
                                       mutation_insert_probability=parameters['insert_prob'])
        population = local_search.local_search(population)
        best_ordo = find_best_ordo_in_list(population)
        iteration_time = time.time() - start_time_iteration
    return best_ordo
