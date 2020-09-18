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
from copy import deepcopy

seen = set()
driver = None

def strip_for_id(s):
    return s.split('/')[-2]

def processPage(driver, g, paperid, direction):
    titles = driver.find_elements_by_css_selector('a.title.au-target')
    for t in titles:
        newid = strip_for_id(t.get_property('href'))
        g.add_node(newid, label=t.text)
        if direction == 'reference':
            g.add_edge(paperid, newid)
        elif direction == 'citedby':            
            g.add_edge(newid, paperid)

def processMultiPage(driver, g, paperid, direction):
    pages = driver.find_elements_by_css_selector('div.au-target.page')
    if len(pages) == 0:
        processPage(driver, g, paperid, direction)
    else:
        noOfPages = min([int(pages[-1].text), pagesLimit])
        for pageNo in range(1, noOfPages+1):
            print ('page:',pageNo,'/',noOfPages)
            pages = driver.find_elements_by_css_selector('div.au-target.page')
            pages[[p.text for p in pages].index(str(pageNo))].click()
            time.sleep(T)
            processPage(driver, g, paperid, direction)
    

# ready to start up headless browser
driver = webdriver.Chrome()
g = networkx.DiGraph()


pagesLimit = 10
T = 10

def expand(paperid):
    if paperid in seen:
        return
    seen.add(paperid)
    
    print ('references:')
    url = 'https://academic.microsoft.com/paper/'+paperid+'/reference'
    driver.get(url)

    time.sleep(T)
    
    if( 'reference' in driver.current_url ):        
        processMultiPage(driver, g, paperid, direction='reference')
                
    print ('citations:')
    url = 'https://academic.microsoft.com/paper/'+paperid+'/citedby'
    driver.get(url)

    time.sleep(T)
    if( 'citedby' in driver.current_url ):            
        processMultiPage(driver, g, paperid, direction='citedby')
                
    networkx.write_gexf(g, 'outputGraph.gexf')

#%%
expand('2796885425')     
expand('2895739182')
for tek in range(10):
    for n in deepcopy(g.node):
        if not(n in seen):
            if g.degree[n] > 1:
                expand(n)
g.in_degree                
#tabs = driver.find_elements_by_css_selector('ma-call-to-action.au-target.route')
#REF = tabs[[t.text for t in tabs].index('REFERENCES')]
#CIT = tabs[[t.text for t in tabs].index('CITED BY')]
# create our graph that will get populated

#driver.close()
                
#%%
for n in deepcopy(g.node):
    if g.degree[n] == 1:
        g.remove_node(n)
networkx.write_gexf(g, 'output_clean.gexf')