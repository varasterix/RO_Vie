import unittest
from solution_crossover import crossover_2_points
from flowshop import Flowshop
from job import Job
from ordonnancement import Ordonnancement

job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])


class TestSolutionCrossoverFileMethods(unittest.TestCase):
    def test_crossover_2_points(self):
        parent_1 = Ordonnancement(job_1.nb_op)
        parent_2 = Ordonnancement(job_1.nb_op)
        parent_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
        parent_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
        # TODO
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
