import matplotlib.pyplot as pyplot


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

  def saveFrame(self, step):
    pyplot.savefig('maze\\maze_{0:03}.png'.format(step))

  def __line(self, x1, y1, x2, y2):
    pyplot.plot([x1, x2], [y1, y2], color='white')
  

  def __clearLine(self, x1, y1, x2, y2):
    pyplot.plot([x1, x2], [y1, y2], color='black')


  def __drawBackground(self, ratio):
    scale = max(self.__size_x, self.__size_y) / ratio / 2
    pyplot.figure(figsize=(self.__size_x / scale, self.__size_y / scale))

    pyplot.rcParams['font.size'] = 20

    #pyplot.xticks([])
    #pyplot.yticks([])
    pyplot.style.use('dark_background')


  def __drawMazeBorder(self):
    self.__line(0, 0, self.__size_x, 0)
    self.__line(0, 0, 0, self.__size_y)
    self.__line(self.__size_x, 0, self.__size_x, self.__size_y)
    self.__line(0, self.__size_y, self.__size_x, self.__size_y)
