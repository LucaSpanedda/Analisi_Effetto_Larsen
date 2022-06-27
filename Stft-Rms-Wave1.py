# CALCOLO RMS E RAPPRESENTAZIONE DELLA FORMA D'ONDA


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

# leggiamo il file audio ed assegniamo le coordinate
[fs, x] = read(audiofile+".wav")
print("SR: ",fs,"\ndimensione del file audio in campioni: ", np.size(x))
#fwr.writelines("SR: ",fs,"\ndimensione del file audio in campioni: ", np.size(x))

# normalizziamo il file audio(a 0 dB)
# dividendo il file per l'assoluto del suo massimo
x = x/np.max(abs(x))


# ---------------------------------------- RMS
# funzioni per il calcolo dell'RMS 
def rms (m):
    #square each element of the matrix
    m = np.square(m)
    #mean(medie relative ad ogni frame)
    m = np.mean(m, axis=1) #media per riga
    #root(ne realizziamo la radice quadrata)
    m = np.sqrt(m)

    return m


# generiamo la matrice dei frame temporali (segmentazione del campione nel dominio del tempo)
# lunghezza della frame di analisi in campioni
frameLength = 512

# hopSize in campioni -> di quanto ci spostiamo in ogni finestra di analisi, 
# mentre l'overlap e' il complemento dell'hopSize
hopSize = 1024

# costruzione della matrice delle frame temporali
# (array, dimensione, hopSize)
xFrames = pyACA.ToolBlockAudio(x, frameLength, hopSize)
# numero di frame di analisi
nFrames = xFrames.shape[0]
print("\n dimensioni della matrice delle frame temporali: ", xFrames.shape)
#fwr.writelines("\n dimensioni della matrice delle frame temporali: ", xFrames.shape)

# costruzione della base tempi
# (esso e' un array con istanti di tempo corrispondenti alle varie frame di analisi)
# per avere i valori dell'asse x in unita' temporali
t = (np.arange(0, nFrames)*hopSize + (frameLength/2))/fs

# estrarre il calcolo RMS 
RMS = rms(xFrames) #scala lineare
RMS_log = 20*np.log(rms(xFrames)) #scala logaritmica

print("\ndimensioni del vettore RMS: ", RMS.shape)
#fwr.writelines("\ndimensioni del vettore RMS: ", RMS.shape)


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