#!/usr/bin/env python

import re
import sys
import json
import time
import random
import argparse
import networkx
import requests_html


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse, parse_qs

seen = set()
driver = None

def strip_for_id(s):
    return s.split('/')[-2]

# ready to start up headless browser
driver = webdriver.Chrome()
g = networkx.DiGraph()


paperid = '2539828367'
pagesLimit = 10
hops = 2
searchList = [(paperid, hops)]
nodes = [paperid]
edges = []
i = 0
while i < len(searchList):
    paperid, hops = searchList[i]
    print (paperid, hops)
    i += 1
    if (hops == 0):
        continue
    if paperid in seen:
        continue
    seen.add(paperid)
    hops -= 1
    
    print ('references:')
    url = 'https://academic.microsoft.com/paper/'+paperid+'/reference'
    driver.get(url)

    time.sleep(8)
    
    pages = driver.find_elements_by_css_selector('div.au-target.page')
    if len(pages) == 0:
        titles = driver.find_elements_by_css_selector('a.title.au-target')
        for t in titles:
            newid = strip_for_id(t.get_property('href'))
            g.add_node(newid, label=t.text)
            g.add_edge(paperid, newid)
            searchList.append((newid, hops))

    else:                
        noOfPages = min([int(pages[-1].text), pagesLimit])
        for pageNo in range(1, noOfPages+1):
            print ('page:',pageNo,'/',noOfPages)
            pages = driver.find_elements_by_css_selector('div.au-target.page')
            pages[[p.text for p in pages].index(str(pageNo))].click()
            time.sleep(8)
            titles = driver.find_elements_by_css_selector('a.title.au-target')
            for t in titles:
                newid = strip_for_id(t.get_property('href'))
                g.add_node(newid, label=t.text)
                g.add_edge(paperid, newid)
                searchList.append((newid, hops))
                
    print ('citations:')
    url = 'https://academic.microsoft.com/paper/'+paperid+'/citedby'
    driver.get(url)

    time.sleep(8)
    
    pages = driver.find_elements_by_css_selector('div.au-target.page')
    if len(pages) == 0:
        titles = driver.find_elements_by_css_selector('a.title.au-target')
        for t in titles:
            newid = strip_for_id(t.get_property('href'))
            g.add_node(newid, label=t.text)
            g.add_edge(newid, paperid)
            searchList.append((newid, hops))
    else:                
        noOfPages = min([int(pages[-1].text), pagesLimit])
        for pageNo in range(1, noOfPages+1):
            print ('page:',pageNo,'/',noOfPages)
            pages = driver.find_elements_by_css_selector('div.au-target.page')
            pages[[p.text for p in pages].index(str(pageNo))].click()
            time.sleep(8)
            titles = driver.find_elements_by_css_selector('a.title.au-target')
            for t in titles:
                newid = strip_for_id(t.get_property('href'))
                g.add_node(newid, label=t.text)
                g.add_edge(newid, paperid)
                searchList.append((newid, hops))
                
    networkx.write_gexf(g, '%outputGraph.gexf')
        
#tabs = driver.find_elements_by_css_selector('ma-call-to-action.au-target.route')
#REF = tabs[[t.text for t in tabs].index('REFERENCES')]
#CIT = tabs[[t.text for t in tabs].index('CITED BY')]
# create our graph that will get populated

#driver.close()