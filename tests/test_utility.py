import unittest


class SampleTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(2, 1 + 1)

    @unittest.skip("demonstare skipped test case")
    def test_2(self):
        self.assertEqual(1, 2 - 1)
