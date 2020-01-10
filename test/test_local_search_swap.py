
import unittest
from job import Job
from ordonnancement import Ordonnancement
from flowshop import Flowshop
from local_search import local_search_swap

job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])


class TestSolutionLocalSearchClassMethods(unittest.TestCase):
    def test_duration(self):
        flowshop = Flowshop(5, 5)
        sched_1 = Ordonnancement(job_1.nb_op)
        sched_2 = Ordonnancement(job_2.nb_op)
        sched_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
        sched_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
        sched_1duree = sched_1.duree()
        sched_2duree = sched_2.duree()
        new_sched1 = local_search_swap(flowshop, sched_2, 20)
        new_sched1_duree = new_sched1.duree()
        self.assertTrue(new_sched1.duree() < sched_2.duree())
        self.assertEqual(len(new_sched1.sequence()), 5)
        for job in [job_1, job_2, job_3, job_4, job_5]:
            self.assertIn(job, new_sched1.sequence())


if __name__ == '__main__':
    unittest.main()
