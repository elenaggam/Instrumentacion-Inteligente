import numpy as np
import matplotlib.pyplot as plt

intR3 = 105
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


switch = 0
R_left = 0
R_right = 0
for i in range(len(epsilon)):
    if switch == 0 and epsilon[i] < tol:
        R_right = Rf[i-1]/1000
        f_right = freq_sq[i-1]
        print(R_right)
        switch = 1
    if switch == 1 and epsilon[i] > tol:
        R_left = Rf[i-1]/1000
        f_left = freq_sq[i-1]
        print(R_left)
        break
if R_right == 0:
    R_right = Rf[0]/1000
    print(R_right)



IS = np.abs(t_up_tr - t_down_tr) / (t_up_tr + t_down_tr) * 100

plt.plot(freq_sq, IS, 'o-')
plt.xlabel('freq (Hz)')
plt.ylabel('Indice de simetria (%)')
plt.axvline(x=f_left, color='red', linestyle='--', label='Rf limits')
plt.axvline(x=f_right, color='red', linestyle='--')
plt.title('Indice de simetria vs frecuencia')
plt.show()


plt.plot(freq_sq, DC_tr, 'o-')
plt.plot(freq_sq, DC_sq, 's-')
plt.legend(['DC_tr', 'DC_sq'])
plt.xlabel('Rf (kOhm)')
plt.ylabel('Duty Cycle (%)')
# plt.show()
plt.axvline(x=f_left, color='red', linestyle='--', label='Rf limits')
plt.axvline(x=f_right, color='red', linestyle='--')
plt.show()


plt.plot(freq_sq, t_up_tr*1e3, 'o-')
plt.plot(freq_sq, t_down_tr*1e3, 'o--')
plt.plot(freq_sq, t_up_sq*1e3, 's-')
plt.plot(freq_sq, t_down_sq*1e3, 's--')
plt.plot(freq_sq, (1/(2*f_teo))*1e3, 'k--', label='t_teo')
plt.legend(['t_up_tr', 't_down_tr', 't_up_sq', 't_down_sq', 't_teo'])
plt.xlabel('Rf (kOhm)') 
plt.ylabel('Time (ms)')
# plt.show()
plt.axvline(x=f_left, color='red', linestyle='--', label='Rf limits')
plt.axvline(x=f_right, color='red', linestyle='--')
plt.show()


