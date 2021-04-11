from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QPushButton
from PyQt5 import QtWidgets, QtCore,QtGui,uic,QtMultimedia
from mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
from scipy.io import wavfile
from random import randint
import pandas as pd
import pyqtgraph as pg
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
    #Colors of every channels
        self.pen1 = pg.mkPen(color=(255, 0, 0))
        self.pen2 = pg.mkPen(color=(100, 100, 100))
     #Timers
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
    #pause&resume buttons
        #ch_1
        self.ui.pushButton_9.clicked.connect(self.resume_1)
        self.ui.pushButton_10.clicked.connect(self.pause_1)
    #Actions for zooming in:
        self.ui.pushButton_7.clicked.connect(lambda: self.zoomin1())
     #Actions for zooming out:
        self.ui.pushButton_8.clicked.connect(lambda: self.zoomout1())
     #Action for Scrolling:
        self.ui.pushButton_5.clicked.connect(lambda: self.scroll_right1())
        self.ui.pushButton_6.clicked.connect(lambda: self.scroll_left1())


    def load(self):
        options =  QtWidgets.QFileDialog.Options()
        fname = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
                        "(*.wav) ", options=options) 
        if(fname[0]!=''):
            self.read_data(fname)
             
        else:
            pass
        
    #Reading data from files
    def read_data(self,fname):
        path = fname[0]
        self.samplerate,self.data = wavfile.read(path)
        self.sample_length = self.data.shape[0] 
        self.time = np.arange(self.sample_length) / self.samplerate
        self.Channel1(self.data,self.time)
        self.spectro(self.data)
    #Plotting input signal 
    def Channel1 (self,data,time):
        self.data_line1 =self.ui.Channel1_2.plot(time,data,pen=self.pen1)
        self.ui.Channel1_2.plotItem.setLimits(xMin =0, xMax=12)
        self.idx1=0
        self.ui.Channel1_2.plotItem.getViewBox().setAutoPan(x=True,y=True)
        self.timer1.setInterval(10)
        self.timer1.timeout.connect(lambda:self.update_plot_data1(self.data_line1,time,data))
        self.timer1.start()
        self.ui.Channel1_2.show()
        #self.ui.Channel1_2.setXRange(0))

  #Updating plots and repeating signals 
    def update_plot_data1(self,data_line,time,data):
        x = time[:self.idx1]
        y = data[:self.idx1]  
        self.idx1 +=10
        if self.idx1 > len(self.time) :
            self.idx1 = 0 
        if  self.time[self.idx1] >0.5:
            self.ui.Channel1_2.setLimits(xMin =min(x , default=0), xMax=max(x, default=0))
        self.ui.Channel1_2.plotItem.setXRange(max(x,default=0)-0.5 , max(x,default=0))
        self.data_line1.setData(x, y)
    #Input spectro 
    def spectro(self,data):
        sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None)
        plot.xlabel('Time')
        plot.ylabel('Frequency')
        plot.show()
       

 #resume&pause
    def resume_1(self):
        self.timer1.start()
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(True)
    def pause_1(self):
        self.timer1.stop()
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_9.setEnabled(True)
    #Zooming in and out 
    def zoomin1 (self):
        self.ui.Channel1_2.plotItem.getViewBox().scaleBy(y=0.9 ,x=0.9)
    def zoomout1 (self):
       self.ui.Channel1_2.plotItem.getViewBox().scaleBy(y=1/0.9 ,x=1/0.9)
    #Scrolling Left,right
    def scroll_right1(self):
        self.ui.Channel1_2.plotItem.getViewBox().translateBy(x=-0.1,y=0)
    def scroll_left1(self):
        self.ui.Channel1_2.plotItem.getViewBox().translateBy(x=0.1,y=0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()
