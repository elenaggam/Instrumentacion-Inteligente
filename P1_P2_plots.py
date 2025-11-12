import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P


# Medidas caja (grueso)
freq, vi, vo, phase = np.loadtxt('try_flog1000-40000-500000_steps70_avg8_Vin1.txt', unpack=True)
magn = vo/vi

P.bode_magnitude(freq, magn, directory='try2')

input("Enter para continuar.")
plt.close('all')

