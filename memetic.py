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


def find_best_sched_in_list(list_sched):
    """
    Finds the Ordonnancement object in the given list that has the lowest duration
    :param list_sched: list of Ordonnancement objects
    :return: the Ordonnancement object with the lowest duration
    """
    best_sched = list_sched[0]
    for sched in list_sched:
        if sched.duree() < best_sched.duree():
            best_sched = sched
    return best_sched


def memetic_heuristic(flowshop, parameters):
    """
        memetic heuristic for the flowshop problem
        :param flowshop: instance of flowshop
        :param parameters: dict of parameters used in the function.
            It must contain the following keys: 'rdm_size', 'swap_prob', 'insert_prob'
        :return: the Ordonnancement object with the lowest duration
        """
    start_time = time.time()
    population_size = parameters['population_size']
    best_sched = Ordonnancement(flowshop.nombre_machines())
    list_best_sched = []
    population = initial_population.random_initial_pop(flowshop, rdm_size='rdm_size')
    iteration_time = 0
    while time.time() - start_time + iteration_time < 60 * 10:
        start_time_iteration = time.time()
        population = solution_crossover.crossover(flowshop, population)
        population = mutation.mutation(flowshop, population, mutation_swap_probability=parameters['swap_prob'],
                                       mutation_insert_probability=parameters['insert_prob'])
        population = local_search.local_search(population)
        best_sched = find_best_sched_in_list(population)
        list_best_sched.append(best_sched)
        iteration_time = time.time() - start_time_iteration
    return list_best_sched
