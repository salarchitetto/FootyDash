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


def grab_uk_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(uk_webpage)

    prem = create_link_path('premier_league')
    champ = create_link_path('championship')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)

    driver.close()

def grab_scot_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(scot_webpage)

    prem = create_link_path('scot_prem')
    champ = create_link_path('scot_d1')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_germany_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(germany_webpage)

    prem = create_link_path('bundesliga1')
    champ = create_link_path('bundesliga2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_italy_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(italy_webpage)

    prem = create_link_path('seriea')
    champ = create_link_path('serieb')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_spain_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(spain_webpage)

    prem = create_link_path('laliga1')
    champ = create_link_path('laliga2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_france_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(french_webpage)

    prem = create_link_path('french1')
    champ = create_link_path('french2')

    paths = prem.create_path() + champ.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_netherlands_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(netherlands_webpage)

    prem = create_link_path('netherlands')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_belgium_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(belgium_webpage)

    prem = create_link_path('belgium')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)
    driver.close()

def grab_portugal_data():
    driver = webdriver.Chrome(executable_path=chromeDriver)

    driver.get(portugal_webpage)

    prem = create_link_path('portugal')

    paths = prem.create_path()

    for links in paths:
        driver.find_element_by_css_selector(f"a[href='{links}']").click()
        time.sleep(1)

    driver.close()


if __name__ == '__main__':

    grab_uk_data()
    grab_scot_data()
    grab_germany_data()
    grab_italy_data()
    grab_spain_data()
    grab_france_data()
    grab_netherlands_data()
    grab_belgium_data()
    grab_portugal_data()

