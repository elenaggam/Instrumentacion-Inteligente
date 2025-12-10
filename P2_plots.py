import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P


intR, V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq = np.loadtxt('Wave_gen/R1_R3/new_avg8_Vcc10.txt', unpack=True, skiprows=1)


R1 = intR*42/255  # Valor real de R1 en kOhm

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
plt.plot(R1, freq_tr, 'o--', label='Freq_tr')
plt.xlabel('R1 (kOhm)')
plt.ylabel('Frequency (Hz)')
plt.legend()
plt.show()
plt.plot(R1, freq_sq, 's--', label='Freq_sq')
plt.xlabel('R1 (kOhm)')
plt.ylabel('Frequency (Hz)')
plt.legend()
plt.show()
plt.plot(R1, phas, 'd-', label='Phase')
plt.legend()
plt.xlabel('R1 (kOhm)')
plt.ylabel('Phase (deg)')
plt.show()



input("Enter para continuar.")
plt.close('all')

