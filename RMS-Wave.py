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
frameLength = 1000

# hopSize in campioni -> di quanto ci spostiamo in ogni finestra di analisi, 
# mentre l'overlap e' il complemento dell'hopSize
hopSize = 500

# zero padding alla fine del file (non necessario in questo caso)
x = np.pad(x, (0,frameLength), 'constant', constant_values=(0,0))
print("\ndimensione del file audio post zero padding: ", np.size(x))
#fwr.writelines("\ndimensione del file audio post zero padding: ", np.size(x))

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

# plot
plt.subplot(2,1,1)
plt.grid()
plt.plot(x)
plt.ylabel('')
plt.xlabel('')

plt.subplot(2,1,2)
plt.grid()
plt.plot(t, RMS)
plt.ylabel('[RMS]')
plt.xlabel('[Seconds] - '+audiofile)

# ---------------------------------------- FIGURE

# nomina output
nomeplot = audiofile+"-RMS-Wave.png"

# plottiamo il tutto
plt.subplot(4,1,1)
plt.xlabel('')
plt.ylabel('[Wave]')
plt.plot(x)


# salva output
plt.savefig(nomeplot)