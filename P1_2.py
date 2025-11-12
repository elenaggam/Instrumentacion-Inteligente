import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P


# Medidas caja (grueso)
freq, vi, vo, phase = np.loadtxt('Bode/1_Caja/DEF_flog100-10000000-10000000_steps30_avg8_Vin1.txt', unpack=True)
magn = vo/vi

P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CG_All')

input("Enter para continuar.")
plt.close('all')


# Medidas caja (fino)
freq, vi, vo, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000_steps70_avg8_Vin1.txt', unpack=True)
magn = vo/vi

P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CF_All', infLim=-44)

input("Enter para continuar.")
plt.close('all')


# Medidas caja (fino + medidas)
freq, vi, vo, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000_steps70_avg8_Vin1.txt', unpack=True)
magn = vo/vi

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)
delta = 20*np.log10(max_magn/min_magn)
print("\n\nCAJA\nGain:\t\tA_0 = {max_magn:.3f}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CFM_All', infLim=-44, f_low=f_low, f_cut=f_cut)

input("Enter para continuar.")
plt.close('all')


# Datos Tina
freq, magn, phase = np.loadtxt('Bode/2_Tina/DatosBodeTinaFINO.txt', unpack=True, skiprows=1, delimiter=None,
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
print("\n\nTINA\nGain:\t\tA_0 = {max_magn:.3f}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

P.bode_diagrams(freq, magn, phase, infLim=-44, directory='Bode/2_Tina/Bode_Tina_All')

input("Enter para continuar.")
plt.close('all')


# Medidas montaje
freq, vi, vo, phase = np.loadtxt('Bode/3_Montaje/flog1000-1000000-1000000_steps55_avg8_Vin1.txt', unpack=True)
magn = vo/vi

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)
delta = 20*np.log10(max_magn/min_magn)
print("\n\nEXP\nGain:\t\tA_0 = {max_magn:.3f}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

P.bode_diagrams(freq, magn, phase, directory='Bode/3_Montaje/Bode_EXP_All')

input("Enter para continuar.")
plt.close('all')


# TINA vs CAJA
freq, vi, vo, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000_steps70_avg8_Vin1.txt', unpack=True)
magn = vo/vi
freq2, magn2, phase2 = np.loadtxt('Bode/2_Tina/DatosBodeTinaFINO.txt', unpack=True, skiprows=1, delimiter=None,
    converters={
        0: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        1: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        2: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
    },
)
magn2 = 10**(magn2/20)  # dB a V/V

P.bode_diagrams(freq, magn, phase, infLim=-44, label1='Medida Caja', label2='Simulación TINA', freq2=freq2, magn2=magn2, phase2=phase2, directory='Bode/2_Tina/Tina_vs_Caja_All')

input("Enter para continuar.")
plt.close('all')


# EXP vs CAJA
freq, vi, vo, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000_steps70_avg8_Vin1.txt', unpack=True)
magn = vo/vi
freq2, vi2, vo2, phase2 = np.loadtxt('Bode/3_Montaje/flog1000-1000000-1000000_steps55_avg8_Vin1.txt', unpack=True)
magn2 = vo2/vi2

freq2 = freq2[:-5]
vi2 = vi2[:-5]
magn2 = magn2[:-5]
phase2 = phase2[:-5]

P.bode_diagrams(freq, magn, phase, infLim=-44, label1='Medida Caja', label2='Medida Montaje', freq2=freq2, magn2=magn2, phase2=phase2, directory='Bode/3_Montaje/Exp_vs_Caja_All')

input("Enter para continuar.")
plt.close('all')