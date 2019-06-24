import matplotlib.pyplot as pyplot
from random import randint, seed


size_x = 10
size_y = 6

#seed(1)


scale = max(size_x, size_y) / 8

pyplot.figure(figsize=(size_x/scale, size_y/scale))
#pyplot.xticks([])
#pyplot.yticks([])
pyplot.style.use('dark_background')


def line(x1, y1, x2, y2):
  pyplot.plot([x1, x2], [y1, y2], color='white')

def clearLine(x1, y1, x2, y2):
  pyplot.plot([x1, x2], [y1, y2], color='black')


# maze's border
def drawMazeBorder():
  line(0, 0, size_x, 0)
  line(0, 0, 0, size_y)
  line(size_x, 0, size_x, size_y)
  line(0, size_y, size_x, size_y)


# True or False if cell was visited, visited[x][y] = False
visitedMaze = [ [ False for y in range( size_y ) ] for x in range( size_x ) ]

# stack of visited cells; each item is [x, y]
visitedCells = []


def visitCell(x, y):
  visitedMaze[x][y] = True
  visitedCells.append([x, y])


class MazeRules:
  
  def __init__(self, size_x, size_y):
    self.size_x = size_x
    self.size_y = size_y
  
  def getNextCell(self, x, y):
    validDirections = self.getValidDirections(x, y)
    
    if len(validDirections) == 0:
      return [-1, -1]
  
    dir = randint(0, len(validDirections) - 1)
    return validDirections[dir]

  
  def getValidDirections(self, x, y):
    validDirections = []
  
    if (self.validCell(x, y + 1)):
      validDirections.append([x, y + 1])
    if (self.validCell(x + 1, y)):
      validDirections.append([x + 1, y])
    if (self.validCell(x, y - 1)):
      validDirections.append([x, y - 1])
    if (self.validCell(x - 1, y)):
      validDirections.append([x - 1, y])
  
    return validDirections
  
  
  def validCell(self, x, y):
    if x < 0 or y < 0:
      return False
    if x >= self.size_x or y >= self.size_y:
      return False
    if visitedMaze[x][y]:
      return False
    return True


def drawClosedCell(x, y):
  line(x, y + 1, x + 1, y + 1)
  line(x, y, x + 1, y)
  line(x + 1, y, x + 1, y + 1)
  line(x, y, x, y + 1)


def drawOpening(old_x, old_y, new_x, new_y):  
  if old_x == new_x:
    # only Y changed
    if old_y < new_y:
      clearLine(old_x, old_y + 1, old_x + 1, old_y + 1)
    else:
      clearLine(old_x, old_y, old_x + 1, old_y)
  else:
    # only X changed
    if old_x < new_x:
      clearLine(old_x + 1, old_y, old_x + 1, old_y + 1)
    else:
      clearLine(old_x, old_y, old_x, old_y + 1)


def getDecreasingRadius(distance):
  distance = len(visitedCells)
  """
  assume R1 radius at D1% of max distance, R2 radius at D2% of max distance
  then r = max_distance * b / (x + max_distance * a), where
  a = (R2 * D2 - R1 * D1) / (R1 - R2)
  b = R1 * D1 + R1 * a
  Below I assumed: D1 = 0.5, R1 = 0.1; D2 = 0.05, R2 = 0.4
  """
  max_distance = size_x * size_y
  r = max_distance * 0.24 / (distance + max_distance * 0.4)
  return min(0.4, r)


class FarthestDeadEnd:
  
  def __init__(self, size_x, size_y):
    self.size_x = size_x
    self.size_y = size_y
    self.max_distance = 0
    self.x = 0
    self.y = 0
    self.marker = None

  def drawDeadEnd(self, backing, x, y):
    if not backing:
      distance = len(visitedCells)
      radius = self.getIncreasingRadius(distance)

      dead_end = pyplot.Circle((x + 0.5, y + 0.5), radius=radius, fc='moccasin')
      pyplot.gca().add_patch(dead_end)
      
      if distance > self.max_distance:
        self.max_distance = distance
        self.x = x
        self.y = y
        if not self.marker:
          circle = pyplot.Circle((x + 0.5, y + 0.5), radius=radius, fc='red')
          circle.zorder = 100
          pyplot.gca().add_patch(circle)
          self.marker = circle
        else:
          self.marker.center = (x + 0.5, y + 0.5)
          self.marker.radius = radius

  def getIncreasingRadius(self, distance):
    distance = len(visitedCells)
    return min(0.4, 0.5 * distance / self.size_x / self.size_y)


class StepController:

  def __init__(self, size_x, size_y):
    self.max_steps = 2 * size_x * size_y
    self.step = 1

  def progress(self):
    self.step += 1
    if self.step > self.max_steps:
      print('Something went wrong?')

class CurrentCell:
  
  def __init__(self, size_x, size_y):
    self.size_x = size_x
    self.size_y = size_y
    self.backing = False

    # starting cell
    self.x = randint(0, size_x - 1)
    self.y = randint(0, size_y - 1)

    self.marker = pyplot.Circle((self.x + 0.5, self.y + 0.5), radius=0.4, fc='y')
    pyplot.gca().add_patch(self.marker)
    drawClosedCell(self.x, self.y)

  def redraw(self):
    visitCell(self.x, self.y)
    self.marker.center = (self.x + 0.5, self.y + 0.5)
    self.marker.radius = getDecreasingRadius(len(visitedCells))
    #pyplot.savefig('maze\maze_{0:03}.png'.format(steps.step))
  
  def moveForward(self, new_x, new_y):
    drawClosedCell(new_x, new_y)
    drawOpening(self.x, self.y, new_x, new_y)
    self.x = new_x
    self.y = new_y
    self.backing = False


def generateMaze():

  currentCell = CurrentCell(size_x, size_y)
  steps = StepController(size_x, size_y)
  mazeRules = MazeRules(size_x, size_y)
  
  farthestDeadEnd = FarthestDeadEnd(size_x, size_y)
  
  while True:
    currentCell.redraw()

    steps.progress()
    
    [new_x, new_y] = mazeRules.getNextCell(currentCell.x, currentCell.y)
    
    if new_x == -1:
      # no direction is possible, go back
      if len(visitedCells) <= 1:
        # no more options - maze is complete
        break
      removeCurrentCellAndIgnoreIt = visitedCells.pop()
      previousCell = visitedCells.pop()
      
      farthestDeadEnd.drawDeadEnd(currentCell.backing, currentCell.x, currentCell.y)

      currentCell.x = previousCell[0]
      currentCell.y = previousCell[1]
      currentCell.backing = True

    else:
      currentCell.moveForward(new_x, new_y)


drawMazeBorder()
generateMaze()
#pyplot.show()
