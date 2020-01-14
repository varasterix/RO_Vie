import unittest
from src import initial_population as ip
from src.job import Job
from src.flowshop import Flowshop
from src.ordonnancement import Ordonnancement

MAXINT = 10000


job_1 = Job(1, [3, 2, 1, 2, 10])
job_2 = Job(2, [8, 4, 0, 2, 8])
job_3 = Job(3, [12, 1, 7, 5, 2])
job_4 = Job(4, [2, 5, 9, 3, 3])
job_5 = Job(5, [1, 3, 1, 1, 1])
l_job = [job_1, job_2, job_3, job_4, job_5]
flowshop_1 = Flowshop(5, 5, l_job)
flowshop_2 = Flowshop()
flowshop_2.definir_par("data\\dataset3\\jeu2.txt")

seq_1 = [job_3, job_1, job_5, job_2, job_4]
seq_2 = [job_1, job_2, job_4, job_3, job_5]
seq_3 = [job_1, job_4, job_3, job_2, job_5]


class MyTestCase(unittest.TestCase):
    def test_initial_pop(self):
        size = 150
        init_pop = ip.initial_pop(flowshop_1, 0.5, 0.5, False, size)
        for sched in init_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in flowshop_1.l_job:
                self.assertIn(job, sched.sequence())

    def test_is_population_size_correct(self):
        self.assertEqual(ip.is_population_size_correct(4, 12), True)
        self.assertEqual(ip.is_population_size_correct(5, 176), False)

    def test_random_initial_pop(self):
        rdm_size = 100
        rdm_pop = ip.random_initial_pop(flowshop_1, rdm_size)
        self.assertEqual(len(rdm_pop), rdm_size)
        for sched in rdm_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in flowshop_1.l_job:
                self.assertIn(job, sched.sequence())

    def test_deterministic_initial_pop_rdm(self):
        deter_size = 12
        deter_pop = ip.deterministic_initial_pop(flowshop_1, deter_size, False)
        self.assertEqual(len(deter_pop), deter_size)
        for sched in deter_pop:
            self.assertEqual(len(sched.sequence()), 5)
            self.assertEqual(sched.has_duplicate(), False)
            for job in flowshop_1.l_job:
                self.assertIn(job, sched.sequence())

    def test_deterministic_initial_pop_best(self):
        deter_size = 5
        deter_pop = ip.deterministic_initial_pop(flowshop_2, deter_size, True)
        self.assertEqual(len(deter_pop), deter_size)
        min = MAXINT
        for sched in deter_pop:
            self.assertEqual(len(sched.sequence()), 8)
            self.assertEqual(sched.has_duplicate(), False)
            for job in flowshop_2.l_job:
                self.assertIn(job, sched.sequence())
            if sched.duree() < min:
                min = sched.duree()
        score_neh = 705
        self.assertGreaterEqual(score_neh, min)

    def test_neh_order(self):
        seq = ip.neh_order(flowshop_2)
        sched = Ordonnancement(flowshop_2.nb_machines)
        sched.ordonnancer_liste_job(seq)
        self.assertEqual(sched.duree(), 705)

    def test_johnson_rule_order(self):
        seq = ip.johnson_rule_order(flowshop_1, 2)
        self.assertEqual(seq, seq_3)

    def test_job_duration_order_asc(self):
        seq = ip.job_duration_order_asc(flowshop_1, 1)
        self.assertEqual(seq, seq_1)

    def test_job_duration_order_desc(self):
        seq = ip.job_duration_order_desc(flowshop_1, 4)
        self.assertEqual(seq, seq_2)


if __name__ == '__main__':
    unittest.main()
