import minesweeper
import solver
import time

m = minesweeper.Minesweeper(16, 30, 99)
s = solver.Solver()
m.Display()

while True:
  move = raw_input("Enter a move as (column, row): ")
  if move == "auto":
    while True:
      [column, row] = s.GetNextMove(m.board)
      result = m.Probe(column, row)
      if result == 1:
        print "\r\n\r\n-----------\r\n You win!\r\n-----------\r\n"
        quit()
      elif result == -1:
        print "\r\n\r\n---------------\r\n You lose...\r\n---------------\r\n"
        quit()
  else:
    splitmove = move.split(", ")
    column = int(splitmove[0][1:])
    row = int(splitmove[1][:-1])
    m.Probe(column, row)