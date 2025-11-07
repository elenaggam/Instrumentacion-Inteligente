import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P



# Medidas caja
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000.0_steps70_avg8_Vin1.txt', unpack=True)

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)

delta = 20*np.log10(max_magn/min_magn)
print("\nGain:\t\tA_0 = {max_magn}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))
P.bode_plots(freq, magn, phase, show = False, f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)



# Datos Tina
freq, magn, phase = np.loadtxt(
    'Bode/2_Tina/DatosBodeTinaFINO.txt',
    unpack=True,
    skiprows=1,
    delimiter=None,  # acepta tab o espacios
    converters={
        0: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        1: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        2: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
    },
)
magn = 10**(magn/20)  # dB a V/V

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)

delta = 20*np.log10(max_magn/min_magn)
print("\nGain:\t\tA_0 = {max_magn}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))
P.bode_plots(freq, magn, phase, show=True, f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)
