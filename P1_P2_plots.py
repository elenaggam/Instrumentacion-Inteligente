import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P


# Medidas caja (grueso)
freq, vi, vo, phase = np.loadtxt('try_flog100-10000-500000_steps80_avg8_Vin1.txt', unpack=True)
magn = vo/vi

P.bode_diagrams(freq, magn, phase, directory='final_try', show=True)

input("Enter para continuar.")
plt.close('all')

