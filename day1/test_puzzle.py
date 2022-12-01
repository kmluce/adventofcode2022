import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo(self):
        demoa = Puzzle("demo_data.txt")
        demoa.parse()
        answer = demoa.solvea()
        self.assertEqual(24000, answer)

    def test_parta(self):
        parta = Puzzle("test_data.txt")
        parta.parse()
        answer = parta.solvea()
        self.assertEqual(68802, answer)

    def test_partb(self):
        parta = Puzzle("test_data.txt")
        parta.parse()
        answer = parta.solveb()
        self.assertEqual(205370, answer)


if __name__ == '__main__':
    unittest.main()