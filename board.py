class Board:
  def __init__(self, width, height):
    self.cells = []
    self.width = width
    self.height = height
    for i in range(width):
      column = []
      for j in range(height):
        column.append(-1)
      self.cells.append(column)

  def GetCell(self, x, y):
    return self.cells[x][y]

  def GetAdjacents(self, x, y):
    adjacents = []
    for ip in range(-1, 2):
      adj_i = ip+x
      for jp in range(-1, 2):
        adj_j = jp+y
        if adj_i >= 0 and adj_i < self.GetWidth():
          if adj_j >= 0 and adj_j < self.GetHeight():
            if adj_i != x or adj_j != y:
              adjacents.append([adj_i, adj_j])
    return adjacents

  def GetUnknownAdjacents(self, x, y):
    uadjacents = []
    for adjacent in self.GetAdjacents(x, y):
      if self.GetCell(adjacent[0], adjacent[1]) < 0:
        uadjacents.append(adjacent)

    return uadjacents

  def SetCell(self, x, y, value):
    self.cells[x][y] = value

  def GetWidth(self):
    return self.width

  def GetHeight(self):
    return self.height

  def RepString(self, debug = False):
    spacerString = '-'*4*self.width
    rstring = ""
    for j in range(self.height):
      for i in range(self.width):
        if debug == True and self.cells[i][j] == -2:
          rcell = " X "
        elif self.cells[i][j] < 0:
          rcell = "[ ]"
        elif self.cells[i][j] == 0:
          rcell = "   "
        else:
          rcell = " " + str(self.cells[i][j]) + " "
        rstring += "|" + rcell
      rstring += "\r\n" + spacerString
      rstring += "\r\n"
    return rstring