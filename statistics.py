import statistics


def population_statistics(pop):
    pop_duration = [sched.duree() for sched in pop]
    return statistics.mean(pop_duration), min(pop_duration), max(pop_duration)