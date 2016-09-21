import time
import random
import board
import solver
import cProfile
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from ch_tas import TAS

from datetime import datetime

from lxml import etree
from io import StringIO, BytesIO


t = TAS()
html = t.driver.page_source

print (datetime.now())
soup = BeautifulSoup(html, "html.parser")
print (datetime.now())

parser = etree.HTMLParser()

print (datetime.now())
tree   = etree.parse(StringIO(html), parser)
print (datetime.now())

def testparse(html,parser):
	print (datetime.now())
	soup = BeautifulSoup(html, "html.parser")
	print (datetime.now())

	parser = etree.HTMLParser()

	print (datetime.now())
	tree   = etree.parse(StringIO(html), parser)
	print (datetime.now())

def testparse2(t, html,parser):
	print (datetime.now())
	soup = BeautifulSoup(html, "html.parser")
	cells = soup.findAll("div", {"class": u'square'})
	print (datetime.now())

	print (datetime.now())
	tree   = etree.parse(StringIO(html), parser)
	lxmlcells = tree.xpath('.//div[contains(@class, "square")]')
	print (datetime.now())

	print (datetime.now())
	drivercells = t.driver.find_elements_by_xpath('.//div[contains(@class, "square")]')
	print (datetime.now())

	return (cells, lxmlcells, drivercells)


