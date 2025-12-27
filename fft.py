import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('fft_d.txt', skiprows=1)
print("FFT [dBV] → min:", np.min(data[:,1]), "max:", np.max(data[:,1]))

plt.plot(data[:,0], data[:,1])
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (dB)')
plt.title('FFT de la señal')
plt.grid()

plt.show()