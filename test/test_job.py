import unittest
from src.job import Job


job_1 = Job(1, [1, 1, 1, 1, 10])
job_2 = Job(2, [1, 1, 1, 4, 8])
job_3 = Job(3, [1, 1, 1, 4, 8])
job_2b = Job(2, [1, 1, 1, 4, 8])


class TestJobClassMethods(unittest.TestCase):
    def test_eq(self):
        self.assertNotEqual(job_1, job_2)
        self.assertNotEqual(job_2, job_3)
        self.assertEqual(job_2, job_2b)


if __name__ == '__main__':
    unittest.main()
