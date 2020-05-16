from selenium import webdriver
from shutil import which
from lxml import html

import json
import time


main_feed = []

geckodr = which('geckodriver')

driver = webdriver.Firefox(executable_path=geckodr)
#driver.implicitly_wait(60)
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




# =========================================================
def get_western_chords(western_chords_block, ind, western_ch_main):

    print(f"{len(western_chords_block)} lents found from {ind+1} staff - Western")
    
    for western in western_chords_block:
        text_concat = ''
        for text in western.xpath(".//*[contains(@alignment-baseline, 'middle') or contains(@class, 'gotham') or contains(@dy, 'ex')]"):
            if text.xpath(".//text()"):
                if text.xpath(".//text()")[0] != ' ':
                    text_concat += text.xpath(".//text()")[0]
        
        western_ch_main.append(text_concat)
    
    return western_ch_main

# =================================================================
def get_roman_chords(roman_chords_block, ind, roman_ch_main):
    
    print(f"{len(roman_chords_block)} lents found from {ind+1} staff - Roman")
    
    for roman in roman_chords_block:
        roman_chords = []
        roman_chords_tmp = []

        for text in roman.xpath(".//*[contains(@font-size, '28') or contains(@font-size, '12') or contains(@font-size, '11')]"):
            if text.xpath(".//*[contains(@class,'times') or contains(@class, 'gotham')]"):
                tspan_texts = text.xpath(".//*[contains(@class,'times') or contains(@class, 'gotham')]/text()")
                if len(tspan_texts) > 1:
                    for tspan_txt in tspan_texts:
                        if tspan_txt != ' ':
                            roman_chords.append(tspan_txt)
                else:
                    roman_chords.append(tspan_texts[0])
            else:
                if text.xpath(".//text()"):
                    if text.xpath(".//text()") != ' ':
                        roman_chords_tmp.append(text.xpath(".//text()")[0])     
     
        # appending letters from temporary array to array specifically for this condition - [V, 4, 2, /, V]
        # where / and V are coming before 4, 2
        for t in roman_chords_tmp:
            roman_chords.append(t)
        
        roman_ch_main.append(roman_chords)
        
    return roman_ch_main
        

    

def get_extras():
    pass


hook_theory = []

page_resp = html.fromstring(driver.page_source) 

tabs = page_resp.xpath("//*[contains(@class,'tab-container')]")

for ind, tab in enumerate(tabs):

    print(f'\nFor Tab no - {ind+1}')
    print('============================\n')

    widths = []
    fills = []
    roman_ch_main = []
    roman_ch_main1 = []
    western_ch_main = []
    western_ch_main1 = []


    # For some, segemnts are broken into 2, so getting them and iterating for width, fill, roman/western chords value.
    chord_staff = tab.xpath(".//*[@data-type='line']//*[@data-type='segment']//*[@data-type='chord-staff']")
    #  ----- CHORD STAFF --------
    for ind, staff in enumerate(chord_staff):

        # ---- WESTERN CHORD STAFF --------
        western_chords_block = staff.xpath(".//*[contains(@dominant-baseline, 'middle')]")
        
        western_chrds = get_western_chords(western_chords_block, ind, western_ch_main)


        print('\n')

        roman_chords_block = staff.xpath(".//*[contains(@transform, 'translate') and not(contains(@class, 'gotham'))]")
        length = len(roman_chords_block)

        roman_chrds = get_roman_chords(roman_chords_block, ind, roman_ch_main)


        print('\n')

        print(f'For {length}')

        # ----- Getting WIDTH and FILL value from each chord staff segment ------
        for ind, lng in enumerate(staff.xpath(".//*[name()='g' and not(contains(@transform, 'translate'))]")):
            if ind < length:
                width = lng.xpath("(.//*[name()='rect'])[1]/@width")[0]
                fill = lng.xpath("(.//*[name()='rect'])[1]/@fill")[0]

                widths.append(width)
                fills.append(fill)


    ###########################################################################
            #  DATA FORMATTING
    ##########################################################################
    hook = []
    for w, f, roman, western in zip(widths, fills, roman_chrds, western_chrds):
        data = {}
        data['width'] = w
        data['fill'] = f
        data['chord_western'] = western
        data['chord_roman'] = roman

        hook.append(data)
    
    hook_theory.append(hook)


with open('hook.json', 'w') as f:
    f.write(json.dumps(hook_theory))

    # print(f'{len(western_chrds)} - Western')
    # print(f'{len(roman_chrds)} - Roman')
    # print(f'{len(widths)} - Width')
    # print(f'{len(fills)} - Fill')




