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
from bs4 import BeautifulSoup
from selenium import webdriver

class TAS:
    def __init__(self):
        #select the headless web browser (whatever is installed)
        self.driver = webdriver.Firefox()

        self.driver.get('http://minesweeperonline.com/#')

    def Run(self, profile = False):
        if profile:
            cProfile.runctx("self.Solve(self.driver)", globals(),locals())#
        else:
            self.Solve(self.driver)

    def Solve(self, driver):
        self.solver = solver.Solver()
        (self.height, self.width) = self.GetBoardSize()

        while True:
            (b, win, lose) = self.ReadBoard()

            if win:
                print "--- WE WON! ---"
                break
            
            if lose:
                print "--- WE LOST :( ---"
                self.driver.find_element_by_id("face").click()
            (move, bombs, covered) = self.solver.GetNextMove(b)
            self.make_move(move)
            covered -= 1
            if covered == bombs:
                print "DONE!"
                break

            # raw_input()

    def GetBoardSize(self):
        cells = []

        rows = 0
        cols = 0
        row = 1
        column = 1

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        while True:
            name = str(row)+"_"+str(column)
            cell_soup = soup.find("div", {"id":name})
            if cell_soup == None or ('style' in cell_soup.attrs and 'display: none;' not in cell_soup.attrs['style']):
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

        rows -= 1
        cols -= 1

        mines_hundreds = int(soup.find("div", {"id":"mines_hundreds"}).attrs['class'][0][4:])
        mines_tens = int(soup.find("div", {"id":"mines_tens"}).attrs['class'][0][4:])
        mines_ones = int(soup.find("div", {"id":"mines_ones"}).attrs['class'][0][4:])
        num_bombs = mines_hundreds*100 + mines_tens*10 + mines_ones
        return (rows, cols, num_bombs)

    def ReadBoard(self):
        b = board.Board(self.width, self.height)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        cells = soup.findAll("div", {"class": u'square'})
        for cell in cells:
            (row, col) = cell.attrs['id'].split("_")
            if int(row) <= self.height and int(col) <= self.width:
                t = cell.attrs['class'][1]
                if "open" in t:
                    b.SetCell(int(col)-1, int(row)-1, int(t[4:]))

        faceClass = soup.find("div", {"id": u'face'}).attrs['class']

        didWin = "facewin" in faceClass
        didLose = "facedead" in faceClass

        return (b, didWin, didLose)

    def make_move(self, move):
        clickID = str(move[1]+1)+"_"+str(move[0]+1)
        self.driver.find_element_by_id(clickID).click()

t = TAS()
t.Run()