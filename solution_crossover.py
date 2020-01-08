import random
from ordonnancement import Ordonnancement


def crossover(flowshop, initial_pop, cross_1_point_prob, cross_2_points_prob, gentrification):
    """
    Generates a new population by crossing schedulings of the previous one
    :param flowshop: an instance of the flow shop permutation problem
    :param initial_pop: population of schedulings to cross
    :param cross_1_point_prob: the probability of using the 1 point crossover method for each pair of parent
    :param cross_2_points_prob: the probability of using the 2 points crossover method for each pair of parent
    :return population: the population with crossed schedulings
    """
    sum_prop = cross_1_point_prob + cross_2_points_prob
    cross_1_point_prob /= sum_prop
    cross_2_points_prob /= sum_prop
    nb_jobs = flowshop.nombre_jobs()
    population = initial_pop.copy()
    population_size = len(population)
    if gentrification:
        population = sorted(population, key=lambda sched: sched.duree(), reverse=False)
    else:
        random.shuffle(population)
    indices = [i for i in range(nb_jobs)]
    for j in range(0, len(population), 2):
        method_random = random.random()
        if method_random < cross_1_point_prob:
            point = random.randint(0, nb_jobs)
            children_temp = crossover_1_point(population[j], population[j+1], point)
        else:
            point1, point2 = random.sample(indices, 2)
            children_temp = crossover_2_points(population[j], population[j+1], point1, point2)
        population.append(children_temp[0])
        population.append(children_temp[1])
    population = sorted(population, key=lambda sched: sched.duree(), reverse=False)
    population = population[0:population_size]
    return population


def crossover_2_points(sched1, sched2, point1, point2):
    """
    Crosses two schedulings with the
    :param sched1: parent 1 for crossover (Ordonnancement object)
    :param sched2: parent 2 for crossover (Ordonnancement object)
    :param point1: first point of the interval to swap, INTEGER between 0 and nb_jobs
    :param point2: second point of the interval to swap, INTEGER between 0 and nb_jobs, different of point1
    :return population: the two children schedulings (Ordonnancement objects)
    """
    nb_jobs = len(sched1.sequence())
    point1, point2 = min(point1, point2), max(point1, point2)
    seq1 = sched1.sequence().copy()
    seq2 = sched2.sequence().copy()
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
        k = random.randint(0, len(list_exclude[1]) - 1)
        n = list_exclude[1][k]
        m = list_exclude[0][j]
        seq12[m], seq22[n] = seq22[n], seq12[m]
        list_exclude[1].pop(k)
    new_seq1 = seq11 + seq22 + seq13
    new_seq2 = seq21 + seq12 + seq23
    nb_machines = sched1.nb_machines
    scheduling1 = Ordonnancement(nb_machines)
    scheduling2 = Ordonnancement(nb_machines)
    scheduling1.ordonnancer_liste_job(new_seq1)
    scheduling2.ordonnancer_liste_job(new_seq2)
    return [scheduling1, scheduling2]


def crossover_1_point(sched1, sched2, point1):
    """
    Crosses two schedulings with the
    :param sched1: parent 1 for crossover (Ordonnancement object)
    :param sched2: parent 2 for crossover (Ordonnancement object)
    :param point1: separation point to swap the sub-sequences, INTEGER between 0 and nb_jobs
    :return population: the two children schedulings (Ordonnancement objects)
    """
    nb_jobs = len(sched1.sequence())
    seq1 = sched1.sequence().copy()
    seq2 = sched2.sequence().copy()
    seq11 = seq1[0:point1]
    seq12 = seq1[point1:]
    seq21 = seq2[0:point1]
    seq22 = seq2[point1:]
    list_exclude = [[], []]
    for i in range(len(seq11)):
        if seq11[i] not in seq21:
            list_exclude[0].append(i)
        if seq21[i] not in seq11:
            list_exclude[1].append(i)
    for j in range(len(list_exclude[0])):
        k = random.randint(0, len(list_exclude[1]) - 1)
        n = list_exclude[1][k]
        m = list_exclude[0][j]
        seq11[m], seq21[n] = seq21[n], seq11[m]
        list_exclude[1].pop(k)
    new_seq1 = seq11 + seq22
    new_seq2 = seq21 + seq12
    nb_machines = sched1.nb_machines
    scheduling1 = Ordonnancement(nb_machines)
    scheduling2 = Ordonnancement(nb_machines)
    scheduling1.ordonnancer_liste_job(new_seq1)
    scheduling2.ordonnancer_liste_job(new_seq2)
    return [scheduling1, scheduling2]
