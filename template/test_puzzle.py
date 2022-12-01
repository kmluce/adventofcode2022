import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo_part_a(self):
        demoa = Puzzle("demo_data.txt")
        demoa.parse()
        answer = demoa.solvea()
        self.assertEqual(24000, answer)

#    def test_part_a(self):
#        parta = Puzzle("test_data.txt")
#        parta.parse()
#        answer = parta.solvea()
#        self.assertEqual(68802, answer)
#
#    def test_demo_part_b(self):
#        demoa = Puzzle("demo_data.txt")
#        demoa.parsb()
#        answer = demoa.solveb()
#        self.assertEqual(24000, answer)
#
#
#    def test_part_b(self):
#        parta = Puzzle("test_data.txt")
#        parta.parse()
#        answer = parta.solveb()
#        self.assertEqual(205370, answer)


if __name__ == '__main__':
    unittest.main()