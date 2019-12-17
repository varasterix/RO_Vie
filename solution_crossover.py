import random
from ordonnancement import Ordonnancement


def crossover(flowshop, initial_pop):
    """
    Generates a new population by crossing schedulings of the previous one
    :param flowshop: an instance of the flow shop permutation problem
    :param initial_pop: population of schedulings to cross
    :return population: the population with crossed schedulings
    """
    nb_jobs = flowshop.nombre_jobs()
    population = initial_pop
    population = sort_by_duration(population)
    indices = [i for i in range(nb_jobs)]
    for j in range(0, len(population), 2):
        point1, point2 = random.sample(indices, 2)
        children_temp = crossover_2_points(population[j], population[j+1], point1, point2)
        population.append(children_temp[0])
        population.append(children_temp[1])
    return population


def sort_by_duration(population):
    for i in range(len(population) - 1):
        best_index = i
        for j in range(i + 1, len(population)):
            if population[j].duree() < population[best_index].duree():
                best_index = j
        population[i], population[best_index] = population[best_index], population[i]
    return population


def crossover_2_points(sched1, sched2, point1, point2):
    """
    Crosses two schedulings with the
    :param sched1: parent 1 for crossover
    :param sched2: parent 2 for crossover
    :param point1: first point of the interval to swap, INTEGER between 0 and nb_jobs
    :param point2: second point of the interval to swap, INTEGER between 0 and nb_jobs, different of point1
    :return population: the two children schedulings
    """
    nb_jobs = len(sched1.sequence())
    point1, point2 = min(point1, point2), max(point1, point2)
    seq1 = sched1.sequence()
    seq2 = sched2.sequence()
    seq11 = seq1[0:point1]
    seq12 = seq1[point1:point2]
    seq13 = seq1[point2:nb_jobs]
    seq21 = seq2[0:point1]
    seq22 = seq2[point1:point2]
    seq23 = seq2[point2:nb_jobs]
    list_exclude = [[], []]
    for i in range(len(seq12)):
        if seq12[i] not in seq22:
            list_exclude[0].append(i)
        if seq22[i] not in seq12:
            list_exclude[1].append(i)
    for j in range(len(list_exclude[0])):
        k = random.randint(0, len(list_exclude[0]) - 1)
        seq12[j], seq22[k] = seq22[k], seq12[j]
        list_exclude[0].pop(j)
        list_exclude[1].pop(k)
    new_seq1 = seq11 + seq22 + seq13
    new_seq2 = seq21 + seq12 + seq23
    nb_machines = sched1.nb_machines
    scheduling1 = Ordonnancement(nb_machines)
    scheduling2 = Ordonnancement(nb_machines)
    scheduling1.ordonnancer_liste_job(new_seq1)
    scheduling2.ordonnancer_liste_job(new_seq2)
    return [scheduling1, scheduling2]
