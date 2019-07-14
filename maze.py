from random import randint, seed

from MazeDrawer import MazeDrawer
from MazeRules import MazeRules
from FarthestDeadEnd import FarthestDeadEnd
from StepController import StepController
from CurrentCell import CurrentCell


#seed(1)


def generateMaze(size_x, size_y):

  mazeDrawer = MazeDrawer(size_x, size_y)
  mazeDrawer.drawBackgroundAndBorder(8)

  mazeRules = MazeRules(size_x, size_y)
  currentCell = CurrentCell(size_x, size_y, mazeDrawer, mazeRules)
  steps = StepController(size_x, size_y)
  
  farthestDeadEnd = FarthestDeadEnd(size_x, size_y, mazeRules)
  
  while True:
    currentCell.redraw()

    # create 'maze' subfolder before running
    mazeDrawer.saveFrame(steps.get_step())

    steps.progress()
    
    nextCell = mazeRules.getNextCell(currentCell.get_x(), currentCell.get_y())
    
    if nextCell.noValidMovement:
      # no direction is possible, go back
      previousCell = mazeRules.getPreviousCell()

      if previousCell.noValidMovement:
        # no more options - maze is complete
        break
      else:
        farthestDeadEnd.drawDeadEnd(currentCell.get_backing(), currentCell.get_x(), currentCell.get_y())
        currentCell.goBack(previousCell.new_x, previousCell.new_y)

    else:
      currentCell.moveForward(nextCell.new_x, nextCell.new_y)


generateMaze(20,10)
