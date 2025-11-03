import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P

freq, vi, magn, phase = np.loadtxt('Bode/flog10-10000000.0-10000000.0_steps30_avg8_Vin1.txt', unpack=True)

P.bode_plots(freq, magn, phase, directory='Bode/30st', show=True)