import matplotlib.pyplot as pyplot


class FarthestDeadEnd:
  
  def __init__(self, size_x, size_y, mazeRules):
    self.__size_x = size_x
    self.__size_y = size_y
    self.__max_distance = 0
    self.__x = 0
    self.__y = 0
    self.__marker = None
    self.__mazeRules = mazeRules

  def drawDeadEnd(self, backing, x, y):
    if not backing:
      distance = self.__mazeRules.getPathLength()
      radius = self.__getIncreasingRadius(distance)

      dead_end = pyplot.Circle((x + 0.5, y + 0.5), radius=radius, fc='moccasin')
      pyplot.gca().add_patch(dead_end)
      
      if distance > self.__max_distance:
        self.__max_distance = distance
        self.__x = x
        self.__y = y
        if not self.__marker:
          circle = pyplot.Circle((x + 0.5, y + 0.5), radius=radius, fc='red')
          circle.zorder = 100
          pyplot.gca().add_patch(circle)
          self.__marker = circle
        else:
          self.__marker.center = (x + 0.5, y + 0.5)
          self.__marker.radius = radius

  def __getIncreasingRadius(self, distance):
    return min(0.4, 0.5 * distance / self.__size_x / self.__size_y)
