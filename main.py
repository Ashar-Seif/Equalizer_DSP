from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QPushButton
from PyQt5 import QtWidgets, QtCore,QtGui,uic,QtMultimedia
from mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
from scipy.fftpack import fft,rfft
from scipy.io import wavfile
from random import randint
import pandas as pd
import pyqtgraph as pg
import numpy as np 
import sys  # We need sys so that we can pass argv to QApplication
import os
import cmath 
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
        self.ui.spinBox.setSingleStep(10)
        self.ui.spinBox.setValue(10)
        self.ui.spinBox.setMinimum(10)
        self.ui.spinBox.setMaximum(90)
    #Set_speed 
        self.ui.spinBox.valueChanged.connect(lambda: self.set_speed())
    #Show / Hide
        self.ui.checkBox.clicked.connect(self.ui.scrollArea_4.hide)
        self.ui.checkBox_2.clicked.connect(self.ui.scrollArea_5.hide)
    #pallettes
        self.ui.comboBox.activated.connect(self.default_palette)



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
        self.default_palette(self.data)
        self.FFT(self.data,self.samplerate,self.sample_length)
    #spectos
    def default_palette(self, data):
        if(self.ui.comboBox.currentText()=="Pallette 1"):
             sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="viridis")
             plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
             self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
             os.remove("Input1.png")
             print("1")
             
        elif(self.ui.comboBox.currentText()=="Pallette 2"):
             self.palette_2(self.data)
        elif(self.ui.comboBox.currentText()=="Pallette 3"):
            self.palette_3(self.data)
        elif(self.ui.comboBox.currentText()=="Pallette 4"):
            self.palette_4(self.data)
        else:
            self.palette_5(self.data)


    def palette_2(self,data):
             self.ui.scrollArea_4.clear
             sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="inferno")
             plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
             self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
             os.remove("Input1.png")
             print("2")
    def palette_3(self,data):
             self.ui.scrollArea_4.clear
             sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="magma")
             plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
             self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
             os.remove("Input1.png")
             print("3")
    def palette_4(self,data):
             self.ui.scrollArea_4.clear
             sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="plasma")
             plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
             self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
             os.remove("Input1.png")
             print("4")
    def palette_5(self,data):
             self.ui.scrollArea_4.clear
             sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="Greys")
             plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
             self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
             os.remove("Input1.png")
             print("5")

            

        
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
        #self.ui.Channel1_2.setXRange(0)

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

    def FFT(self,data,samplerate,sample_length):
        self.FFT = np.fft.fft(data)
        # Normalize
        self.FFTdata = abs(self.FFT)
        self.freqs = np.fft.fftfreq(self.sample_length,1/samplerate)
        print(self.freqs)
        #self.Bands(self.FFTdata.size)
        #self.IFFT(self.FFTdata,samplerate)
   
    def IFFT (self,data,samplerate):
        self.IFFT=(np.fft.ifft(self.FFT))
        self.magnitude= self.IFFT.real
        self.sample_length = self.IFFT.shape[0] 
        self.phase=[]
        self.time = np.arange(self.sample_length) / self.samplerate
        self.Channel2(self.magnitude,self.time)
        self.spectro1(self.data)
        for i in (self.IFFT):
           self.fphase=cmath.phase(i)
           self.phase.append(self.fphase)
           
    #def Bands(self,size): 
       # bandsno = math.ceil(0.05 * size)
     #  self.bands =[self.FFT[i * bandsno:(i + 1) * bandsno] for i in range(0,20)]  
     #Plotting input signal 
    def Channel2 (self,data,time):
       self.data_line2 =self.ui.Channel1_3.plot(time,data,pen=self.pen2)
       self.ui.Channel1_3.plotItem.setLimits(xMin =0, xMax=12)
       self.idx2=0
       self.ui.Channel1_3.plotItem.getViewBox().setAutoPan(x=True,y=True)
       self.timer2.setInterval(10)
       self.timer2.timeout.connect(lambda:self.update_plot_data2(self.data_line2,time,data))
       self.timer2.start()
       self.ui.Channel1_3.show()
      # self.ui.Channel1_2.setXRange(0)

  #dating plots and repeating signals 
    def update_plot_data2(self,data_line,time,data):
       x = time[:self.idx2]
       y = data[:self.idx2]  
       self.idx2 +=10
       if self.idx2 > len(self.time) :
           self.idx2 = 0 
       if  self.time[self.idx2] >0.5:
           self.ui.Channel1_3.setLimits(xMin =min(x , default=0), xMax=max(x, default=0))
       self.ui.Channel1_3.plotItem.setXRange(max(x,default=0)-0.5 , max(x,default=0))
       self.data_line2.setData(x, y)

#Input spectro 
    def spectro(self,data):
     sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None)
     plot.savefig('Input.png', dpi=300, bbox_inches='tight')
     self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input.png'))
     os.remove("Input.png")
 #Ouput spectro 
  #  def spectro1(self,data):
       #sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None)
       #plot.savefig('Output.png', dpi=300, bbox_inches='tight')
       #self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Output.png'))
       #os.remove("Output.png")

 #rume&pause
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
    def set_speed(self):
        # self.label_3.setText("current value:"+str(self.spinBox.value()))
        self.timer1.setInterval(self.ui.spinBox.value())
        self.timer1.timeout.connect(self.update_plot_data1(self.data_line1,time,data))
        self.timer1.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()
