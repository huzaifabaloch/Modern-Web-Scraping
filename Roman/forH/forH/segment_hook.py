from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from get_roman_chords import get_roman_chords
import math
import urllib.request
import requests
import time
import sys

import json
import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from lxml import html
from shutil import which

#'/Users/romain/Desktop/Projects/Bravon Project/Code/beautifulSoupScript/hooktheory/geckodriver'

session = HTMLSession()
geckodriver = 'geckodriver'
xpath_genre = '/html/body/div[4]/div[1]/div/div/div[1]/div[6]/div/multiselect/ul/li[1]'

options = Options()
options.headless = True
x_path_page = '/html/body/div[4]/div[1]/div/div'
measures = []
driver = webdriver.Firefox(firefox_options=options,
                           executable_path=geckodriver)


def bin_function():
    number_of_segments(url)
    list_to_return = []
    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=geckodriver)
    driver.get(url)
    results_genre = driver.find_elements_by_xpath(xpath_genre)
    print(results_genre, 'result genre here')
    for result in results_genre:
        link = result.find_elements_by_tag_name('a')
        for x in link:
            list_to_return.append(x.text)
    print(list_to_return, 'list to rente')
    driver.quit()


def segment_hook(url, array_segments):
    create_object_number_segment(array_segments)
    result = get_array_segments(url, array_segments)
    print(measures, 'the measure here')
    return result




