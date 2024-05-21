import json
from abc import ABC

import pandas as pd
import googlemaps
from bokeh.io import webdriver
from icecream import ic
import selenium

from python_algorithms.example.crime_abstract import PrinterBase, ReaderBase, ScraperBase, EditorBase


class Editor(EditorBase):

    def dropna(self, this: pd.DataFrame) -> pd.DataFrame:
        this = this.dropna()
        return this


class Printer(PrinterBase):

    def print(self):
        pass

    def dframe(self, this: pd.DataFrame) -> None:
        print('-' * 100)
        ic(f'타입: {type(this)}')
        ic(f'컬럼: {this.columns}')
        ic(f'상위 1개행: {this.head(1)}')
        ic(f'null 갯수: {this.isnull().sum()} 개')
        print('-' * 100)


class Reader(ReaderBase):

    def __init__(self) -> None:
        self.printer = Printer()

    def csv(self, file) -> object:
        return pd.read_csv(f'{file}.csv', encoding='UTF-8', thousands=',')

    def excel(self, file, header, usecols) -> object:
        return pd.read_excel(f'{file}.xls', header=header, usecols=usecols)

    def json(self, file) -> object:
        return json.load(open(f'{file}.json', encoding='UTF-8'))

    def gmaps(self, api_key: str) -> pd.DataFrame:
        return googlemaps.Client(key=api_key)

    def dframe(self, this: pd.DataFrame) -> None:
        self.printer.dframe(this)  # Printer 클래스의 dframe 메서드 호출

    def print(self) -> None:
        self.printer.print()  # Printer 클래스의 print 메서드 호출


class Scraper(ScraperBase):

    def __init__(self) -> None:
        pass

    def driver(self) -> object:
        return webdriver.Chrome('C:/Program Files/Google/Chrome/chromedriver.exe')

    def auto_login(self, driver, url, selector, data) -> None:
        driver.get(url)
        driver.find_element_by_css_selector(selector).send_keys(data)
        driver.find_element_by_css_selector(selector).submit()
