import numpy as np
import matplotlib.pyplot as plt

intR3 = 255
dir = 'Wave_gen/Rf/k_fija/'

intRf, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{intR3}_avg8_Vcc10.txt', unpack=True, skiprows=1)

R1 = 98.1e3
R2 = 98.5e3
R3s = 67.8e3
Rfs = 32.8e3
C = 9.29e-9
Rf = intRf / 255 * 42.0e3
R3 = intR3 / 255 * 42.0e3
f_teo = (R2)/(4*C*(Rf+Rfs)*(R3+R3s))

epsilon = np.abs((freq_sq - f_teo)/f_teo)*100
tol = 5

plt.plot(Rf/1000, epsilon, 'o-')
plt.axhline(y=tol, color='red', linestyle='--', label=f'Tol = {tol}%')
plt.axhline(y=2*tol, color='green', linestyle='--', label=f'Tol = {2*tol}%')
plt.xlabel('Rf (kOhm)')
plt.ylabel('Relative Error (%)')
plt.legend()
plt.show()

switch = 0
R_left = 0
R_right = 0
for i in range(len(epsilon)):
    if switch == 0 and epsilon[i] < tol:
        R_right = Rf[i-1]/1000
        print(R_right)
        switch = 1
    if switch == 1 and epsilon[i] > tol:
        R_left = Rf[i-1]/1000
        print(R_left)
        break
if R_right == 0:
    R_right = Rf[0]/1000
    print(R_right)


plt.plot(Rf/1000, f_teo, '-', label='Freq_tr', color='orange')
plt.plot(Rf/1000, freq_sq, 's-', label='Freq_sq', color='green')
plt.plot(Rf/1000, (f_teo-f_teo[-1])/(f_teo[0]-f_teo[-1])*(freq_sq[0]-freq_sq[-1])+freq_sq[-1], 'k--', label='Freq_sq ajustada')
plt.scatter(Rf/1000, freq_tr, label='Freq_meas')
plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
plt.title(f'Limits for tol = {tol}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
plt.axvline(x=R_right, color='red', linestyle='--')
plt.legend()
plt.xlabel('Rf (kOhm)')
plt.ylabel('Frequency (Hz)')
plt.show()
