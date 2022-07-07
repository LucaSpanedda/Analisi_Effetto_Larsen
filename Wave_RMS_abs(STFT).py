# CALCOLO RMS E RAPPRESENTAZIONE DELLA FORMA D'ONDA E ABS STFT


# librerie
import numpy as np
import sys
import pyACA
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy import signal


# leggiamo un file audio mono importandolo da terminale
audiofile = input("Enter your file name (without extension):")

# print informazioni su file di testo
#with open(audiofile+"-INFO.txt", 'w') as fwr:
    #fwr.writelines('readme')

# leggiamo il file audio e ne stampiamo la durata
[fs, x] = read(audiofile+".wav")
print("SR: ",fs,"\ndimensione del file audio in campioni: ", np.size(x))
#fwr.writelines("SR: ",fs,"\ndimensione del file audio in campioni: ", np.size(x))

# normalizziamo il file audio(a 0 dB)
# dividendo il file per il modulo del suo massimo
x = x/np.max(abs(x))

t = np.arange(0,np.size(x))/fs

#calcoliamo gli RMS
[RMS, t] = pyACA.computeFeature("TimeRms", x, fs, iBlockLength=1024, iHopLength=512)

#calcoliamo la matrice STFT
f, t2, STFT = signal.stft(x, fs, nperseg=4096, noverlap=512, window='blackmanharris')
# window, documentazione: https://docs.scipy.org/doc/scipy/reference/signal.windows.html


# plot
# numero di grafici verticali, numero di finestre orizzontali, numero progressivo
plt.subplot(3,1,1)
plt.grid()
plt.plot(x)
plt.ylabel('[Wave]')
plt.xlabel('')

plt.subplot(3,1,3)
plt.pcolormesh(t2, f, np.abs(STFT), vmin=0, vmax=np.max(abs(STFT)*0.1), shading='auto', cmap='Blues')
plt.xlabel('[Seconds] - '+audiofile)
plt.ylabel('ABS(frequency)[Hz]')

plt.subplot(3,1,2)
plt.grid()
plt.plot(t, RMS)
plt.ylabel('[RMS]')
plt.xlabel('')

# ---------------------------------------- FIGURE

# nomina output
nomeplot = audiofile+"-RMS-STFT-Wave.png"

# salva output
plt.savefig(nomeplot)
