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
from selenium.webdriver import ActionChains

from datetime import datetime

from lxml import etree
from io import StringIO, BytesIO

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
        self.parser = etree.HTMLParser()
        (self.height, self.width, self.num_bombs) = self.GetBoardSize()
        self.b = board.Board(self.width, self.height)
        self.bombLocs = []
        
        init = True

        while True:

            while init:
                #click corners
                self.cell_objs[2][2].click()
                self.cell_objs[27][2].click()
                self.cell_objs[2][13].click()
                self.cell_objs[27][13].click()

                #click middle diamond
                self.cell_objs[16][4].click()
                self.cell_objs[16][12].click()
                self.cell_objs[8][8].click()
                self.cell_objs[20][8].click()
                (win, lose) = self.ReadBoard()

                if lose:
                    print "--- WE LOST :( ---"
                    self.driver.find_element_by_id("face").click()
                    self.b = board.Board(self.width, self.height)
                else:
                    init = False


            (win, lose) = self.ReadBoard()

            if win:
                print "--- WE WON! ---"
                break
            
            if lose:
                print "--- WE LOST :( ---"
                self.driver.find_element_by_id("face").click()
                self.b = board.Board(self.width, self.height)
                init = True
                self.bombLocs = []

            (moves, bombs, covered, bombLocs) = self.solver.GetNextMove(self.b)

            for move in moves:
                self.make_move(move)

                covered -= 1
                if covered == self.num_bombs:
                    return 'Done!'

            if len(bombLocs) > len(self.bombLocs):
                for bomb in bombLocs:
                    self.mark_bomb(bomb)


    def GetBoardSize(self):
        rows = 0
        cols = 0
        row = 1
        column = 1

        html = self.driver.page_source
        tree   = etree.parse(StringIO(html), self.parser)

        #lxml+xpath
        while True:
            name = str(row)+"_"+str(column)
            cell_soup = tree.xpath('.//div[contains(@id, "'+name+'")]')
            if len(cell_soup) == 0:
                if column == 1:
                    rows = row-1
                    break
                cols = max(column-1, cols)
                column = 1
                row += 1
            else:
                column += 1

        mines_hundreds = int(tree.xpath('.//div[contains(@id,"mines_hundreds")]')[0].get('class')[-1])
        mines_tens = int(tree.xpath('.//div[contains(@id,"mines_tens")]')[0].get('class')[-1])
        mines_ones = int(tree.xpath('.//div[contains(@id,"mines_ones")]')[0].get('class')[-1])
        num_bombs = mines_hundreds*100 + mines_tens*10 + mines_ones

        rows -= 1
        cols -= 1

        self.cell_objs = [[self.driver.find_element_by_id(str(r+1)+"_"+str(c+1)) for r in range(rows)] for c in range(cols)] 

        return (rows, cols, num_bombs)

    def ReadBoard(self):
        html = self.driver.page_source
        tree   = etree.parse(StringIO(html), self.parser)

        #lxml+xpath
        cells = tree.xpath('.//div[contains(@class, "square") and not(contains(@style,"display: none;"))]')
        for cell in cells:
            (row, col) = cell.get('id').split("_")
            if int(row) <= self.height and int(col) <= self.width and self.b.GetCell(int(col)-1, int(row)-1) == -1:
                t = cell.get('class')
                if "open" in t:
                    self.b.SetCell(int(col)-1, int(row)-1, int(t[-1]))

        faceClass = tree.xpath('.//div[contains(@id, "face")]')[0].get('class')

        didWin = "facewin" in faceClass
        didLose = "facedead" in faceClass
        return (didWin, didLose)

    def make_move(self, move):
        self.cell_objs[move[0]][move[1]].click()

    def mark_bomb(self, bomb):
        if bomb not in self.bombLocs:
            self.bombLocs.append(bomb)
            ActionChains(self.driver).context_click(self.cell_objs[bomb[0]][bomb[1]]).perform()         

t = TAS()
t.Run()

