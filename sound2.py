import numpy as np
import wavio
# imports
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import random
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
# Parameters
samplerate = 44100   # samples per second
#T = 3           # sample duration (seconds)
#f = 440.0       # sound frequency (Hz)
x3=np.array([])
#for f in range(400,700,30):
for i in range (15):
     f = random.randint(300,700)
     print(f)
     #Returns a random float number between 0 and 1
     duration = random.randint(1,3)
     samples = duration*samplerate
     t = np.linspace(0,duration, samples, endpoint=False)
     x = np.sin(2*np.pi * f * t) 
     x2 =np.concatenate((x3,x),axis=0)
     x3=x2
x3=np.delete(x3,0,0)
# Write the samples to a file
wavio.write("sine.wav", x3, samplerate, sampwidth=3)
