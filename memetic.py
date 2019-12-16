# The four stages are:
#   - initial population generation
#   - solution crossing
#   - mutation
#   - local search
# The 3 last stages are iterated several times

import time
from ordonnancement import Ordonnancement
from flowshop import Flowshop
import initial_population
import solution_crossing
import mutation
import local_search

def memetic_heuristic(flowshop):
    start_time = time.time()
    best_ordo = Ordonnancement()
    population = initial_population.random_initial_pop(flowshop)
    while time.time() - start_time < 60 * 10:
        population = solution_crossing.crossing(flowshop, population)
        population = mutation.mutation(population)
        population = local_search.local_search(population)
        best_ordo = population[0]
    return best_ordo
