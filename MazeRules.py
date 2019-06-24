from random import randint


class MazeRules:
  
  def __init__(self, size_x, size_y):
    self.__size_x = size_x
    self.__size_y = size_y

    # True or False if cell was visited, visited[x][y] = False
    self.__visitedMaze = [ [ False for y in range( size_y ) ] for x in range( size_x ) ]
    
    # stack of visited cells; each item is [x, y]
    self.__visitedCells = []
  
  
  def getPathLength(self):
    return len(self.__visitedCells)


  def visitCell(self, x, y):
    self.__visitedMaze[x][y] = True
    self.__visitedCells.append([x, y])


  def getNextCell(self, x, y):
    validDirections = self.__getValidDirections(x, y)
    
    if len(validDirections) == 0:
      return self.Result.Failure(self)
  
    index = randint(0, len(validDirections) - 1)
    dir = validDirections[index]
    return self.Result.Success(self, dir[0], dir[1])
  

  def getPreviousCell(self):
    if self.getPathLength() <= 1:
      # no more options - maze is complete
      return self.Result.Failure(self)

    removeCurrentCellAndIgnoreIt = self.__visitedCells.pop()
    previousCell = self.__visitedCells.pop()
    return self.Result.Success(self, previousCell[0], previousCell[1])
  

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
    if self.__visitedMaze[x][y]:
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
