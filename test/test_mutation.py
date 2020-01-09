import unittest
from mutation import mutation, mutation_insert, mutation_swap
from flowshop import Flowshop
from job import Job
from ordonnancement import Ordonnancement

flow_shop = Flowshop(5, 5)
job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])
scheduling_1 = Ordonnancement(job_1.nb_op)
scheduling_2 = Ordonnancement(job_1.nb_op)
scheduling_3 = Ordonnancement(job_1.nb_op)
scheduling_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
scheduling_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
scheduling_3.ordonnancer_liste_job([job_5, job_4, job_3, job_2, job_1])
initial_pop = [scheduling_1, scheduling_2, scheduling_3]


class TestMutationFileMethods(unittest.TestCase):
    def test_mutation_swap(self):
        new_pop = mutation_swap(flow_shop, initial_pop, mutation_probability=1.0)
        self.assertEqual(len(initial_pop), len(new_pop))
        for scheduling in new_pop:
            self.assertEqual(len(scheduling.sequence()), 5)
            self.assertEqual(scheduling.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, scheduling.sequence())

    def test_mutation_insert(self):
        new_pop = mutation_insert(flow_shop, initial_pop, mutation_probability=1.0)
        self.assertEqual(len(initial_pop), len(new_pop))
        for scheduling in new_pop:
            self.assertEqual(len(scheduling.sequence()), 5)
            self.assertEqual(scheduling.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, scheduling.sequence())

    def test_mutation(self):
        new_pop = mutation(flow_shop, initial_pop, mutation_swap_probability=1.0, mutation_insert_probability=1.0)
        self.assertEqual(len(initial_pop), len(new_pop))
        for sched in new_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in [job_1, job_2, job_3, job_4, job_5]:
                self.assertIn(job, sched.sequence())


if __name__ == '__main__':
    unittest.main()
