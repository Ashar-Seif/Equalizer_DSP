from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QPushButton
from PyQt5 import QtWidgets, QtCore,QtGui,uic,QtMultimedia
from mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
from scipy.io import wavfile
from random import randint
import pandas as pd
import numpy as np 
import sys  # We need sys so that we can pass argv to QApplication
import os
QMediaPlayer=QtMultimedia.QMediaPlayer
QMediaContent=QtMultimedia.QMediaContent
QAction=QtWidgets.QAction


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.player = QMediaPlayer(self)
    #Actions of open menulist
        self.ui.actionChannel1.triggered.connect(self.load)
        self.ui.Channel1_2.setBackground('w')
        self.ui.Channel1_3.setBackground('w')

    def load(self):
        path,extention = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
            "(*.wav )")
        sound = QMediaContent(QtCore.QUrl.fromLocalFile(path))
        if path != '':
            self.player.setMedia(sound) 
        if(path!=''):
            self.read(path) 
        else:
            pass 
    def read(self,path):
        self.samplerate, self.dataa = wavfile.read(path)  
        self.sample_length = self.dataa.shape[0] 
        self.time = np.arange(self.sample_length) / self.samplerate
        self.plot_Time(self.time,self.dataa,self.graphsTime[0])
        self.FFS(self.dataa,self.samplerate) 









def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()