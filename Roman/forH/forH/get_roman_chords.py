
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import math
import urllib.request
import requests
import time
import sys
import json
import os

from bs4 import BeautifulSoup
from requests_html import HTMLSession


#  ================= MY IMPORTS ================
from lxml import html
from shutil import which
# ==============================================

session = HTMLSession()
geckodr = which('geckodriver')
xpath_genre = '/html/body/div[4]/div[1]/div/div/div[1]/div[6]/div/multiselect/ul/li[1]'

options = Options()
options.headless = True
x_path_page = '/html/body/div[4]/div[1]/div/div'
measures = []
driver = webdriver.Firefox(executable_path=geckodr, options=options)
main_array = []

def get_array_segments(url):
  print('start function')
  # the script wait 60 seconds than the page load
  driver.implicitly_wait(60)  # seconds
  driver.get(url)
  tabs = []
  time.sleep(20)
  y = 500
  counter_scroll = 1
  # the script scroll down 7 times to load the page. There are lazy loading. Otherwise no data.
  while counter_scroll < 7:
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 500
    time.sleep(10)
    counter_scroll += 1



  # ======================= MY CHANGES =======================================
  # will hold the final chords


  page = driver.page_source
  page_resp = html.fromstring(page)

  #tabs = driver.find_elements_by_xpath("//*[contains(@class,'tab-container')] ")
  tabs = page_resp.xpath("//*[contains(@class,'tab-container')]")
  print(tabs, 'TAB HERE')
  print(len(tabs),'THE LEN GGGGG')

  with open('abba1.json', 'w') as f:
    f.write(json.dumps(main_array))

  print("DONE")

  # Below that represents one segment of the page - on this test URl - there are 3 segments  (one segment = verse, chorus, prechorus)
  for segment in tabs:
    test = get_roman_chords(segment)
    print(test,'TEST HERE')


  time.sleep(10)  # i changes the time to go to sleep after
  driver.quit()




def get_roman_chords(segment_tab):
  segment_arr = []
  
  chords_block = segment_tab.xpath(".//*[@data-type='line']//*[@data-type='segment']//*[@data-type='chord-staff']//*[contains(@transform, 'translate') and not(contains(@class, 'gotham'))]")
  print(len(chords_block), ' - lent here')
  for chord in chords_block:

    # getting all the <text> tags of chord 
    texts = chord.xpath(
        ".//*[contains(@font-size, '28') or contains(@font-size, '12') or contains(@font-size, '11')]")

    # this will contain each chord like [I], [V, 4, 2, / V] etc
    array = []

    # This one is temporary which will hold some letters and then append
    # to array provided above, used specifically for this condition - [V, 4, 2, /, V]
    # where / and V are coming before 4, 2
    t_array = []

    # This loop will get roman letters and numbers associated with each chord. 
    for text in texts:
      if text.xpath(".//*[contains(@class,'times') or contains(@class, 'gotham')]"):
        chord_texts = text.xpath(".//*[contains(@class,'times') or contains(@class, 'gotham')]/text()")
        if len(chord_texts) > 1:
          for ind in chord_texts: 
            array.append(ind)
        else:
          array.append(chord_texts[0])
      else:
        if text.xpath(".//text()"):
          t_array.append(text.xpath(".//text()")[0])
    
    # appending letters from temporary array to array specifically for this condition - [V, 4, 2, /, V]
    # where / and V are coming before 4, 2
    for t in t_array:
      array.append(t)
    print(array,'the array')
    segment_arr.append(array)
    print(segment_arr, 'segment_arr')
  return segment_arr
  
   #main_array.append(segment_arr)



  # ==========================================================================





#get_array_segments('https://www.hooktheory.com/theorytab/view/ABBA/Waterloo')











