import copy
import math
import random
import warnings
from src.ordonnancement import Ordonnancement

MAXINT = 10000


def initial_pop(flow_shop, random_prop, deter_prop, best_deter=False, pop_init_size=100):
    """
    Generates the initial population following a proportion of deterministic and random population
    :param flow_shop: an instance of the flow shop permutation problem
    :param deter_prop: desired proportion of the initial population computed in a deterministic manner
    :param random_prop: desired proportion of the initial population randomly generated
    :param best_deter: if true, select deterministic initial pop by scheduling duration, else random selection
    :param pop_init_size: size of the initial population, if bigger than the size of the total population, redefined
    to 1/3 of the total population
    :return: the initial population for the memetic algorithm
    """
    pop_max_size = math.factorial(flow_shop.nb_jobs)
    if pop_max_size < pop_init_size:
        pop_init_size = round(pop_max_size * 1 / 3)
        warning_size = "[INIT_POP] Initial population size is too high, new size: " + str(pop_init_size)
        warnings.formatwarning = custom_formatwarning
        warnings.warn(warning_size, Warning)

    deter_size = round(deter_prop / (deter_prop + random_prop) * pop_init_size)
    deter_pop = []
    if deter_size != 0:
        deter_pop = deterministic_initial_pop(flow_shop, deter_size, best_deter)

    rdm_size = pop_init_size - len(deter_pop)
    rdm_pop = []
    if rdm_size != 0:
        rdm_pop = random_initial_pop(flow_shop, rdm_size)

    starting_pop = rdm_pop + deter_pop
    random.shuffle(starting_pop)
    if len(deter_pop) < deter_size:
        warning_deter = "[INIT_POP] Deterministic proportion is too high, new proportion : Total size "\
                        + str(len(starting_pop)) + "\tDeterministic size " + str(len(deter_pop)) + "\tRandom size "\
                        + str(len(rdm_pop))
        warnings.formatwarning = custom_formatwarning
        warnings.warn(warning_deter, Warning)
    return starting_pop


def random_initial_pop(flow_shop, rdm_size):
    """
    Generates randomly the initial population
    :param flow_shop: an instance of the flow shop permutation problem
    :param rdm_size: number of element in the initial population to generate
    :return: the random part of the initial population for the memetic algorithm
    """
    population_seq = []
    population = []
    start = [flow_shop.liste_jobs(i) for i in range(flow_shop.nb_jobs)]
    for i in range(rdm_size):
        random.shuffle(start)
        elem = copy.copy(start)
        population_seq.append(elem)
    for seq in population_seq:
        temp_scheduling = Ordonnancement(flow_shop.nb_machines)
        temp_scheduling.ordonnancer_liste_job(seq)
        population.append(temp_scheduling)
    return population


def deterministic_initial_pop(flow_shop, deter_size, best_deter):
    """
    Generates deterministically the initial population
    :param flow_shop: an instance of the flow shop permutation problem
    :param deter_size: number of element in the initial population to generate
    :param best_deter:
    :return:
    """
    all_deterministic_seq = []
    neh_seq = neh_order(flow_shop)
    all_deterministic_seq.append(neh_seq)
    for m_index in range(flow_shop.nb_machines):
        temp_sep_desc = job_duration_order_desc(flow_shop, m_index)
        temp_sep_asc = job_duration_order_asc(flow_shop, m_index)
        all_deterministic_seq.append(temp_sep_asc)
        all_deterministic_seq.append(temp_sep_desc)
    for sum_index in range(flow_shop.nb_machines - 1):
        temp_johnson_seq = johnson_rule_order(flow_shop, sum_index)
        all_deterministic_seq.append(temp_johnson_seq)

    deter_pop = []
    if best_deter:
        all_deterministic_ordo = []
        for seq in all_deterministic_seq:
            ordo = Ordonnancement(flow_shop.nb_machines)
            ordo.ordonnancer_liste_job(seq)
            all_deterministic_ordo.append(ordo)
        sorted_scheduling = sorted(all_deterministic_ordo, key=lambda o: o.duree(), reverse=False)
        if deter_size > len(sorted_scheduling):
            deter_pop = sorted_scheduling
        else:
            deter_pop = sorted_scheduling[0:deter_size]
    else:
        if deter_size > len(all_deterministic_seq):
            seq_deter_sample = all_deterministic_seq
        else:
            seq_deter_sample = random.sample(all_deterministic_seq, deter_size)
        for seq in seq_deter_sample:
            ordo = Ordonnancement(flow_shop.nb_machines)
            ordo.ordonnancer_liste_job(seq)
            deter_pop.append(ordo)
    return deter_pop


def neh_order(flow_shop):
    """
    Compute the NEH scheduling of flow_shop
    :param flow_shop: an instance of the flow shop permutation problem
    :return: return the NEH scheduling of flow_shop
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda j: j.duree(), reverse=True)
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


def johnson_rule_order(flow_shop, sum_index):
    """
    Schedule a flow shop following the Johnson rule
    :param flow_shop: an instance of the flow shop permutation problem
    :param sum_index: splinting tasks in two groups at this index
    :return:
    """
    list_to_order = []
    for j in flow_shop.l_job:
        start = 0
        end = 0
        for i in range(0, sum_index):
            start += j.duree_operation(i)
        for i in range(sum_index, flow_shop.nb_machines):
            end += j.duree_operation(i)
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


def job_duration_order_desc(flow_shop, m_index):
    """
    Schedule a flow shop following the duration of each job on the reference machine (descending order)
    :param flow_shop: an instance of the flow shop permutation problem
    :param m_index: index of the reference machine
    :return: return the computed schedule
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda job: job.duree_operation(m_index), reverse=True)
    return sorted_jobs


def job_duration_order_asc(flow_shop, m_index):
    """
    Schedule a flow shop following the duration of each job on the reference machine (ascending order)
    :param flow_shop: an instance of the flow shop permutation problem
    :param m_index: index of the reference machine
    :return: return the computed schedule
    """
    sorted_jobs = sorted(flow_shop.l_job, key=lambda job: job.duree_operation(m_index), reverse=False)
    return sorted_jobs


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'
