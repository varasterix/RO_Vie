import job
import ordonnancement


def valueOfOrdo(ordo):
    return ordo.date_disponibilite[ordo.nb_machines-1]

def crossing(flowshop, initial_pop):
    n = len(initial_pop)
    population = initial_pop
    #to have as many children as parents we group parents by 3 and make 3 couples for each group of three
    for i in range(len(initial_pop)//3):
        child1 = crossingIndividuals(initial_pop[3*i], initial_pop[3*i+1], flowshop)
        child2 = crossingIndividuals(initial_pop[3*i], initial_pop[3*i+2], flowshop)
        child3 = crossingIndividuals(initial_pop[3*i+1], initial_pop[3*i+2], flowshop)
        population.append(crossingIndividuals(child1))
        population.append(crossingIndividuals(child2))
        population.append(crossingIndividuals(child3))
    population.sort(key = valueOfOrdo)
    return population[:n]




def crossingIndividuals(ordo1, ordo2, flowshop):
    """crossing rules : two individuals : [2,3,5,1,4] & [3,4,1,2,5] the index of the lists are the jobs
    and the values are the positions. We sum the two lists : [5,7,6,3,9] and we reaarenge it [2,4,3,1,5]"""
    positionsJobs1 = {} #The keys are the jobs and the values their positions in ordo1
    positionsJob2 = {} #same thing for ordo
    for i in range(len(ordo1.seq)):
        positionsJobs1[ordo1.seq[i]] = i
        positionsJob2[ordo2.seq[i]] = i
    sumPositions = {} #the keys are the jobs and the values the sum of the positions
    for job in ordo1.seq:
        sumPositions[job] = positionsJobs1[job] + positionsJob2[job]
    childrenSeq = sorted(sumPositions, key=sumPositions.__getitem__, reverse=False)
    childOrdo = ordonnancement.Ordonnancement(flowshop.nb_machines)
    childOrdo.ordonnancer_liste_job(childrenSeq)
    return childOrdo










