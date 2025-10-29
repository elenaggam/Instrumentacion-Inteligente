import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P

freq, vi, magn, phase = np.loadtxt('Bode/flog2-6_steps56_avg8_Vin1.txt', unpack=True)

P.bode_plots(freq, magn, phase, directory='Bode/8', show=True)