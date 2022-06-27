# CALCOLO STFT


# librerie
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# leggiamo un file audio mono importandolo da terminale
audiofile = input("Enter your file name (without extension):")

#leggiamo un file audio(mono)
[fs, x] = read(audiofile+".wav")
# print su terminale: samplerate, dimensione del file audio in campioni
print("SR: ",fs,"\ndimensione del file audio in campioni: ", np.size(x))

#normalizziamo il file audio(a 0 dB)
x = x/np.max(abs(x))

#calcoliamo la matrice STFT
f, t, STFT = signal.stft(x, fs, nperseg=4096, noverlap=512, window='blackmanharris')
# window, documentazione: https://docs.scipy.org/doc/scipy/reference/signal.windows.html

# nomina output
nomeplot = audiofile+"-STFT.png"


# plot
plt.figure(1)
plt.pcolormesh(t, f, np.abs(STFT), vmin=0, vmax=np.max(abs(STFT)), shading='auto')
plt.xlabel('[Seconds] - '+audiofile)
plt.ylabel('Frequency [Hz]')

# salva output
plt.savefig(nomeplot)