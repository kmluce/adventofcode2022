import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo_part_a(self):
        demoa = Puzzle("demo_data.txt", "a")
        demoa.parse()
        answer = demoa.solve()
        self.assertEqual(7, answer)

    def test_part_a(self):
        parta = Puzzle("test_data.txt", "a")
        parta.parse()
        answer = parta.solve()
        self.assertEqual(1953, answer)

    def test_demo_part_b(self):
        demob = Puzzle("demo_data.txt", "b")
        demob.parse()
        answer = demob.solve()
        self.assertEqual(19, answer)

    def test_part_b(self):
        partb = Puzzle("test_data.txt", "b")
        partb.parse()
        answer = partb.solve()
        self.assertEqual(2301, answer)

if __name__ == '__main__':
    unittest.main()