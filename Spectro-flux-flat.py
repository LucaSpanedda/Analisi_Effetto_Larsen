# CALCOLO SPECTRAL FLUX / FLATNESS


# librerie
import pyACA
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# leggiamo un file audio mono importandolo da terminale
audiofile = input("Enter your file name (without extension):")

# leggiamo un file audio(file audio mono)
[fs, x] = pyACA.ToolReadAudio(audiofile+".wav")

# normalizziamo il file audio(a 0 dB)
x = x/np.max(abs(x)) 

# genero una base tempi coerente con il segnale analizzato, usando l'istruzione arange
time = np.arange(0,np.size(x))/fs

# spectral flux
[dsx, t] = pyACA.computeFeature("SpectralFlux",x,fs,iBlockLength=1024, iHopLength=512)

# spectral flatness
[dsf, t] = pyACA.computeFeature("SpectralFlatness",x,fs,iBlockLength=1024, iHopLength=512)


# plot

# nomina output
nomeplot = audiofile+"-Spectral-flux-flatness.png"

# numero di grafici verticali, numero di finestre orizzontali, numero progressivo

plt.subplot(3,1,1) 
plt.grid()
plt.specgram(x, NFFT=2048, Fs=fs, noverlap=1024, cmap='jet_r')
plt.xlabel("[Seconds]")
plt.ylabel("Frequency [Hz]")

plt.subplot(3,1,2) 
plt.grid()
plt.plot(t,dsx)
plt.xlabel("[Seconds]")
plt.ylabel("[Spectral Flux]")

plt.subplot(3,1,3) 
plt.grid()
plt.plot(t, np.log(dsf))
plt.xlabel("[Seconds] - "+audiofile)
plt.ylabel("[Spectral Flattness]")

# salva output
plt.savefig(nomeplot)