import unittest
from job import Job
from flowshop import Flowshop

job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [2, 1, 3, 5, 1])
job_4 = Job(4, [2, 5, 5, 3, 3])
job_5 = Job(5, [1, 1, 3, 7, 1])
l_job = [job_1, job_2, job_3, job_4, job_5]
flowshop_1 = Flowshop(5, 5, l_job)


class MyTestCase(unittest.TestCase):
    def test_job_duration_order_asc(self):
        self.assertEqual(True, False)
        #TODO


if __name__ == '__main__':
    unittest.main()
