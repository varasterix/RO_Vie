import random
import copy
from src.ordonnancement import Ordonnancement

"""
This python file implements the mutation step in memetic/genetic algorithms for an instance of the flow-shop permutation 
problem. Several mutation functions are implemented.

WARNING: If a new mutation method is added, the global "mutation" function of this file has to be modified (parameters, 
method indices, conditions...) and its function calls everywhere else in the project 
"""


def mutation(flowshop, population, mutation_swap_probability=0.4, mutation_insert_probability=0.4):
    """
    Returns a new population after the all the mutation step given an instance of the flow-shop permutation problem, a
    population and a mutation probability for each mutation function
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :param mutation_swap_probability: probability for each Ordonnancement object in the population to mutate with the
    swap method mutation
    :param mutation_insert_probability: probability for each Ordonnancement object in the population to mutate with the
    insert method mutation
    :return: the population (list of Ordonnancement objects) after all the mutation step
    """
    # Note :
    # The mutation_swap method has the index 0
    # The mutation_insert method has the index 1

    nb_mutation_methods = 2
    swap_mutation_allowed = mutation_swap_probability != 0.0
    insert_mutation_allowed = mutation_insert_probability != 0.0
    mutated_population = copy.copy(population)

    order_of_mutations = [index_method for index_method in range(nb_mutation_methods)]
    random.shuffle(order_of_mutations)
    for index_method in order_of_mutations:
        if index_method == 0 and swap_mutation_allowed:
            mutated_population = mutation_swap(flowshop, mutated_population, mutation_swap_probability)
        elif index_method == 1 and insert_mutation_allowed:
            mutated_population = mutation_insert(flowshop, mutated_population, mutation_insert_probability)
    return mutated_population


def mutation_swap(flowshop, population, mutation_probability=0.4):
    """
    Returns a new population after mutation given an instance of the flowshop permutation problem, a population and a
    mutation probability (swap method)
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :param mutation_probability: probability for each Ordonnancement object in the population to mutate
    :return: the population after mutation
    """
    nb_jobs = flowshop.nombre_jobs()
    mutated_population = []
    for sched in population:
        if random.random() < mutation_probability:
            sequence = sched.sequence().copy()
            indices = [j for j in range(nb_jobs)]
            a, b = random.sample(indices, 2)
            sequence[a], sequence[b] = sequence[b], sequence[a]

            mutated_sched = Ordonnancement(sched.nb_machines)
            mutated_sched.ordonnancer_liste_job(sequence)
            mutated_population.append(mutated_sched)
        else:
            mutated_population.append(sched)
    return mutated_population


def mutation_insert(flowshop, population, mutation_probability=0.4):
    """
    Returns a new population after mutation given an instance of the flowshop permutation problem, a population and a
    mutation probability (insert method)
    :param flowshop: a Flowshop object
    :param population: list of Ordonnancement objects
    :param mutation_probability: probability for each Ordonnancement object in the population to mutate
    :return: the population after mutation
    """
    nb_jobs = flowshop.nombre_jobs()
    mutated_population = []
    for sched in population:
        if random.random() < mutation_probability:
            sequence = sched.sequence().copy()
            indices = [i for i in range(nb_jobs)]
            elt_index, insert_index = random.sample(indices, 2)
            temp = sequence[elt_index]
            sequence.remove(temp)
            sequence.insert(insert_index, temp)

            mutated_sched = Ordonnancement(sched.nb_machines)
            mutated_sched.ordonnancer_liste_job(sequence)
            mutated_population.append(mutated_sched)
        else:
            mutated_population.append(sched)
    return mutated_population
