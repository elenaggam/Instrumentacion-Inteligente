import numpy as np
import matplotlib.pyplot as plt


dir = 'Wave_gen/Rf/k127_630Hz_fft/'

tr_f, tr_v = np.loadtxt(dir+'tr.txt', unpack=True, delimiter='\t')
sq_f, sq_v = np.loadtxt(dir+'sq.txt', unpack=True, delimiter='\t')
print(tr_f.shape)
V_sq = 8.3  # V
V_tr = 7.77
f = 0.630  # kHz
plt.scatter(sq_f, sq_v/V_sq)
n = [i for i in range(1, 19)]
plt.plot(n, 1/np.array(n), 'r-')
plt.show()

plt.scatter(tr_f, tr_v/V_tr)
plt.plot(n, 1/np.array(n)**2, 'r-')
plt.show()


