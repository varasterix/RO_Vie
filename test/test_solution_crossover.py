import unittest
from solution_crossover import crossover_2_points, crossover, crossover_1_point
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
        initial_pop = [parent_1, parent_2]
        new_pop = crossover_2_points(parent_1, parent_2, 1, 3)
        self.assertEqual(len(initial_pop), len(new_pop))
        for sched in new_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, sched.sequence())
        # TODO

    def test_crossover_1_points(self):
        parent_1 = Ordonnancement(job_1.nb_op)
        parent_2 = Ordonnancement(job_1.nb_op)
        parent_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
        parent_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
        initial_pop = [parent_1, parent_2]
        new_pop = crossover_1_point(parent_1, parent_2, 3)
        self.assertEqual(len(initial_pop), len(new_pop))
        for sched in new_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, sched.sequence())

    def test_crossover(self):
        parent_1 = Ordonnancement(job_1.nb_op)
        parent_2 = Ordonnancement(job_1.nb_op)
        parent_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
        parent_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
        initial_pop = [parent_1, parent_2]
        flowshop = Flowshop(5, 5)
        new_pop = crossover(flowshop, initial_pop, 0.5, 0.5, True)
        self.assertEqual(len(initial_pop), len(new_pop))
        for sched in new_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, sched.sequence())


if __name__ == '__main__':
    unittest.main()
