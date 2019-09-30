import os
import time
from selenium import webdriver
from config import *

class create_link_path:
    league_dictionary = {'premier_league': 'E0',
                         'championship' : 'E1',
                         'scot_prem': 'SC0',
                         'scot_d1': 'SC1',
                         'bundesliga1': 'D1',
                         'bundesliga2': 'D2',
                         'seriea': 'I1',
                         'serieb': 'I2',
                         'laliga1': 'SP1',
                         'laliga2': 'SP2',
                         'french1': 'F1',
                         'french2': 'F2',
                         'netherlands': 'N1',
                         'belgium': 'B1',
                         'portugal': 'P1'}

    country_constant = {'constant': 'mmz4281'}

    def __init__(self, league,):
        self.league = league

    def create_path(self):
        yearEnd = range(19, -1, -1)
        yearStart = range(18, -1, -1)

        yearList = []
        for x, y in zip(yearStart, yearEnd):
            yearList.append(str(x) + str(y))

        newYears = []
        for x in yearList:
            if len(x) == 4:
                newYears.append(x)
            elif len(x) == 3:
                string = '0' + x
                newYears.append(string)
            elif len(x) == 2:
                string = '0' + x[0] + '0' + x[1]
                newYears.append(string)
            elif x == '01':
                newYears.append('0001')

        paths = []
        for x in newYears:
            paths.append(create_link_path.country_constant['constant'] + '/' + x + '/' + \
                         create_link_path.league_dictionary[self.league] + '.csv')

        return paths

def create_directory(file_path, list_O_links):
    for x in list_O_links:
        os.mkdir(file_path + '\\' + x.split('/')[3][:-5])


def grab_uk_data():

    print('Working on the England Data')

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\england'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(uk_webpage)

    prem = create_link_path('premier_league')
    champ = create_link_path('championship')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)

    driver.close()

def grab_scot_data():

    print('Working on the Scottish Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\scotland'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)


    driver.get(scot_webpage)

    prem = create_link_path('scot_prem')
    champ = create_link_path('scot_d1')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_germany_data():

    print('Working on the German Data')

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\germany'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)


    driver.get(germany_webpage)

    prem = create_link_path('bundesliga1')
    champ = create_link_path('bundesliga2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_italy_data():

    print('Working on the Italian Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\italy'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(italy_webpage)

    prem = create_link_path('seriea')
    champ = create_link_path('serieb')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_spain_data():

    print('Working on the Spanish Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\spain'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(spain_webpage)

    prem = create_link_path('laliga1')
    champ = create_link_path('laliga2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_france_data():

    print('Working on the French Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\france'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(french_webpage)

    prem = create_link_path('french1')
    champ = create_link_path('french2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_netherlands_data():

    print('Working on the Netherland Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\netherlands'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(netherlands_webpage)

    prem = create_link_path('netherlands')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_belgium_data():

    print('Working on the Belgium Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\belgium'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(belgium_webpage)

    prem = create_link_path('belgium')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_portugal_data():

    print('Working on the Pork And Cheese Data')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': r'C:\Users\Sal Architetto\Desktop\footy_data_sets\portugal'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chrome_options)

    driver.get(portugal_webpage)

    prem = create_link_path('portugal')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)

    driver.close()
