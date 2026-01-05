import numpy as np
import matplotlib.pyplot as plt
import Analysis as A
import Plotting as P
import os

fija = 'k'

R1 = 98.1e3
R2 = 98.5e3
R3s = 67.8e3
Rfs = 32.8e3
C = 9.29e-9

tol = [5, 10, 15, 20]

if fija == 'k':

    intR3LISTA = [5, 105, 255]
    dir = 'Wave_gen/Rf/k_fija/'

    for intR3 in intR3LISTA:

        R3 = intR3 / 255 * 42.0e3

        intRf, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{intR3}_avg8_Vcc10.txt', unpack=True, skiprows=1)

        Rf = intRf / 255 * 42.0e3

        f_teo = (R2)/(4*C*(Rf+Rfs)*(R3+R3s))

        epsilon = np.abs((freq_sq - f_teo)/f_teo)*100

        plt.plot(Rf/1000, epsilon, 'o-')
        for t in tol:
            plt.axhline(y=t, linestyle='--', label=f'Tol = {t}%')
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Relative Error (%)')
            plt.legend()

            dir_out = f'Graphs/k_relativo_f/{t}/'
            if not os.path.exists(dir_out):
                os.makedirs(dir_out)
                print(f'Directory {dir_out} created.')
        plt.savefig(f'Graphs/k_relativo_f/{intR3}_0.png', dpi=300)
        plt.clf()

        for t in tol:
            dir_out = f'Graphs/k_relativo_f/{t}/'
            switch = 0
            R_left = 0
            R_right = 0
            for i in range(len(epsilon)):
                if switch == 0 and epsilon[i] < t:
                    R_right = Rf[i-1]/1000
                    # print(R_right)
                    switch = 1
                if switch == 1 and epsilon[i] > t:
                    R_left = Rf[i-1]/1000
                    # print(R_left)
                    break
            if R_right == 0:
                R_right = Rf[0]/1000
                # print(R_right)


            plt.plot(Rf/1000, f_teo, '-', label='Freq_tr', color='orange')
            plt.plot(Rf/1000, freq_sq, 's-', label='Freq_sq', color='green')
            plt.plot(Rf/1000, (f_teo-f_teo[-1])/(f_teo[0]-f_teo[-1])*(freq_sq[0]-freq_sq[-1])+freq_sq[-1], 'k--', label='Freq_sq ajustada')
            plt.scatter(Rf/1000, freq_tr, label='Freq_meas')
            plt.legend()
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Frequency (Hz)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_1.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, V_tr, 'o-')
            plt.plot(Rf/1000, V_sq, 's-')
            plt.axhline(y=10, color='red', linestyle='--')
            plt.axhline(y=10*(R3+R3s)/R2, color='blue', linestyle='--')
            plt.axhline(y=V_sq[0]*(R3+R3s)/R2, color='green', linestyle='--')
            plt.legend(['V_tr', 'V_sq', 'Vcc', 'Vcc*R3/R2', 'V_tr con V_sq real'])
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Voltaje (V)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_3.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, V_tr/V_sq, 'd-')
            plt.axhline(y=(R3+R3s)/R2, color='k', linestyle='--', label='V_tr/V_sq teo')
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('V_tr/V_sq')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_4.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, phas, 'd-')
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Phase (deg)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_5.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, DC_tr, 'o-')
            plt.plot(Rf/1000, DC_sq, 's-')
            plt.legend(['DC_tr', 'DC_sq'])
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Duty Cycle (%)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_6.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, t_up_tr*1e3, 'o-')
            plt.plot(Rf/1000, t_down_tr*1e3, 'o--')
            plt.plot(Rf/1000, t_up_sq*1e3, 's-')
            plt.plot(Rf/1000, t_down_sq*1e3, 's--')
            plt.plot(Rf/1000, (1/(2*f_teo))*1e3, 'k--', label='t_teo')
            plt.legend(['t_up_tr', 't_down_tr', 't_up_sq', 't_down_sq', 't_teo'])
            plt.xlabel('Rf (kOhm)') 
            plt.ylabel('Time (ms)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_7.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, top_tr, 'o-')
            plt.plot(Rf/1000, base_tr, 'o--')
            plt.legend(['top_tr', 'base_tr'])
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Voltage (V)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_8.png', dpi=300)
            plt.clf()

            plt.plot(Rf/1000, top_sq, 's-')
            plt.plot(Rf/1000, base_sq, 's--')
            plt.axhline(y=10, color='red', linestyle='--')
            plt.axhline(y=0, color='blue', linestyle='--')
            plt.legend(['top_sq', 'base_sq'])
            plt.xlabel('Rf (kOhm)')
            plt.ylabel('Voltage (V)')
            # plt.show()
            plt.axvline(x=R_left, color='red', linestyle='--', label='Rf limits')
            plt.title(f'Limits for tol = {t}%: R_left = {R_left:.2f} kOhm, R_right = {R_right:.2f} kOhm')
            plt.axvline(x=R_right, color='red', linestyle='--')
            plt.savefig(dir_out+f'{intR3}_9.png', dpi=300)
            plt.clf()


elif fija == 'f':

    fLISTA = np.arange(330, 1091, 20)
    dir = 'Wave_gen/Rf/f_fija/'

    for f in fLISTA:

        intRf, intR3, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{f:.2f}_avg8_Vcc10.txt', unpack=True, skiprows=1)

        R3 = intR3 / 255 * 42.0e3
        Rf = intRf / 255 * 42.0e3

        K = (R3+R3s)/R2

        f_teo = (R2)/(4*C*(Rf+Rfs)*(R3+R3s))

        plt.plot(K, f_teo, '-', label='Freq_tr', color='orange')
        plt.plot(K, freq_sq, 's-', label='Freq_sq', color='green')
        plt.scatter(K, freq_tr, label='Freq_meas')
        plt.legend()
        plt.xlabel('K')
        plt.ylabel('Frequency (Hz)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_1.png', dpi=300)
        plt.clf()

        plt.plot(f_teo, freq_tr, 'o')
        plt.plot(f_teo, f_teo, 'k--', label='y=x')
        plt.xlabel('Freq_teo (Hz)')
        plt.ylabel('Freq_meas (Hz)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_2.png', dpi=300)
        plt.clf()

        plt.plot(K, V_tr, 'o-')
        plt.plot(K, V_sq, 's-')
        plt.axhline(y=10, color='red', linestyle='--')
        plt.plot(K, 10*K, color='blue', linestyle='--')
        plt.plot(K, V_sq[0]*K, color='green', linestyle='--')
        plt.legend(['V_tr', 'V_sq', 'Vcc', 'Vcc*R3/R2', 'V_tr con V_sq real'])
        plt.xlabel('K')
        plt.ylabel('Voltaje (V)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_3.png', dpi=300)
        plt.clf()

        plt.plot(K, V_tr/V_sq, 'd-')
        plt.plot(K, K, color='k', linestyle='--', label='V_tr/V_sq teo')
        plt.xlabel('K')
        plt.ylabel('V_tr/V_sq')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_4.png', dpi=300)
        plt.clf()

        plt.plot(K, phas, 'd-')
        plt.xlabel('K')
        plt.ylabel('Phase (deg)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_5.png', dpi=300)
        plt.clf()

        plt.plot(K, DC_tr, 'o-')
        plt.plot(K, DC_sq, 's-')
        plt.legend(['DC_tr', 'DC_sq'])
        plt.xlabel('K')
        plt.ylabel('Duty Cycle (%)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_6.png', dpi=300)
        plt.clf()

        plt.plot(K, t_up_tr*1e3, 'o-')
        plt.plot(K, t_down_tr*1e3, 'o--')
        plt.plot(K, t_up_sq*1e3, 's-')
        plt.plot(K, t_down_sq*1e3, 's--')
        plt.plot(K, (1/(2*f_teo))*1e3, 'k--', label='t_teo')
        plt.legend(['t_up_tr', 't_down_tr', 't_up_sq', 't_down_sq', 't_teo'])
        plt.xlabel('K') 
        plt.ylabel('Time (ms)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_7.png', dpi=300)
        plt.clf()

        plt.plot(K, top_tr, 'o-')
        plt.plot(K, base_tr, 'o--')
        plt.legend(['top_tr', 'base_tr'])
        plt.xlabel('K')
        plt.ylabel('Voltage (V)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_8.png', dpi=300)
        plt.clf()

        plt.plot(K, top_sq, 's-')
        plt.plot(K, base_sq, 's--')
        plt.axhline(y=10, color='red', linestyle='--')
        plt.axhline(y=0, color='blue', linestyle='--')
        plt.legend(['top_sq', 'base_sq'])
        plt.xlabel('K')
        plt.ylabel('Voltage (V)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_9.png', dpi=300)
        plt.clf()

# input("Enter para continuar.")
# plt.show()
# plt.close('all')