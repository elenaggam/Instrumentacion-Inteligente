import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P

dir = 'Wave_gen/Rf/k_fija/'
intRf, V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+'20_avg8_Vcc10.txt', unpack=True, skiprows=1)

R2 = 226
R1 = intR*42/255  # Valor real de R1 en kOhm
R3 = R2*R1/(R2+R1)  # Valor real de R3 en kOhm
Rf = 81.7
C = 9.29
f_teo = (R1+R2)/(4*C*Rf*R1)*1000 # f en kHz
plt.plot(R1, V_tr, 'o-', label='V_tr')

plt.legend()
plt.xlabel('R1 (kOhm)')
plt.ylabel('Voltage (V)')
plt.show()
plt.plot(R1, V_sq, 's-', label='V_sq')
plt.legend()
plt.xlabel('R1 (kOhm)')
plt.ylabel('Voltage (V)')
plt.show()
plt.plot(R1, freq_tr/1000, 'o--', label='Freq_tr')
plt.plot(R1, f_teo, 'k-', label='Freq_teo')
plt.xlabel('R1 (kOhm)')
plt.ylabel('Frequency (kHz)')
plt.legend()
plt.show()
plt.plot(R1, freq_sq/1000, 's--', label='Freq_sq')
plt.plot(R1, f_teo, 'k-', label='Freq_teo')
plt.xlabel('R1 (kOhm)')
plt.ylabel('Frequency (kHz)')
plt.legend()
plt.show()
plt.plot(R1, phas, 'd-', label='Phase')
plt.legend()
plt.xlabel('R1 (kOhm)')
plt.ylabel('Phase (deg)')
plt.show()



input("Enter para continuar.")
plt.close('all')

