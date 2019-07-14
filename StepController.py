class StepController:

  def __init__(self, size_x, size_y):
    self.__max_steps = 2 * size_x * size_y
    self.__step = 1

  def progress(self):
    self.__step += 1
    if self.__step > self.__max_steps:
      print('Something went wrong?')

  def get_step(self):
    return self.__step