def get_array_segments(url, array_segments):
    # driver = webdriver.Firefox(firefox_options=options,
    #  executable_path = geckodriver)

    # test2 = driver.find_elements_by_xpath(
    # '//*[@class="padding-bottom-20 padding-right-5"]')
    # print(len(test2), 'TEST2')

    #try:
        main_array=[]
      # We wait until we get the call called .tab container to start scraping
        #firefox_options = options,executable_path = geckodriver
        driver = webdriver.Firefox(firefox_options=options,
                                   executable_path=geckodriver)
        driver.implicitly_wait(60)  # seconds
        driver.get(url)
        tabs = []
        time.sleep(20)
        print("executre SCRIPTPIITPITTIPTIT")
        y = 500
        counter_scroll = 1
        while counter_scroll < 7:
          driver.execute_script("window.scrollTo(0, "+str(y)+")")
          y += 500
          time.sleep(3)
          counter_scroll += 1
        #tabs = driver.find_elements_by_class_name("app-content-score")
        tabs = driver.find_elements_by_xpath("//*[contains(@class,'tab-container')] ")
        #element = WebDriverWait(driver, 10).until_not(
        #EC.presence_of_element_located((
         #   By.XPATH, "//*[contains(@class,'tab-container')] ")))
        #time.sleep(60)
        print(len(tabs), 'the len of new tabs')
        print(tabs, 'new TABS new222')
        print(array_segments, 'ARRAY segments')
        # We create a dictionnary in a List, dictionnary=[ {'name_segment': 'chorus','segment_hook_theory':'tab_segment',chords:[[measure1],[measure2]]}, {same}]
        dictionnary = []
        counter = 0
        genres = []
        genre_find= driver.find_elements_by_xpath(
                "//*[contains(@items ,'genres')]//*[contains(@class ,'ng-binding')]//*[contains(@class ,'ng-binding')]")
        print(genre_find, 'genre_findgenre_findgenre_find')
        print(len(genre_find),'the LEN HERE')
        for x in genre_find:
            print(x, 'XX')
            x = x.text
            print(x,'XX')
            genres.append(x)
            print(genres, 'new genre', x)
        
        main_array.append(genres)
        print('now genre no')

        for segment in array_segments:
            obj = {'name_segment': segment,
                   'chords': [],
                   'segment_hook_theory': tabs[counter]}
            dictionnary.append(obj)
            counter = counter+1
        print(dictionnary, 'new dictionnary')
        page = driver.page_source
        page_resp = html.fromstring(page)
        segment_tab = page_resp.xpath("//*[contains(@class,'tab-container')]")
        print(segment_tab, 'TAB HERE')
        print(len(segment_tab), 'THE LEN GGGGG')

        # Now, Loop in each segment_hook_theory
        print(len(dictionnary))
        counter2 = 0
        counter_tab = 0
        for segment in dictionnary:
            counter_test=0
            main_counter=0
            # create an array of chords for each segments roman
            chord_list=[]
            text_list = []
            
            #array_roman_test = get_roman_chords(segment)
            print('#########################################################')
            print('######################################################^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            #print(array_roman_test, '#########################################################array roman test here')
            print('#########################################################')
            #new solution find groups of 
            # 1.create an array of theses g group (by measure)
            # 2.create a string of this array
            # 3.append the string in chord_list
            #chords_block = get_roman_chords(segment['segment_hook_theory'])
           
            """  
            g_groups = segment['segment_hook_theory'].find_elements_by_xpath(
                ".//*[name()='g']//*[contains(@transform, 'scale(1)')]")
            print(g_groups, '*********************g_group3')
            print(len(g_groups), '*********************g_group LEN')
            for one_group in g_groups:
              objects_item = {"big_items":[], "small_items":[], "second_letter":None, "separator":"false"}
              
              objects_item ["big_items"]= one_group.find_elements_by_xpath(
                  ".//*[name()='text' and contains(@font-size ,'28')]")
              print(len(objects_item["big_items"]), '$$$$$$$$$$$$$$$$$$      LEN      $objects_item ["big_items"new]')
              print('###############################################')
              print('###############################################')
              print('###############################################')
       
              objects_item["small_items"] = one_group.find_elements_by_xpath(
                  ".//*[name()='text' and contains(@font-size ,'12')]")
              print(len(objects_item["small_items"]),
                    '#######################        LEN -----------------objects_item["small_items"]')
              print('###############################################')
              print('###############################################')
              print('###############################################')
              small_items_2 = one_group.find_elements_by_xpath(
                  ".//*[name()='tspan']")
              sentence=[]
              print(objects_item, '###########################objects_item')
              for x in objects_item["big_items"]:
                 print(x.text,'XXXXXXXXXXXX')
                 sentence.append(x.text)
              for y in objects_item["small_items"]:
                 print(y.text,"yyyyyyyyyy")
                 sentence.append(y.text)
              for z in small_items_2:
                print(z.text,'zzzzzzzzzzzzzzzzz')
              print('###############################################')
              print(sentence, '#####################################the magic lat sentece new')
              print('###############################################')
              print('############################################### COUNTER2',counter2)
              print('############################################### COUNTER_TEST:', counter_test,'main_counter:',main_counter)
              counter_test=counter_test+1

              """

            #roman_chords = get_roman_chords(segment_tab[counter_tab])
            #print(roman_chords,'the good CHORD ROMAN HERE$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            
            #text_list=segment['segment_hook_theory'].find_elements_by_xpath(
               # ".//*[@data-type='chord-staff']//*[name()='g']//*[1][name()='text']")
            text_list=segment['segment_hook_theory'].find_elements_by_xpath(
                ".//*[name()='g']//*[1][name()='text' and contains(@font-size ,'28')]")


            # .//*[name() = 'g']//*[name() = 'text' and contains(@font-size, '28') or contains(@font-size, '12')]
                # font size = 24 for the US letter
            print(len(text_list),'TEXT_LIST LEN new')
            tspan_list=[]
            for text in text_list:
              group_tspan_list=[]
              tspan_list=[]
              tspan_list=text.find_elements_by_xpath(".//*[name()='tspan']")
              for x in tspan_list:
                group_tspan_list.append(x.text)
              group_tspan_list=''.join(group_tspan_list)  
              chord_list.append(group_tspan_list)
            chord_list = get_roman_chords(segment_tab[counter_tab])
            print(chord_list, 'HOPE$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            counter_tab = counter_tab+1
            # create array chord western notation text

            chord_list_western=[]
            text_list_western=segment['segment_hook_theory'].find_elements_by_xpath(
                ".//*[name()='g']//*[1][name()='text' and contains(@font-size ,'24')]")
            tspan_list_western=[]
            for text_western in text_list_western:
              group_tspan_list_western=[]
              tspan_list_western=[]
              tspan_list_western=text_western.find_elements_by_xpath(".//*[name()='tspan']")
              for x_western in tspan_list_western:
                group_tspan_list_western.append(x_western.text)
              group_tspan_list_western=''.join(group_tspan_list_western)  
              chord_list_western.append(group_tspan_list_western)

            # loop in each segment of the pages
            counter2=counter2+1
            attempt = []
            print(segment['segment_hook_theory'],"SEGMENT HOOKTHEORY")
            attempt= segment['segment_hook_theory'].find_elements_by_xpath(
                ".//*[@data-type='chord-staff']//*[name()='g']//*[1][name()='rect']")
            values_list_fill=[]
            values_list_width=[]
            list_values_scrapped=[]
            list_measures = []
            key_top = None
            key_middle = None
            key_bottom = None
            tempo:None
            key_top = segment['segment_hook_theory'].find_element_by_xpath("//*[contains(@title ,'Change the master key and scale of the project')]//*[contains(@class ,'div-control-button-content')]//*[contains(@class ,'gotham')]")
            key_top = key_top.text
            try:
              key_middle = segment['segment_hook_theory'].find_element_by_xpath(
                  "//*[contains(@title ,'Change the master key and scale of the project')]//*[contains(@class ,'div-control-button-content')]//*[contains(@class ,'scale-degrees')]")
            except NoSuchElementException:
              print('NOOOOO####')
              key_middle = None
            if key_middle != None:
               key_middle = key_middle.text
            
            print(key_middle, 'key middle test &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            key_bottom = segment['segment_hook_theory'].find_element_by_xpath(
                "//*[contains(@title ,'Change the master key and scale of the project')]//*[contains(@class ,'div-control-button-content')]//*[contains(@class ,'secondary')]")
            key_bottom=key_bottom.text
            tempo = segment['segment_hook_theory'].find_element_by_xpath(
                "//*[contains(@title ,'Change the master tempo of the project')]//*[contains(@class ,'primary')]")
            print(tempo,'TEMPO HERE')
            tempo = tempo.text
            print(tempo,'TEMPO TEXT HERE')
            
            print(key_top, key_bottom, "key top key bottom##############################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            if key_middle == None:
              obj_measure = {"key": "{} {}".format(
                key_top, key_bottom), "tempo": tempo}
            else:
              obj_measure = {"key": "{} {} {}".format(
                    key_top,key_middle, key_bottom), "tempo": tempo}
            list_measures.append(obj_measure)
            print(obj_measure,'the obj measure2 test@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################################')
            beat_counter=0
            counter_measure=0
            for x in attempt:
              
              if x.get_attribute('width')=="1" or x.get_attribute('width')=="2": 
                print('')
                #print('its 1 here or 2',x.get_attribute('width') )
              else:
                values_list_fill.append(x.get_attribute('fill'))
                values_list_width.append(x.get_attribute('width'))
                four_beats=81.125
                beat= four_beats / float(x.get_attribute('width'))
                beat= 4/beat
                beat = round(beat, 2)
                # 1.1 floor or 0.9 ceil a number or make 0,4 == to 5 
                decimal=int(str(beat).split('.')[1][0])
                if decimal== 9 :
                  beat = math.ceil(beat)
                elif decimal==1 or decimal==0:
                  beat = math.floor(beat)
                elif decimal==4 or decimal==5:
                  beat= float(str(beat).split('.')[0]+'.'+'50')
                else:
                  print('nothing')
                dictionnary = {"width":x.get_attribute('width'), "fill":x.get_attribute('fill'), "beat":beat, "chord_roman":None,"chord_western":None}
                # if beat + beat + beat = 4 I push list_values_scrapped in list_measures
                beat_counter=beat_counter+beat
                
                print('@@@@@@@@@@@@@@@@@@@@@@')
                print("BEAT COUNTER:",beat_counter,"BEAT:",beat,"WIDTH:", x.get_attribute('width'),"FILL:",x.get_attribute('fill'))
                print('@@@@@@@@@@@@@@@@@@@@@@')
                def get_note(fill, type_note):
                  
                  chord=[]
                  if fill=="#aaa":
                    chord.append(None)
                    chord.append(None)
                  else:
                    #changed the main counter by 0
                    # each time it takes a color, it deletes the color it took
                    if (type_note == "roman"):
                      if len(chord_list)!= 0:
                        chord.append(chord_list.pop(0))
                      
                      print("ROMANNNNNNNNN")
                      print(chord_list,"###########$$$$$$$$$$$$$$  new chordl list ROMAN")
                    elif (type_note == "western"):
                      if len(chord_list_western) != 0:
                        chord.append(chord_list_western.pop(0))

                      print("WESTERNNNNNNN")
                      print(chord_list_western,"###########$$$$$$$$$$$$$$  new chordl list WESTERN")
                    #chord.append(chord_list[0])
                    #chord.append(chord_list_western[0])
                  return chord
                #global main_counter  fix bug with main counter and
                if beat_counter == 4:
                  print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$equal to 4')
                  dictionnary['chord_roman'] = get_note(
                      x.get_attribute('fill'), 'roman')[0]
                  dictionnary['chord_western'] = get_note(
                      x.get_attribute('fill'), 'western')[0]
                  print(main_counter,"MAIN_COUNTER")
                  main_counter=main_counter+1
                  list_values_scrapped.append(dictionnary)
                  list_measures.append(list_values_scrapped)
                  list_values_scrapped=[]
                  beat_counter=0
                  print('@@@@@@@@@@@@@@@@@@@@@@')
                  print("WIDTH end Tab ",x.get_attribute('width'),"counter:",counter2,'////////////////////////////////////////////////////////////////////',counter_measure)
                  print('@@@@@@@@@@@@@@@@@@@@@@')
                  counter_measure=counter_measure+1
                elif beat_counter > 4:
                  dictionnary['chord_roman'] = get_note(x.get_attribute('fill'),"roman")[0]
                  dictionnary['chord_western'] = get_note(x.get_attribute('fill'),"western")[0]

                  print(main_counter,"MAIN_COUNTER")
                  beat_counter=beat_counter-4
                  #dictionnary['beat']=dictionnary['beat']-beat_counter
                  dictionnary['beat'] = 4
                  dictionnary['test']=1
                  list_values_scrapped.append(dictionnary)
                  list_measures.append(list_values_scrapped)
                  list_values_scrapped=[]
                  dictionnary['beat']=beat_counter
                  list_values_scrapped.append(dictionnary)
                  main_counter = main_counter+1
                  if beat_counter == 4:
                    # get next index x ? of the node name how to get the next x basically and FILL associated to it THen pass it DOn is not working because whts the X
                    #dictionnary['chord_roman'] = get_note(
                       # x.get_attribute('fill'),"roman")[0]
                    #dictionnary['chord_western'] = get_note(
                      #x.get_attribute('fill'),"western")[0]
                    list_values_scrapped.append(dictionnary)
                      # remove before if bug TEST
                    list_measures.append(list_values_scrapped)
                    list_values_scrapped=[]
                    beat_counter = 0
                    main_counter = main_counter+1
                    # possible futur bug, if a segment if more than 8 beats, then have to find a dynamic solution
                else:
                  dictionnary['chord_roman'] = get_note(x.get_attribute('fill'),"roman")[0]
                  dictionnary['chord_western'] = get_note(x.get_attribute('fill'),"western")[0]
                  print(main_counter,"MAIN_COUNTER")
                  list_values_scrapped.append(dictionnary)
            main_array.append(list_measures)
            #print("values are :",values_list_fill,"counter is here :",counter2, "length List :", len(values_list_fill))
            #print("list width", values_list_width,len(values_list_width))
            #print("list_values_scrapped :", list_values_scrapped, "lnew en values scrapped:", len(list_values_scrapped), "counter2 :", counter2)
            print('###########################################################')
            print('###########################################################')
            print('###########################################################')
            print(counter2,"new list_measures printing2 :", list_measures,"counter2 :", counter2, "len list measure:", len(list_measures))
            print('###########################################################')
            print('###########################################################')
            print('###########################################################')
            print('###########################################################')
    #finally:
        print("end here")
        time.sleep(10) # i changes the time to go to sleep after 
        driver.quit()
        return main_array
    


def create_object_number_segment(array_segments):
    counter = 0
    for x in array_segments:
        object_x = {"segment_name": x}
        array = [object_x]
        measures.append(array)
        counter = counter+1
    return measures




