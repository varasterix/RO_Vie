# The four stages are:
#   - initial population generation
#   - solution crossing
#   - mutation
#   - local search
#   - selection
# The 3 last stages are iterated several times

import time
import initial_population
import solution_crossover
import mutation
import local_search
from convergence import is_convergent


def restart_population(population, preserved_prop, flowshop):
    """
    restart_population function called when the population is convergent
    :param population: population to restart
    :param preserved_prop: proportion to preserve
    :param flowshop: instance of the flowshop problem
    :return: the new population
    """
    preserved_size = int(len(population) * preserved_prop)
    random_size = len(population) - preserved_size
    return (extract_best_from_population(population, preserved_size) +
            initial_population.random_initial_pop(flowshop, random_size))


def extract_best_from_population(population, preserved_size):
    """
    Extracts the preserved_prop proportion of the list list_sched that has the lowest durations
    :param population: list of Ordonnancement objects
    :param preserved_size: number of schedulings to extract from the population
    :return: the list of schedulings (Ordonnancement objects) with the lowest durations of the given size
    """
    sorted_list = sorted(population, key=lambda sched: sched.duree(), reverse=True)
    return sorted_list[:preserved_size]


def memetic_heuristic(flowshop, parameters):
    """
        memetic heuristic for the flowshop problem
        :param flowshop: instance of flowshop
        :param parameters: dict of parameters used in the function.
            It must contain the following keys: 'random_prop', 'deter_prop', 'best_deter', 'pop_init_size', 'time_limit'
            , 'cross_1_point_prob', 'cross_2_points_prob', 'swap_prob', 'insert_prob', 'entropy_threshold',
            'preserved_prop'
        :return: the Ordonnancement object with the lowest duration
        """
    start_time = time.time()
    list_best_sched = []
    population = initial_population.initial_pop(flowshop,
                                                random_prop=parameters['random_prop'],
                                                deter_prop=parameters['deter_prop'],
                                                best_deter=parameters['best_deter'],
                                                pop_init_size=parameters['pop_init_size'])
    iteration_time = 0
    while time.time() - start_time + iteration_time < 60 * parameters['time_limit']:
        start_time_iteration = time.time()
        population = solution_crossover.crossover(flowshop,
                                                  population,
                                                  parameters['cross_1_point_prob'],
                                                  parameters['cross_2_points_prob'])
        population = mutation.mutation(flowshop,
                                       population,
                                       mutation_swap_probability=parameters['swap_prob'],
                                       mutation_insert_probability=parameters['insert_prob'])
        population = local_search.local_search(population)
        best_sched = max(population, key=lambda sched: sched.duree())
        list_best_sched.append(best_sched)
        if is_convergent(population, parameters['entropy_threshold']):
            population = restart_population(population, parameters['preserved_prop'], flowshop)
        iteration_time = time.time() - start_time_iteration
    return list_best_sched
