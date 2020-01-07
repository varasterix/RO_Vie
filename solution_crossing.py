import job
import ordonnancement
import flowshop
import random as rd

def valueOfOrdo(ordo):
    return ordo.duree()

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
    sumValue = 0
    for ordo in population:
        sumValue += ordo.duree()
    finalPop = []
    for ordo in population:
        proba = (sumValue - ordo.duree())/((len(population)-1)*ordo.duree())
        if rd.random() < proba:
            finalPop.append(ordo)

    return finalPop




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


def testCrossingIndividuals():
    j1 = job.Job(1, [1, 3, 5, 18, 23])
    j2 = job.Job(2, [1, 3, 5, 18, 23])
    j3 = job.Job(3, [1, 3, 5, 18, 23])
    j4 = job.Job(4, [1, 3, 5, 18, 23])
    j5 = job.Job(5, [1, 3, 5, 18, 23])
    j6 = job.Job(6, [1, 3, 5, 18, 23])
    ordo1 = ordonnancement.Ordonnancement(5)
    ordo2 = ordonnancement.Ordonnancement(5)
    ordo1.ordonnancer_liste_job([j3,j4,j1,j5,j6,j2])
    ordo2.ordonnancer_liste_job([j1,j5,j3,j2,j6,j4])
    fs = flowshop.Flowshop(6,5,[j1,j2,j3,j4,j5,j6])
    child = crossingIndividuals(ordo1, ordo2,fs)
    print("solution found\n")
    print(["j"+str(child.seq[i].num) for i in range(len(child.seq))])
    print("possible expected solutions \n ")
    print(["j3", "j1", "j5", "j4", "j6", "j2"])
    print(["j1", "j3", "j5", "j4", "j6", "j2"])
    print(["j3", "j1", "j5", "j4", "j2", "j6"])
    print(["j1", "j3", "j5", "j4", "j2", "j6"])


testCrossingIndividuals()










