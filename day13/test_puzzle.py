import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo_part_a(self):
        demo_a = Puzzle("demo_data.txt", "a", 1)
        demo_a.parse()
        answer = demo_a.solve()
        self.assertEqual(13, answer)

    def test_part_a(self):
        part_a = Puzzle("test_data.txt", "a", 1)
        part_a.parse()
        answer = part_a.solve()
        self.assertEqual(5684, answer)

    def test_demo_part_b(self):
        demo_b = Puzzle("demo_data.txt", "b", 1)
        demo_b.parse()
        answer = demo_b.solve()
        self.assertEqual(140, answer)

    def test_part_b(self):
        part_b = Puzzle("test_data.txt", "b", 1)
        part_b.parse()
        answer = part_b.solve()
        self.assertEqual(22932, answer)


if __name__ == '__main__':
    unittest.main()
