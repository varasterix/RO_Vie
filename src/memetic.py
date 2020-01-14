# The four stages are:
#   - initial population generation
#   - solution crossing
#   - mutation
#   - local search
#   - selection
# The 3 last stages are iterated several times

import time
from src import initial_population, mutation, local_search, solution_crossover, population_statistics
from src.convergence import is_convergent


def restart_population(population, flowshop, preserved_prop):
    """
    restart_population function called when the population is convergent
    :param population: population to restart
    :param flowshop: instance of the flowshop problem
    :param preserved_prop: proportion to preserve
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
    sorted_list = sorted(population, key=lambda sched: sched.duree(), reverse=False)
    return sorted_list[:preserved_size]


def memetic_heuristic(flowshop, parameters):
    """
        memetic heuristic for the flowshop problem
        :param flowshop: instance of flowshop
        :param parameters: dict of parameters used in the function.
            It must contain the following keys: 'random_prop', 'deter_prop', 'best_deter', 'pop_init_size', 'time_limit'
            , 'cross_1_point_prob', 'cross_2_points_prob','cross_position_prob', 'gentrification', 'swap_prob',
            'insert_prob', 'entropy_threshold', 'preserved_prop'
        :return: the Ordonnancement object with the lowest duration
        """
    start_time = time.time()
    population = initial_population.initial_pop(flowshop,
                                                random_prop=parameters['random_prop'],
                                                deter_prop=parameters['deter_prop'],
                                                best_deter=parameters['best_deter'],
                                                pop_init_size=parameters['pop_init_size'])
    initial_statistics = population_statistics.population_statistics(population)

    overall_best_scheduling = min(population, key=lambda sched: sched.duree())
    list_best_schedulings = [overall_best_scheduling]
    population = local_search.local_search(flowshop,
                                           population,
                                           maximum_nb_iterations=parameters['ls_max_iterations'],
                                           local_search_swap_prob=parameters['ls_swap_prob'],
                                           local_search_insert_prob=parameters['ls_insert_prob'])
    iteration_time = 0
    while time.time() - start_time + iteration_time + 1 < 60 * parameters['time_limit']:
        start_time_iteration = time.time()
        population = solution_crossover.crossover(flowshop,
                                                  population,
                                                  cross_1_point_prob=parameters['cross_1_point_prob'],
                                                  cross_2_points_prob=parameters['cross_2_points_prob'],
                                                  cross_position_prob=parameters['cross_position_prob'],
                                                  gentrification=parameters['gentrification'])
        population = mutation.mutation(flowshop,
                                       population,
                                       mutation_swap_probability=parameters['mut_swap_prob'],
                                       mutation_insert_probability=parameters['mut_insert_prob'])
        best_sched = min(population, key=lambda sched: sched.duree())
        list_best_schedulings.append(best_sched)
        if overall_best_scheduling is None or overall_best_scheduling.duree() > best_sched.duree():
            overall_best_scheduling = best_sched
        if is_convergent(population, threshold=parameters['entropy_threshold']):
            population = restart_population(population,
                                            flowshop,
                                            preserved_prop=parameters['preserved_prop'])
            population = local_search.local_search(flowshop,
                                                   population,
                                                   maximum_nb_iterations=parameters['ls_max_iterations'],
                                                   local_search_swap_prob=parameters['ls_swap_prob'],
                                                   local_search_insert_prob=parameters['ls_insert_prob'])
        iteration_time = time.time() - start_time_iteration
    return list_best_schedulings, overall_best_scheduling, initial_statistics
