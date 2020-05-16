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

class Reviewtable(QDialog):
    def __init__(self):
        try:
            super(Reviewtable, self).__init__()
            self.setWindowTitle(" HERE'S REQUIRED DETAILS!!! ")
            self.setGeometry(50, 100, 1800, 700)
            df = pd.read_csv("reviews.csv")
            self.tableWidget = QTableWidget()
            self.tableWidget.setRowCount(len(df.index))
            self.tableWidget.setColumnCount(len(df.columns))
            self.tableWidget.move(0, 0)
            column_headers = ('s.no','name','review','rating','Age of review','No of reviews given till date')
            self.tableWidget.setHorizontalHeaderLabels(column_headers)
            for i in range(len(df.index)):
                for j in range(len(df.columns)):
                    self.tableWidget.setItem(i,j,QTableWidgetItem(str(df.iat[i, j])))
            self.tableWidget.move(0, 0)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.tableWidget)
            self.setLayout(self.layout)
            self.show()
        except BaseException as ex:
            print(ex)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = Reviewtable()
    sys.exit(app.exec_())