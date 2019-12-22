import copy
import math
import random
from ordonnancement import Ordonnancement

MAXINT = 10000


def initial_pop(flow_shop, deter_prop, random_prop):
    """
    Generates the initial population following a proportion of deterministic and random population
    :param flow_shop: an instance of the flow shop permutation problem
    :param deter_prop: proportion of the initial population computed in a deterministic manner
    :param random_prop: proportion of the initial population randomly generated
    :return: the initial population for the memetic algorithm
    """
    pop_max_size = math.factorial(flow_shop.nb_jobs)
    pop_init_size = 100
    if pop_max_size < 100:
        pop_init_size = round(pop_max_size * 1/3)
    deter_size = round(deter_prop / (deter_prop+random_prop) * pop_init_size)
    rdm_size = pop_init_size - deter_size
    rdm_pop = random_initial_pop(flow_shop, rdm_size)
    deter_pop = deterministic_initial_pop(flow_shop, deter_size)
    starting_pop = rdm_pop + deter_pop
    return starting_pop


def random_initial_pop(flow_shop, nb_value=10):
    """
    Generates randomly the initial population
    :param flow_shop: an instance of the flow shop permutation problem
    :param nb_value: number of element in the initial population to generate
    :return population: the random part of the initial population for the memetic algorithm
    """
    population_seq = []
    population = []
    start = [flow_shop.liste_jobs(i) for i in range(flow_shop.nb_jobs)]
    for i in range(nb_value):
        random.shuffle(start)
        elem = copy.copy(start)
        population_seq.append(elem)
    for seq in population_seq:
        temp_scheduling = Ordonnancement(flow_shop.nb_machines)
        temp_scheduling.ordonnancer_liste_job(seq)
        population.append(temp_scheduling)
    return population


def johnson_rule_order(flow_shop, sum_index):
    list_to_order = []

    for j in flow_shop.l_job:
        start = 0
        end = 0
        for i in range(0, sum_index):
            start += j.duree_operation(i)
        for i in range(sum_index, flow_shop.nb_machines):
            end += j.duree_opeation(i)
        list_to_order.append((j, start, end))
    john_start = []
    john_end = []
    while len(list_to_order) != 0:
        min_start = min(list_to_order, key=lambda t: t[1])
        min_end = min(list_to_order, key=lambda t: t[2])
        if min_start[1] < min_end[2]:
            john_start.append(min_start[0])
            list_to_order.remove(min_start)
        else:
            john_end.insert(0, min_end[0])
            list_to_order.remove(min_end)
    johnson_order = john_start + john_end
    return johnson_order


def deterministic_initial_pop(flow_shop, nb_value=10):
    """

    :param flow_shop:
    :param nb_value:
    :return deter_pop:
    """
    all_deterministic_seq = []
    neh_seq = neh_order(flow_shop)
    all_deterministic_seq.append(neh_seq)
    for m_index in range(flow_shop.nb_machines):
        temp_sep_desc = job_duration_order_desc(flow_shop, m_index)
        temp_sep_asc = job_duration_order_asc(flow_shop, m_index)
        all_deterministic_seq.append(temp_sep_asc, temp_sep_desc)
    for sum_index in range(flow_shop.nb_machines-1):
        temp_johnson_seq = johnson_rule_order(flow_shop, sum_index)
        all_deterministic_seq.append(temp_johnson_seq)
    seq_deter_sample = random.sample(all_deterministic_seq, nb_value)
    deter_pop = []
    for seq in seq_deter_sample:
        ordo = Ordonnancement(flow_shop.nb_machines)
        ordo.ordonnancer_liste_job(seq)
        deter_pop.append(ordo)
    return deter_pop


def neh_order(flow_shop):
    """
    Compute the NEH scheduling of flow_shop
    :param flow_shop: an instance of the flow shop permutation problem
    :return best_order: return the NEH scheduling of flow_shop
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda job: job.duree(), reverse=True)
    best_order = []
    for job in sorted_jobs:
        min_duration = MAXINT
        best_pos = 0
        for i in range(0, len(best_order) + 1):
            scheduling = Ordonnancement(flow_shop.nb_machines)
            new_list = [j for j in best_order]
            new_list.insert(i, job)
            scheduling.ordonnancer_liste_job(new_list)
            if scheduling.duree() < min_duration:
                min_duration = scheduling.duree()
                best_pos = i
        best_order.insert(best_pos, job)
    return best_order


def job_duration_order_desc(flow_shop, m_index):
    """

    :param flow_shop:
    :param m_index:
    :return sorted_jobs:
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda job: job.duree_operation(m_index), reverse=True)
    return sorted_jobs


def job_duration_order_asc(flow_shop, m_index):
    """

    :param flow_shop:
    :param m_index:
    :return sorted_jobs:
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda job: job.duree_operation(m_index), reverse=False)
    return sorted_jobs
