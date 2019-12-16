import random
from ordonnancement import Ordonnancement


def mutation(flowshop, population, mutation_probability=0.4):
    nb_jobs = flowshop.nb_jobs()
    for i in range(len(population)):
        if random.random() < mutation_probability:
            sequence = population[i].sequence()
            indices = [j for j in range(nb_jobs)]
            a, b = random.sample(indices, 2)
            sequence[a], sequence[b] = sequence[b], sequence[a]

            ordo = Ordonnancement(population[i].nb_machines)
            for k in range(len(sequence)):
                ordo.ordonnancer_job(flowshop.liste_jobs[k])
    return population
