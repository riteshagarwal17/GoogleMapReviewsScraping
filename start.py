from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import time
import pandas as pd
import numpy as np
import os
import table
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait


class Demo1(QWidget):
    def __init__(self):
        super(Demo1, self).__init__()
        self.setWindowTitle(" Google map reviews ")
        # self.setWindowIcon(QIcon("ipl2.png"))
        self.setGeometry(100, 100, 1030, 750)
        grid = QGridLayout()
        newfont = QFont("cambria", 18, QFont.Bold)
        label1 = QLabel("Welcome you can see reviews of ambience mall gurugram here")
        btn1 = QPushButton("Click here to start")
        btn2 = QPushButton("Click here to see reviews")
        btn3 = QPushButton("Click here to load more reviews")
        btn4 = QPushButton("Click here to close app")
        label1.setFont(newfont)
        btn1.setFont(newfont)
        btn2.setFont(newfont)
        btn3.setFont(newfont)
        btn4.setFont(newfont)
        grid.addWidget(btn1, 4, 1, 2, 1)
        grid.addWidget(btn2, 7, 1, 2, 1)
        grid.addWidget(btn3, 10, 1, 2, 1)
        grid.addWidget(btn4, 13, 1, 2, 1)
        grid.addWidget(label1, 1, 1, 1, 1)

        btn1.clicked.connect(self.scrape)
        btn2.clicked.connect(self.see_again)
        btn3.clicked.connect(self.load_more)
        btn4.clicked.connect(self.close)
        # image = QImage(os.path.abspath("ipl15.jpg"))
        # sImage = image.scaled(QSize(1900, 1000))
        # palette = QPalette()
        # palette.setBrush(10, QBrush(sImage))
        # self.setPalette(palette)

        self.setLayout(grid)
        self.show()

    def scrape(self):
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\Lenovo\\Downloads\\chromedriver.exe")
        url = "https://www.google.com/maps/place/Ambience+Mall,+Gurugram/@28.5036504,77.0951417,17z/data=!3m1!4b1!4m7!3m6!1s0x390d1938456789c7:0x45a757aa37e73026!8m2!3d28.5036504!4d77.0973304!9m1!1b1"
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)

    def see_again(self):
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        rlist = response.find_all('div', class_='section-review-content')
        total = []
        for r in rlist:
            username = r.find('div', class_='section-review-title').find('span').text
            review_text = r.find('span', class_='section-review-text').text
            rating = r.find('span', class_='section-review-stars')['aria-label']
            rel_date = r.find('span', class_='section-review-publish-date').text
            no_of_ratings_given = r.find('div', class_='section-review-subtitle').find_all('span')[1].text.strip('・')
            comb = (username, review_text, rating, rel_date, no_of_ratings_given)
            total.append(comb)
        self.df = pd.DataFrame(total,
                               columns=['name', 'review', 'rating', 'Age of review', 'No of reviews given till date'])
        self.df.to_csv('reviews.csv')
        time.sleep(10)
        print(self.df.tail())
        self.obj = table.Reviewtable()
        self.obj.show()

    def load_more(self):
        scrollable_div = self.driver.find_element_by_css_selector(
            'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        print(self.df.shape)

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Demo1()
    sys.exit(app.exec_())

