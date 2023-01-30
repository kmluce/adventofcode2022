import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo_part_a(self):
        demo_a = Puzzle("demo_data.txt", "a", 0)
        demo_a.parse()
        answer = demo_a.solve()
        self.assertEqual(24, answer)

    def test_part_a(self):
        part_a = Puzzle("test_data.txt", "a", 0)
        part_a.parse()
        answer = part_a.solve()
        self.assertEqual(745, answer)

    def test_demo_part_b(self):
        demo_b = Puzzle("demo_data.txt", "b", 0)
        demo_b.parse()
        answer = demo_b.solve()
        self.assertEqual(93, answer)

    def test_part_b(self):
        part_b = Puzzle("test_data.txt", "b", 0)
        part_b.parse()
        answer = part_b.solve()
        self.assertEqual(-1, answer)


if __name__ == '__main__':
    unittest.main()
