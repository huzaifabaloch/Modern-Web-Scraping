from selenium import webdriver
from shutil import which
from lxml import html

import json
import time


main_feed = []

geckodr = which('geckodriver')

driver = webdriver.Firefox(executable_path=geckodr)
driver.implicitly_wait(60)
driver.get('https://www.hooktheory.com/theorytab/view/Oh-Wonder/Lose-It')

time.sleep(20)
y = 500
counter_scroll = 1
# the script scroll down 7 times to load the page. There are lazy loading. Otherwise no data.
while counter_scroll < 7:
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 500
    time.sleep(10)
    counter_scroll += 1


page_resp = html.fromstring(driver.page_source) 

tabs = page_resp.xpath("//*[contains(@class,'tab-container')]")

for tab in tabs:

    #chord_roman_block = tab.xpath("//*[@data-type='line']//*[@data-type='segment']//*[@data-type='chord-staff']//*[contains(@transform, 'translate') and not(contains(@class, 'gotham'))]")

    # For some, segemnts are broken into 2, so getting them and iterating for width, fill, roman/western chords value.
    chord_staff = tab.xpath(".//*[@data-type='line']//*[@data-type='segment']//*[@data-type='chord-staff']")
    #  ----- CHORD STAFF --------
    for staff in chord_staff:

        # ---- WESTERN STAFF --------
        western_chords_block = staff.xpath(".//*[contains(@dominant-baseline, 'middle')]")
        for western in western_chords_block:
            for text in western.xpath(".//*[contains(@alignment-baseline, 'middle') or contains(@class, 'gotham') or contains(@dy, 'ex')]"):
                if text.xpath(".//text()"):
                    if text.xpath(".//text()")[0] != ' ':
                        print(text.xpath(".//text()"))


        

        roman_chords_block = staff.xpath(".//*[contains(@transform, 'translate') and not(contains(@class, 'gotham'))]")
        length = len(roman_chords_block)


        

        print(f'For {length}')

        # ----- Getting WIDTH and FILL value from each chord staff segment ------
        for ind, lng in enumerate(staff.xpath(".//*[name()='g' and not(contains(@transform, 'translate'))]")):
            if ind < length:
                width = lng.xpath("(.//*[name()='rect'])[1]/@width")
                fill = lng.xpath("(.//*[name()='rect'])[1]/@fill")

                print(width, fill) 

        print('\n')

