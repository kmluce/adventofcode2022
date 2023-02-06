import unittest
from puzzle import Puzzle


class MyTestCase(unittest.TestCase):
    def test_demo_part_a(self):
        demo_a = Puzzle("demo_data.txt", "a", 1)
        answer = demo_a.solve()
        self.assertEqual(26, answer)

    def test_part_a(self):
        part_a = Puzzle("test_data.txt", "a", 1)
        answer = part_a.solve()
        self.assertEqual(4665948, answer)

    def test_demo_part_b(self):
        demo_b = Puzzle("demo_data.txt", "b", 2)
        answer = demo_b.solve()
        self.assertEqual(56000011, answer)

    def test_part_b(self):
        part_b = Puzzle("test_data.txt", "b", 1)
        answer = part_b.solve()
        self.assertEqual(13543690671045, answer)


if __name__ == '__main__':
    unittest.main()
