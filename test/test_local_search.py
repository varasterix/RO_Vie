import unittest
from job import Job
from ordonnancement import Ordonnancement
from flowshop import Flowshop
from local_search import local_search_swap, local_search_insert

job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])
flow_shop = Flowshop(5, 5)
scheduling_1 = Ordonnancement(job_1.nb_op)
scheduling_2 = Ordonnancement(job_2.nb_op)
scheduling_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
scheduling_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])


class TestSolutionLocalSearchClassMethods(unittest.TestCase):
    def test_duration_ls_swap(self):
        new_scheduling_1 = local_search_swap(flow_shop, scheduling_1, 20)
        new_scheduling_2 = local_search_swap(flow_shop, scheduling_2, 20)
        self.assertTrue(new_scheduling_1.duree() <= scheduling_1.duree())
        self.assertTrue(new_scheduling_2.duree() <= scheduling_2.duree())
        self.assertEqual(len(new_scheduling_1.sequence()), 5)
        self.assertEqual(len(new_scheduling_2.sequence()), 5)
        for job in [job_1, job_2, job_3, job_4, job_5]:
            self.assertIn(job, new_scheduling_1.sequence())
            self.assertIn(job, new_scheduling_2.sequence())

    def test_duration_ls_insert(self):
        new_scheduling_1 = local_search_insert(flow_shop, scheduling_1, 20)
        new_scheduling_2 = local_search_insert(flow_shop, scheduling_2, 20)
        self.assertTrue(new_scheduling_1.duree() <= scheduling_1.duree())
        self.assertTrue(new_scheduling_2.duree() <= scheduling_2.duree())
        self.assertEqual(len(new_scheduling_1.sequence()), 5)
        self.assertEqual(len(new_scheduling_2.sequence()), 5)
        for job in [job_1, job_2, job_3, job_4, job_5]:
            self.assertIn(job, new_scheduling_1.sequence())
            self.assertIn(job, new_scheduling_1.sequence())


if __name__ == '__main__':
    unittest.main()
