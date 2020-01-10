import statistics


def population_statistics(population):
    pop_duration = [sched.duree() for sched in population]
    return statistics.mean(pop_duration), min(pop_duration), max(pop_duration)
