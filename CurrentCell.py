import matplotlib.pyplot as pyplot
from random import randint


class CurrentCell:
  
  def __init__(self, size_x, size_y, mazeDrawer, mazeRules):
    self.__size_x = size_x
    self.__size_y = size_y
    self.__backing = False

    self.__mazeDrawer = mazeDrawer
    self.__mazeRules = mazeRules

    # starting cell
    self.__x = randint(0, size_x - 1)
    self.__y = randint(0, size_y - 1)

    self.__marker = pyplot.Circle((self.__x + 0.5, self.__y + 0.5), radius=0.4, fc='y')
    pyplot.gca().add_patch(self.__marker)
    self.__mazeDrawer.drawClosedCell(self.__x, self.__y)
  
  def get_x(self):
    return self.__x
  
  def get_y(self):
    return self.__y
  
  def get_backing(self):
    return self.__backing

  def redraw(self):
    self.__mazeRules.visitCell(self.__x, self.__y)
    self.__marker.center = (self.__x + 0.5, self.__y + 0.5)
    self.__marker.radius = self.__getDecreasingRadius()
  
  def moveForward(self, new_x, new_y):
    self.__mazeDrawer.drawClosedCell(new_x, new_y)
    self.__mazeDrawer.drawOpening(self.__x, self.__y, new_x, new_y)
    self.__x = new_x
    self.__y = new_y
    self.__backing = False

  def goBack(self, old_x, old_y):
    self.__x = old_x
    self.__y = old_y
    self.__backing = True

  def __getDecreasingRadius(self):
    distance = self.__mazeRules.getPathLength()
    """
    assume R1 radius at D1% of max distance, R2 radius at D2% of max distance
    then r = max_distance * b / (x + max_distance * a), where
    a = (R2 * D2 - R1 * D1) / (R1 - R2)
    b = R1 * D1 + R1 * a
    Below I assumed: D1 = 0.5, R1 = 0.1; D2 = 0.05, R2 = 0.4
    """
    max_distance = self.__size_x * self.__size_y
    r = max_distance * 0.24 / (distance + max_distance * 0.4)
    return min(0.4, r)
