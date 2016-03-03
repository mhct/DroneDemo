import unittest

from Obstacle import Obstacle
from Environment import Environment
from Helper import Point


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.env = Environment(4, 4, 100, 100)  # size_x size_y res_x res_y

    def test_add_obstacle(self):
        obstacle = Obstacle("obstacles/test_obstacle1.txt")
        self.env.add_obstacle(obstacle)

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 350, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_in_obstacle_region(Point(50, 150, 1)))

    def test_add_two_obstacles(self):
        obstacle1 = Obstacle("obstacles/test_obstacle1.txt")
        obstacle2 = Obstacle("obstacles/test_obstacle2.txt")
        self.env.add_obstacle(obstacle1)
        self.env.add_obstacle(obstacle2)

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 50, 1999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 50, 2001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 350, 1999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 350, 2001)))

    def test_remove_obstacle_case1(self):
        obstacle = Obstacle("obstacles/test_obstacle1.txt")
        self.env.add_obstacle(obstacle)
        self.env.remove_obstacle(obstacle.get_id())

        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 150, 500)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 250, 500)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 350, 500)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(50, 150, 500)))

    def test_remove_obstacle_case2(self):
        obstacle1 = Obstacle("obstacles/test_obstacle1.txt")
        obstacle2 = Obstacle("obstacles/test_obstacle2.txt")
        self.env.add_obstacle(obstacle1)
        self.env.add_obstacle(obstacle2)
        self.env.remove_obstacle(obstacle2.get_id())

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_obstacle_region(Point(150, 350, 999)))
        self.assertFalse(self.env.is_in_obstacle_region(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_in_obstacle_region(Point(50, 150, 1)))


if __name__ == '__main__':
    unittest.main()
