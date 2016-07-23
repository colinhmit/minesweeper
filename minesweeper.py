from board import Board
import random

class Minesweeper:
  def __init__(self, width, height, num_bombs):
    self.width = width
    self.height = height
    self.num_bombs = num_bombs

    if num_bombs >= self.width*self.height:
      print "Too many bombs for this size of a board."
      self.valid = False
    else:
      self.valid = True

    self.board = Board(self.width, self.height)

    self.active = False

  def Probe(self, x, y):
    if not self.active:
      self.SpawnBombs(x, y)
      self.MakeBoard()
      self.active = True
    cell = self.board.GetCell(x, y)
    if cell == -2:
      return -1
    self.Reveal(x, y)
    if self.WonGame():
      return 1
    self.Display()
    return 0

  def WonGame(self):
    for i in range(self.width):
      for j in range(self.height):
        if self.board.GetCell(i, j) == -1:
          return False

    return True

  def Reveal(self, x, y):
    if self.board.GetCell(x, y) != -1:
      return

    adjacents = self.board.GetAdjacents(x, y)
    count = 0
    for adjacent in adjacents:
      acell = self.board.GetCell(adjacent[0], adjacent[1])
      if acell == -2:
        count += 1
    self.board.SetCell(x, y, count)

    if count == 0:
      for adjacent in adjacents:
        if adjacent[0] == x or adjacent[1] == y:
          self.Reveal(adjacent[0], adjacent[1])

  def SpawnBombs(self, immuneX, immuneY):
    self.bomb_locations = []
    random.seed()
    for i in range(self.num_bombs):
      while(True):
        x_pos = random.randint(0, self.width-1)
        y_pos = random.randint(0, self.height-1)
        if ([x_pos, y_pos] not in self.bomb_locations) and (abs(x_pos-immuneX) > 1 or abs(y_pos-immuneY) > 1):
          self.bomb_locations.append([x_pos, y_pos])
          break

  def MakeBoard(self):
    for loc in self.bomb_locations:
      self.board.SetCell(loc[0], loc[1], -2)

  def Display(self):
    print self.board.RepString()