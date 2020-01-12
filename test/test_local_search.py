import unittest
import copy
from job import Job
from ordonnancement import Ordonnancement
from flowshop import Flowshop
from local_search import local_search_swap, local_search_insert, swap

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
initial_scheduling = Ordonnancement(job_1.nb_op)
initial_scheduling.ordonnancer_liste_job([job_1, job_2, job_3, job_4, job_5])


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

    def test_swap_neighborhood(self):
        nb_jobs = flow_shop.nombre_jobs()
        expected_size_neighborhood = 10
        computed_size_neighborhood = nb_jobs * (nb_jobs - 1) / 2
        expected_neighborhood = [
            [job_2, job_1, job_3, job_4, job_5],
            [job_3, job_2, job_1, job_4, job_5],
            [job_4, job_2, job_3, job_1, job_5],
            [job_5, job_2, job_3, job_4, job_1],
            [job_1, job_3, job_2, job_4, job_5],
            [job_1, job_4, job_3, job_2, job_5],
            [job_1, job_5, job_3, job_4, job_2],
            [job_1, job_2, job_4, job_3, job_5],
            [job_1, job_2, job_5, job_4, job_3],
            [job_1, job_2, job_3, job_5, job_4]
        ]
        # The way to compute the swap neighborhood is the same as in the function local_search_swap function
        computed_neighborhood = []
        for i in range(0, nb_jobs - 1):
            for j in range(i + 1, nb_jobs):
                temp = copy.copy(initial_scheduling)
                computed_neighborhood.append(swap(i, j, temp).sequence())
        self.assertEqual(expected_size_neighborhood, computed_size_neighborhood)
        self.assertEqual(expected_size_neighborhood, len(expected_neighborhood))
        self.assertEqual(expected_size_neighborhood, len(computed_neighborhood))
        self.assertEqual(expected_neighborhood, computed_neighborhood)

    def test_insert_neighborhood(self):
        nb_jobs = flow_shop.nombre_jobs()
        expected_size_neighborhood = 16
        computed_size_neighborhood = (nb_jobs - 1) * (nb_jobs - 1)
        expected_neighborhood = [
            [job_2, job_1, job_3, job_4, job_5],
            [job_2, job_3, job_1, job_4, job_5],
            [job_2, job_3, job_4, job_1, job_5],
            [job_2, job_3, job_4, job_5, job_1],
            [job_1, job_3, job_2, job_4, job_5],
            [job_1, job_3, job_4, job_2, job_5],
            [job_1, job_3, job_4, job_5, job_2],
            [job_3, job_1, job_2, job_4, job_5],
            [job_1, job_2, job_4, job_3, job_5],
            [job_1, job_2, job_4, job_5, job_3],
            [job_4, job_1, job_2, job_3, job_5],
            [job_1, job_4, job_2, job_3, job_5],
            [job_1, job_2, job_3, job_5, job_4],
            [job_5, job_1, job_2, job_3, job_4],
            [job_1, job_5, job_2, job_3, job_4],
            [job_1, job_2, job_5, job_3, job_4]
        ]
        # The way to compute the swap neighborhood is the same as in the function local_search_insert function
        computed_neighborhood = []
        for i in range(0, nb_jobs):
            for j in range(0, nb_jobs):
                if j != i and (j != i-1 or i == 0):
                    temp = copy.copy(initial_scheduling)
                    sequence = temp.sequence().copy()
                    ls_insert = sequence[i]
                    sequence.remove(ls_insert)
                    sequence.insert(j, ls_insert)
                    computed_neighborhood.append(sequence)

        self.assertEqual(expected_size_neighborhood, computed_size_neighborhood)
        self.assertEqual(expected_size_neighborhood, len(expected_neighborhood))
        self.assertEqual(expected_size_neighborhood, len(computed_neighborhood))
        self.assertEqual(expected_neighborhood, computed_neighborhood)


if __name__ == '__main__':
    unittest.main()
