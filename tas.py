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
        (self.height, self.width, unused_bombs) = self.GetBoardSize()

        while True:
            print 'reading board'
            print (datetime.now())
            (b, win, lose) = self.ReadBoard()
            print (datetime.now())

            if win:
                print "--- WE WON! ---"
                break
            
            if lose:
                print "--- WE LOST :( ---"
                self.driver.find_element_by_id("face").click()

            print 'solving for move'
            print (datetime.now())
            (move, bombs, covered) = self.solver.GetNextMove(b)
            print (datetime.now())

            print 'making move'
            print (datetime.now())
            self.make_move(move)
            print (datetime.now())

            covered -= 1
            if covered == bombs:
                print "DONE!"
                break


    def GetBoardSize(self):


        cells = []

        rows = 0
        cols = 0
        row = 1
        column = 1
        # print (datetime.now())
        html = self.driver.page_source
        # print (datetime.now())
        soup = BeautifulSoup(html, "html.parser")
        # print (datetime.now())
        # parser = etree.HTMLParser()
        # tree   = etree.parse(StringIO(html), parser)
        # print (datetime.now())

        # old soup
        # print str(rows)+"_"+str(cols)
        # print (datetime.now())
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
        # print (datetime.now())

        rows -= 1
        cols -= 1
        # print str(rows)+"_"+str(cols)

        # #lxml
        # print str(rows)+"_"+str(cols)
        # print (datetime.now())
        # while True:
        #     name = str(row)+"_"+str(column)
        #     cell_soup = tree.xpath('.//div[contains(@id, "'+name+'")]')
        #     if len(cell_soup) == 0:
        #         if column == 1:
        #             rows = row-1
        #             break
        #         cols = max(column-1, cols)
        #         column = 1
        #         row += 1
        #     else:
        #         column += 1
        # print (datetime.now())
        # print str(rows)+"_"+str(cols)
        
        # # print (datetime.now())
        mines_hundreds = int(soup.find("div", {"id":"mines_hundreds"}).attrs['class'][0][4:])
        mines_tens = int(soup.find("div", {"id":"mines_tens"}).attrs['class'][0][4:])
        mines_ones = int(soup.find("div", {"id":"mines_ones"}).attrs['class'][0][4:])
        num_bombs = mines_hundreds*100 + mines_tens*10 + mines_ones
        
        # print (datetime.now())
        # mines_hundreds = int(tree.xpath('.//div[contains(@id,"mines_hundreds")]')[0].get('class')[-1])
        # mines_tens = int(tree.xpath('.//div[contains(@id,"mines_tens")]')[0].get('class')[-1])
        # mines_ones = int(tree.xpath('.//div[contains(@id,"mines_ones")]')[0].get('class')[-1])
        # num_bombs = mines_hundreds*100 + mines_tens*10 + mines_ones
        # print (datetime.now())

        rows -= 1
        cols -= 1

        return (rows, cols, num_bombs)

    def ReadBoard(self):
        b = board.Board(self.width, self.height)

        #print (datetime.now())
        html = self.driver.page_source
        #print (datetime.now())
        soup = BeautifulSoup(html, "html.parser")
        #print (datetime.now())
        # parser = etree.HTMLParser()
        # tree   = etree.parse(StringIO(html), parser)
        # print (datetime.now())

        cells = soup.findAll("div", {"class": u'square'})
        for cell in cells:
            (row, col) = cell.attrs['id'].split("_")
            if int(row) <= self.height and int(col) <= self.width:
                t = cell.attrs['class'][1]
                if "open" in t:
                    b.SetCell(int(col)-1, int(row)-1, int(t[4:]))

        # print ('starting lxml')
        # print (datetime.now())
        # cells = tree.xpath('.//div[contains(@class, "square") and not(contains(@style,"display: none;"))]')
        # for cell in cells:
        #     (row, col) = cell.get('id').split("_")
        #     if int(row) <= self.height and int(col) <= self.width:
        #         t = cell.get('class')
        #         if "open" in t:
        #             b.SetCell(int(col)-1, int(row)-1, int(t[-1]))
        # print (datetime.now())
        # print ('end lxml')

        # print (datetime.now())
        faceClass = soup.find("div", {"id": u'face'}).attrs['class']
        # print (datetime.now())
        # faceClass = tree.xpath('.//div[contains(@id, "face")]')[0].get('class')
        # print (datetime.now())
        
        didWin = "facewin" in faceClass
        didLose = "facedead" in faceClass
        return (b, didWin, didLose)

    def make_move(self, move):
        clickID = str(move[1]+1)+"_"+str(move[0]+1)
        self.driver.find_element_by_id(clickID).click()

t = TAS()
t.Run()



