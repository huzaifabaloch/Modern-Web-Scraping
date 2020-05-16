from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
from selenium import webdriver
import urllib.request
import requests
import sys
import json
from datetime import datetime
import os
import random
from bs4 import BeautifulSoup
from segment_hook import segment_hook

print('starting')

song_test = segment_hook("https://www.hooktheory.com/theorytab/view/Oh-Wonder/Lose-It", ["aaaaa", "fd", "ccc"])

print(song_test,'SONG TEST')


