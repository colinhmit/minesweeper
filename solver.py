import copy

class Solver:
  def __init__(self):
    pass

  def ProbBoardPass(self, board, old_board):
    new_board = copy.deepcopy(old_board)

    for i in range(board.GetWidth()):
      for j in range(board.GetHeight()):
        num_bombs = board.GetCell(i, j)
        if num_bombs > 0:
          adjacents = board.GetUnknownAdjacents(i, j)
          num_adjacents = len(adjacents)
          if num_adjacents == 0:
            continue
          elif num_adjacents == num_bombs:
            for adjacent in adjacents:
              new_board[adjacent[0]][adjacent[1]] = 1
          else:
            accounted_for = 0
            for adjacent in adjacents:
              if new_board[adjacent[0]][adjacent[1]] == 1:
                accounted_for += 1
            p = (float(num_bombs-accounted_for))/num_adjacents
            for adjacent in adjacents:
              if new_board[adjacent[0]][adjacent[1]] != 1:
                if new_board[adjacent[0]][adjacent[1]] == -1:
                  new_board[adjacent[0]][adjacent[1]] = p
                else: 
                  #09/20/16 10:01PM changed from min
                  new_board[adjacent[0]][adjacent[1]] = min(p, new_board[adjacent[0]][adjacent[1]])
    return new_board

  def BuildProbBoard(self, board):
    # Build probability board
    old_board = []
    for i in range(board.GetWidth()):
      column = []
      for j in range(board.GetHeight()):
        if board.GetCell(i, j) >= 0:
          column.append(0)
        else:
          column.append(-1)
      old_board.append(column)

    while(True):
      new_board = self.ProbBoardPass(board, old_board)
      if new_board == old_board:
        break
      old_board = new_board
    return new_board

  def GetNextMove(self, board):
    p = self.BuildProbBoard(board)

    minMoveScore = 1
    minMoves = []
    isopen = False
    bombs_found = 0
    covered_cells = 0
    for i in range(board.GetWidth()):
      for j in range(board.GetHeight()):
        if p[i][j] == 1:
          bombs_found += 1
        if board.GetCell(i, j) == -1:
          covered_cells += 1
        if p[i][j] != -1 and board.GetCell(i, j) == -1:
          isopen = True
          if (p[i][j] == minMoveScore) & (minMoveScore == 0):
            minMoves.append([i, j])
          elif p[i][j] < minMoveScore:
            minMoveScore = p[i][j]
            minMoves = [[i, j]]

    if not isopen:
      minMoves = [[board.GetWidth()/2, board.GetHeight()/2]]
    print minMoveScore
    return (minMoves, bombs_found, covered_cells)

  def Display(self, fullboard, pboard):
    spacerString = '-'*4*fullboard.GetWidth()
    rstring = ""
    for j in range(fullboard.GetHeight()):
      for i in range(fullboard.GetWidth()):
        if pboard[i][j] < 0:
          rcell = "   "
        else:
          rcell = "%.1f" % pboard[i][j]
        rstring += "|" + rcell
      rstring += "\r\n" + spacerString
      rstring += "\r\n"
    print rstring