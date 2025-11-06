import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P

freq, vi, magn, phase = np.loadtxt('Bode_exp/flog1000-40000-1000000.0_steps70_avg8_Vin1.txt', unpack=True)

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)

print(f_low, max_magn)
P.bode_plots(freq, magn, phase, directory='Bode_exp/try2', show=True, f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)

