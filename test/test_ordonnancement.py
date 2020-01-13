import unittest
from src.ordonnancement import Ordonnancement
from src.job import Job

job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])
ord_1 = Ordonnancement(job_1.nb_op)
ord_2 = Ordonnancement(job_1.nb_op)
ord_3 = Ordonnancement(job_1.nb_op)
ord_1.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])
ord_2.ordonnancer_liste_job([job_1, job_4, job_5, job_2, job_3])
ord_3.ordonnancer_liste_job([job_2, job_3, job_4, job_5, job_1])


class TestOrdonnancementClassMethods(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(ord_1, ord_3)
        self.assertNotEqual(ord_1, ord_2)


if __name__ == '__main__':
    unittest.main()
