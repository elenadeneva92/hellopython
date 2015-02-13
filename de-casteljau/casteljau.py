#!/user/bin/env python
"""Implementation De Casteljau's algorithm """

import math
import pygame
import random


class Point:
    """Represnation of 2D point"""

    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def split(self, coef, end_point):
        """Return a new point spliting the segment
        formed by the points in proportion of \"coef\""""
        x_coord = self.x_coord + (end_point.x_coord - self.x_coord) * coef
        y_coord = self.y_coord + (end_point.y_coord - self.y_coord) * coef
        return Point(x_coord, y_coord)

    def distance(self, end):
        """Return the distance between the points"""
        dist_y = self.x_coord - end.x_coord
        dist_x = self.y_coord - end.y_coord
        return math.sqrt(dist_y * dist_y + dist_x * dist_x)

    def as_list(self, func_x, func_y):
        """Return the point's coordinates as list"""
        return [func_x(self.x_coord), func_y(self.y_coord)]

    def as_str(self):
        """Return the point in string fromat"""
        return "[" + str(self.x_coord) + ", " + str(self.y_coord) + "]"


class DeCasteljau:
    """Implementation of DeCasteljau algorithm"""
    def __init__(self):
        self.points = []
        self.precision = 0
        self.coef = 0
        self.result = []

    def set_points(self, points):
        """Sets the points to define the curve"""
        self.points = [points]

    def set_coef(self, coef):
        """Sets the coeficient to split a line to produce new point"""
        self.coef = coef

    def run(self):
        """Finds all the points from the curve"""
        for k in range(0, len(self.points[0]) - 1):
            next_level_points = []
            for i in range(0, len(self.points[k]) - 1):
                begin_point = self.points[k][i]
                end_point = self.points[k][i + 1]
                new_point = begin_point.split(self.coef, end_point)
                next_level_points.append(new_point)
            count = " Count " + str(len(next_level_points)) + " "
            self.points.append(next_level_points)

    def iteration_count(self):
        """return the number iteration that should be performed"""
        return len(self.points)

    def points_after_iteration(self, iteration):
        """Returns all the points returned after iteration"""
        return self.points[iteration]

    def get_result(self):
        """Returns the point of the curve"""
        if len(self.result) == 0:
            self.result = []
            for i in range(0, len(self.points)):
                self.result.append(self.points[i][0])
            for i in range(0, len(self.points)):
                self.result.append(self.points[self.precision - 1 - i][i])

        print("LLL {}".format(self.result))
        return self.result


def rand_color():
    """ Return random valid color value betwwen [0 and 255]"""
    return int(random.random() * 255)


def transform(a, b):
    """ Move x -> a * x + b """
    return lambda x: a + x * b


class Bezier:
    """Find Bezier curve points iterating de Casteljau's algorithm"""
    def __init__(self):
        self.points = []
        self.result = []
        self.precision = 0
        self.coef = 0

    def set_points(self, points):
        """Sets the points to define the curve"""
        self.points = points

    def set_coef(self, coef):
        """Sets the coeficient to split a line to produce new point"""
        self.coef = coef

    def set_precision(self, precision):
        """ Set how many iteration to use de Casteljau's algorithm"""
        self.precision = precision

    def run(self):
        i = 0
        while i <= 1:
            algorithm = DeCasteljau()
            algorithm.set_coef(i)
            algorithm.set_points(self.points)
            algorithm.run()
            points = algorithm.points_after_iteration(len(self.points)-1)
            point = points[0]
            self.result.append(point)
            i += self.precision
        return self.result

    def points_after_iteration(self, i):
        return self.result

    def iteration_count(self):
        return 1


class UI:
    """Simple ui reading and wriging to console"""

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.factor = 100

    def read(self):
        """Read the inputs from the console"""
        points_count = input("Enter count of point: ")
        points = []
        for _ in range(0, int(points_count)):
            x_coord = input("Enter x coordinate: ")
            y_coord = input("Enter y coordinate: ")
            points.append(Point(int(x_coord), int(y_coord)))
        self.algorithm.set_points(points)

    def write(self):
        """Show the curve"""
        self.algorithm.run()
        iteration = self.algorithm.points_after_iteration(0)
        max_x = self.factor * max([item.x_coord for item in iteration])
        max_y = self.factor * max([item.y_coord for item in iteration])
        size = [int(max_x)+10, int(max_y)+10]

        pygame.init()
        screen = pygame.display.set_mode(size)

        for i in range(0, self.algorithm.iteration_count()):
            points = self.algorithm.points_after_iteration(i)
            color = (rand_color(), rand_color(), rand_color())
            for j in range(1, len(points)):
                scale_x = transform(0, self.factor)
                scale_y = transform(max_y, - self.factor)
                start = points[j-1].as_list(scale_x, scale_y)
                end = points[j].as_list(scale_x, scale_y)
                pygame.draw.line(screen, color, start, end, 5)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break


def main():
    """start main"""
    algorithm = Bezier()
    algorithm.set_precision(0.01)
    application = UI(algorithm)
    application.read()
    application.write()

if __name__ == '__main__':
    main()
