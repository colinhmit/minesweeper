# -*- coding: utf-8 -*-
"""
Created on Wed May 27 20:40:52 2015

@author: colinh
"""
import time
import random
import board
import solver
import cProfile
import re
from selenium import webdriver

class TAS:
    def __init__(self):
        #select the headless web browser (whatever is installed)
        driver = webdriver.Firefox()

        driver.get('http://minesweeperonline.com/#')
        
        self.solve(driver)
        #cProfile.runctx("self.solve(driver)", globals(),locals())#

    def solve(self, driver):
        s = solver.Solver()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        clickBoard = self.load_board(driver, soup)
        while(True):
            b = self.extract_board(driver, cells)

            move = s.GetNextMove(b)
            print "Making move: " + str(move)
            self.make_move(driver, [move[0]+1, move[1]+1])

    def load_board(self, driver, soup):
        cells = []

        rows = 0
        cols = 0
        row = 1
        column = 1
        while True:
            name = str(row)+"_"+str(column)
            cell_soup = soup.find("div", {"id":name})
            if cell_soup == None:
                if column == 1:
                    rows = row-1
                    break
                cols = max(column-1, cols)
                column = 1
                row += 1
            else:
                if 'style' not in cell_soup.attrs:
                    cells.append(cell_soup)
                column += 1

        clickBoard = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(cells[i*rows+j])
            clickBoard.append(row)
        return (clickBoard, rows, cols)

    def extract_board(self, clickBoard, rows, cols):
        for i in range(rows):
            for j in range(cols):
                cell_soup = clickBoard[i][j]

        cell_type = cell_soup['class'][-1]
        b = board.Board(cols, rows)
        for cell in cells:
            col = cell[0]
            row = cell[1]
            t = cell[2]
            if "open" in t:
                b.SetCell(col, row, int(t[4:]))

        return b


    def make_move(self, driver, move):
        clickID = str(move[1])+"_"+str(move[0])
        print "Clicking on " + clickID
        driver.find_element_by_id(clickID).click()
TAS()