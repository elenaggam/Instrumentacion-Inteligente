import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P


# Medidas caja (grueso)
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog100-10000000.0-10000000.0_steps30_avg8_Vin1.txt', unpack=True)

# P.bode_magnitude(freq, magn, show = True, directory='Bode/1_Caja/DEF1_')
# P.bode_phase(freq, phase, deltaTicks=90, show = True, directory='Bode/1_Caja/DEF1_')
P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CG_All')

input("Enter para continuar.")
plt.close('all')


# Medidas caja (fino)
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000.0_steps70_avg8_Vin1.txt', unpack=True)

# P.bode_magnitude(freq, magn, show = True, directory='Bode/1_Caja/DEF2_')
# P.bode_phase(freq, phase, show = True, directory='Bode/1_Caja/DEF2_')
P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CF_All', infLim=-44)

input("Enter para continuar.")
plt.close('all')


# Medidas caja (fino + medidas)
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000.0_steps70_avg8_Vin1.txt', unpack=True)

f_low, max_magn = A.bandwidth_gain(freq, magn)
f_cut, min_magn = A.stopband_attenuation(freq, magn)
delta = 20*np.log10(max_magn/min_magn)
print("\nGain:\t\tA_0 = {max_magn}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

# P.bode_magnitude(freq, magn, show = True, directory='Bode/1_Caja/DEF3_', f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)
# P.bode_phase(freq, phase, show = True, directory='Bode/1_Caja/DEF3_', f_low=f_low, f_cut=f_cut)
P.bode_diagrams(freq, magn, phase, directory='Bode/1_Caja/Bode_CFM_All', infLim=-44, f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)

input("Enter para continuar.")
plt.close('all')


# Datos Tina
freq, magn, phase = np.loadtxt('Bode/2_Tina/DatosBodeTinaFINO.txt',
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

# f_low, max_magn = A.bandwidth_gain(freq, magn)
# f_cut, min_magn = A.stopband_attenuation(freq, magn)
# delta = 20*np.log10(max_magn/min_magn)
# print("\nGain:\t\tA_0 = {max_magn}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

# P.bode_magnitude(freq, magn, show = True, directory='Bode/2_Tina/')
# P.bode_phase(freq, phase, show = True, directory='Bode/2_Tina/')
P.bode_diagrams(freq, magn, phase, directory='Bode/2_Tina/Bode_Tina_All', infLim=-44)

input("Enter para continuar.")
plt.close('all')


# Medidas montaje
freq, vi, magn, phase = np.loadtxt('Bode/3_Montaje/flog1000-1000000.0-1000000.0_steps55_avg8_Vin1.txt', unpack=True)

# f_low, max_magn = A.bandwidth_gain(freq, magn)
# f_cut, min_magn = A.stopband_attenuation(freq, magn)
# delta = 20*np.log10(max_magn/min_magn)
# print("\nGain:\t\tA_0 = {max_magn}\nf passband:\tf_c = {f_low:.0f}\nf stopband:\tf_s = {f_cut:.0f}\nsb attenuation: A_sb = {delta:.2f} dB\n".format(max_magn=max_magn, f_low=f_low, f_cut=f_cut, delta=delta))

# P.bode_magnitude(freq, magn, show = True, directory='Bode/3_Montaje/')
# P.bode_phase(freq, phase, show = True, directory='Bode/3_Montaje/')
P.bode_diagrams(freq, magn, phase, directory='Bode/3_Montaje/Bode_EXP_All')

input("Enter para continuar.")
plt.close('all')


# TINA vs CAJA
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000.0_steps70_avg8_Vin1.txt', unpack=True)
freq2, magn2, phase2 = np.loadtxt('Bode/2_Tina/DatosBodeTinaFINO.txt',
    unpack=True,
    skiprows=1,
    delimiter=None,  # acepta tab o espacios
    converters={
        0: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        1: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
        2: lambda s: float(s.decode().replace(',', '.') if isinstance(s, bytes) else s.replace(',', '.')),
    },
)
magn2 = 10**(magn2/20)  # dB a V/V

P.bode_diagrams(freq, magn, phase, label1='Medida Caja', label2='Simulación TINA', freq2=freq2, magn2=magn2, phase2=phase2, directory='Bode/2_Tina/Tina_vs_Caja_All')

input("Enter para continuar.")
plt.close('all')


# EXP vs CAJA
freq, vi, magn, phase = np.loadtxt('Bode/1_Caja/DEF_flog1000-40000-500000.0_steps70_avg8_Vin1.txt', unpack=True)
freq2, vi2, magn2, phase2 = np.loadtxt('Bode/3_Montaje/flog1000-1000000.0-1000000.0_steps55_avg8_Vin1.txt', unpack=True)


P.bode_diagrams(freq, magn, phase, label1='Medida Caja', label2='Medida Montaje', freq2=freq2, magn2=magn2, phase2=phase2, directory='Bode/3_Montaje/Exp_vs_Caja_All')

input("Enter para continuar.")
plt.close('all')