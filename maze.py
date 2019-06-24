import matplotlib.pyplot as pyplot
from random import randint, seed


size_x = 10
size_y = 6

#seed(1)


class MazeDrawer:
  
  def __init__(self, size_x, size_y):
    self.__size_x = size_x
    self.__size_y = size_y
  
  
  def drawBackgroundAndBorder(self, ratio = 8):
    self.__drawBackground(ratio)
    self.__drawMazeBorder()


  def drawClosedCell(self, x, y):
    self.__line(x, y + 1, x + 1, y + 1)
    self.__line(x, y, x + 1, y)
    self.__line(x + 1, y, x + 1, y + 1)
    self.__line(x, y, x, y + 1)
  
  
  def drawOpening(self, old_x, old_y, new_x, new_y):  
    if old_x == new_x:
      # only Y changed
      if old_y < new_y:
        self.__clearLine(old_x, old_y + 1, old_x + 1, old_y + 1)
      else:
        self.__clearLine(old_x, old_y, old_x + 1, old_y)
    else:
      # only X changed
      if old_x < new_x:
        self.__clearLine(old_x + 1, old_y, old_x + 1, old_y + 1)
      else:
        self.__clearLine(old_x, old_y, old_x, old_y + 1)


  def __line(self, x1, y1, x2, y2):
    pyplot.plot([x1, x2], [y1, y2], color='white')
  

  def __clearLine(self, x1, y1, x2, y2):
    pyplot.plot([x1, x2], [y1, y2], color='black')


  def __drawBackground(self, ratio):
    scale = max(self.__size_x, self.__size_y) / ratio
    pyplot.figure(figsize=(self.__size_x / scale, self.__size_y / scale))

    #pyplot.xticks([])
    #pyplot.yticks([])
    pyplot.style.use('dark_background')


  def __drawMazeBorder(self):
    self.__line(0, 0, self.__size_x, 0)
    self.__line(0, 0, 0, self.__size_y)
    self.__line(self.__size_x, 0, self.__size_x, self.__size_y)
    self.__line(0, self.__size_y, self.__size_x, self.__size_y)


# True or False if cell was visited, visited[x][y] = False
visitedMaze = [ [ False for y in range( size_y ) ] for x in range( size_x ) ]

# stack of visited cells; each item is [x, y]
visitedCells = []


def visitCell(x, y):
  visitedMaze[x][y] = True
  visitedCells.append([x, y])


class MazeRules:
  
  def __init__(self, size_x, size_y):
    self.__size_x = size_x
    self.__size_y = size_y
  
  def getNextCell(self, x, y):
    validDirections = self.__getValidDirections(x, y)
    
    if len(validDirections) == 0:
      return self.Result.Failure(self)
  
    index = randint(0, len(validDirections) - 1)
    dir = validDirections[index]
    return self.Result.Success(self, dir[0], dir[1])

  
  def __getValidDirections(self, x, y):
    validDirections = []
  
    if (self.__validCell(x, y + 1)):
      validDirections.append([x, y + 1])
    if (self.__validCell(x + 1, y)):
      validDirections.append([x + 1, y])
    if (self.__validCell(x, y - 1)):
      validDirections.append([x, y - 1])
    if (self.__validCell(x - 1, y)):
      validDirections.append([x - 1, y])
  
    return validDirections
  
  
  def __validCell(self, x, y):
    if x < 0 or y < 0:
      return False
    if x >= self.__size_x or y >= self.__size_y:
      return False
    if visitedMaze[x][y]:
      return False
    return True


  class Result:
    def __init__(self, noValidMovement, new_x, new_y):
      self.noValidMovement = noValidMovement
      self.new_x = new_x
      self.new_y = new_y

    @staticmethod
    def Failure(parent):
      return parent.Result(True, -1, -1)
    
    @staticmethod
    def Success(parent, new_x, new_y):
      return parent.Result(False, new_x, new_y)


class FarthestDeadEnd:
  
  def __init__(self, size_x, size_y):
    self.__size_x = size_x
    self.__size_y = size_y
    self.__max_distance = 0
    self.__x = 0
    self.__y = 0
    self.__marker = None

  def drawDeadEnd(self, backing, x, y):
    if not backing:
      distance = len(visitedCells)
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
    distance = len(visitedCells)
    return min(0.4, 0.5 * distance / self.__size_x / self.__size_y)


class StepController:

  def __init__(self, size_x, size_y):
    self.__max_steps = 2 * size_x * size_y
    self.__step = 1

  def progress(self):
    self.__step += 1
    if self.__step > self.__max_steps:
      print('Something went wrong?')


class CurrentCell:
  
  def __init__(self, size_x, size_y, mazeDrawer):
    self.__size_x = size_x
    self.__size_y = size_y
    self.__backing = False

    self.__mazeDrawer = mazeDrawer

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
    visitCell(self.__x, self.__y)
    self.__marker.center = (self.__x + 0.5, self.__y + 0.5)
    self.__marker.radius = self.__getDecreasingRadius()
    #pyplot.savefig('maze\maze_{0:03}.png'.format(steps.step))
  
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
    distance = len(visitedCells)
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


def generateMaze(size_x, size_y, mazeDrawer):

  currentCell = CurrentCell(size_x, size_y, mazeDrawer)
  steps = StepController(size_x, size_y)
  mazeRules = MazeRules(size_x, size_y)
  
  farthestDeadEnd = FarthestDeadEnd(size_x, size_y)
  
  while True:
    currentCell.redraw()

    steps.progress()
    
    nextCell = mazeRules.getNextCell(currentCell.get_x(), currentCell.get_y())
    
    if nextCell.noValidMovement:
      # no direction is possible, go back
      if len(visitedCells) <= 1:
        # no more options - maze is complete
        break
      removeCurrentCellAndIgnoreIt = visitedCells.pop()
      previousCell = visitedCells.pop()
      
      farthestDeadEnd.drawDeadEnd(currentCell.get_backing(), currentCell.get_x(), currentCell.get_y())

      currentCell.goBack(previousCell[0], previousCell[1])

    else:
      currentCell.moveForward(nextCell.new_x, nextCell.new_y)


mazeDrawer = MazeDrawer(size_x, size_y)
mazeDrawer.drawBackgroundAndBorder(8)
generateMaze(size_x, size_y, mazeDrawer)
#pyplot.show()
