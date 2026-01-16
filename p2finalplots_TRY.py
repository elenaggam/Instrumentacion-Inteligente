import numpy as np
import matplotlib.pyplot as plt
import os

color_palette = ["#003F5C", "#EE1E1E", "#7A5195", "#1051C0",
                 '#FF7F0E', "#00B73A"]


def get_lims(a, t, f, Rf):
    # vamos de intRF alto a bajo, de frecs bajas a altas
    # a tiene un minimo 
    switch = 0
    R_low = Rf[-1]/1000
    R_high = Rf[0]/1000
    f_low = f[0]
    f_high = f[-1]

    for i in range(len(a)):
        if switch == 0 and a[i] < t:
            R_high = Rf[i]/1000
            f_low = f[i]
            # print(R_right)
            switch = 1
        if switch == 1 and a[i] > t:
            R_low = Rf[i-1]/1000
            f_high = f[i-1]
            # print(R_left)
            break

    return [R_low, R_high], [f_low, f_high]

def plot_limits(a, b, label=None, color='gray'):
    if label is not None:
        plt.axvline(x=a, color=color, linestyle='--', zorder=10, label=label)
    else: 
        plt.axvline(x=a, color=color, linestyle='--', zorder=10)
    plt.axvline(x=b, color=color, linestyle='--', zorder=10)

def get_intersection(lim1, lim2):
    sorted = np.sort([lim1[0], lim1[1], lim2[0], lim2[1]])
    return [sorted[1], sorted[2]]

fija = 'f'
criterio = 'c'  # a: simetría, b: frecuencia, c: ambas

R1 = 98.1e3
R2 = 98.5e3
R3s = 67.8e3
Rfs = 32.8e3
C = 9.29e-9
R_1 = [None, None]
f_1 = [None, None]
R_2 = [None, None]
f_2 = [None, None]

t = 10 # tol percentage
Ne = []
Ns = []
max_N = 0
j = 0
if fija == 'k':

    intR3LISTA = [5, 30, 55, 80, 105, 127, 130, 155, 155, 180, 205, 230, 255]
    dir = 'Wave_gen/Rf/k_fija/'

    for intR3 in intR3LISTA:

        R3 = intR3 / 255 * 42.0e3

        intRf, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{intR3}_avg8_Vcc10.txt', unpack=True, skiprows=1)

        Rf = intRf / 255 * 42.0e3

        f_teo = (R2)/(4*C*(Rf+Rfs)*(R3+R3s))


        epsilon = np.abs((freq_sq - f_teo)/f_teo)*100
        S = np.abs(t_up_tr - t_down_tr) / (t_up_tr + t_down_tr) * 100
        ns = 0
        ne = 0
        for i in range(len(S)):
            if S[i] < t:
                ns += 1
            if epsilon[i] < t:
                ne += 1
        Ne.append(ne)
        Ns.append(ns)
        n_aux=0
        if criterio == 'c': #simetría y frecuencia
            for i in range(len(S)):
                if S[i] < t and epsilon[i] < t:
                    n_aux +=1
            if n_aux > max_N:
                max_N = n_aux
                j = intR3LISTA.index(intR3)
            # print(f'R3={intR3}, N
        
  
    if criterio == 'a': #primero simetría
        index = np.argmax(Ns)
        intR3 = intR3LISTA[index]

    elif criterio == 'b': #primero frecuencia
        index = np.argmax(Ne)
        intR3 = intR3LISTA[index]

    elif criterio == 'c': #simetría y frecuencia
        intR3 = intR3LISTA[j]
    

    dir_out = f'Graphs/k_relativo_f/{t}/'+criterio+'/'
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    intRf, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{intR3}_avg8_Vcc10.txt', unpack=True, skiprows=1)
    Rf = intRf / 255 * 42.0e3 + Rfs
    R3 = intR3 / 255 * 42.0e3 + R3s
    f_teo = (R2)/(4*C*(Rf)*(R3))

    S = np.abs(t_up_tr - t_down_tr) / (t_up_tr + t_down_tr) * 100
    epsilon = np.abs((freq_sq - f_teo)/f_teo)*100

    if criterio == 'a':
        R_1, f_1 = get_lims(S, t, freq_tr, Rf)
    elif criterio == 'b':
        R_1, f_1 = get_lims(epsilon, t, freq_tr, Rf)
    elif criterio == 'c':
        R_S, f_S = get_lims(S, t, freq_tr, Rf)
        R_eps, f_eps = get_lims(epsilon, t, freq_tr, Rf)
        R_1 = get_intersection(R_S, R_eps)
        f_1 = get_intersection(f_S, f_eps)
    else:
        print("Criterio no válido")
        exit()

    '''
    # ns = 0
    # ne = 0
    # N = 0
    # avg_S = 0
    # avg_epsilon = 0
    # for i in range(len(S)):
    #     if S[i] < t:
    #         ns +=1
    #     if epsilon[i] < t:
    #         ne +=1
    #     if S[i] < t and epsilon[i] < t:
    #         avg_epsilon += epsilon[i]
    #         avg_S += S[i]
    #         N +=1

    # # plt.plot(intR3LISTA, Ns, 'o-')
    # # plt.xlabel('R3 (int)')
    # # plt.ylabel('Number of points under tolerance')
    # # plt.savefig(dir_out+f'{intR3}_Ns_points.png', dpi=300)
    # # plt.clf()

    # # plt.plot(intR3LISTA, Ne, 'o-')
    # # plt.xlabel('R3 (int)')
    # # plt.ylabel('Number of points under tolerance')
    # # plt.savefig(dir_out+f'{intR3}_Ne_points.png', dpi=300)
    # # plt.clf()

    # avg_S /= N
    # avg_epsilon /= N
    # file = open(dir_out+f'{intR3}_log.txt', 'w')
    # file.write(f'Best R3 int: {intR3}\n')
    # file.write(f'Which gives max Ns = {ns}\n')
    # file.write(f'Which gives max Ne = {ne}\n')
    # file.write(f'Which gives max N_intersection = {N}\n')
    # file.write(f'average S = {avg_S:.2f} % in intersection\n')
    # file.write(f'average epsilon = {avg_epsilon:.2f} % in intersection\n')
    # file.write(f'R limts (kOhm): R_S = {R_1[0]:.2f} - {R_1[1]:.2f}\n')
    # file.write(f'f limits (Hz): f_S = {f_1[0]:.1f} - {f_1[1]:.1f}\n')
    # file.write(f'R limits (kOhm): R_eps = {R_2[0]:.2f} - {R_2[1]:.2f}\n')
    # file.write(f'f limits (Hz): f_eps = {f_2[0]:.1f} - {f_2[1]:.1f}\n')
    # file.close()

    # plt.plot(freq_tr, S, 'o-')
    # plt.axhline(y=t, color='grey', linestyle='--', label='tolerance')
    # plt.xlabel('f (Hz)')
    # plt.ylabel('Asymmetry (%)')
    # plot_limits(f_2[0], f_2[1], color='orange')
    # plot_limits(f_1[0], f_1[1])
    # plt.legend()
    # plt.savefig(dir_out+f'{intR3}_symmetry.png', dpi=300)
    # plt.clf()
    
    # plt.plot(freq_tr, epsilon, 'o-')
    # plt.axhline(y=t, color='grey', linestyle='--', label='tolerance')
    # plt.xlabel('f (Hz)')
    # plt.ylabel('Frequency error (%)')
    # plot_limits(f_2[0], f_2[1], color='orange')
    # plot_limits(f_1[0], f_1[1])
    # plt.legend()
    # plt.savefig(dir_out+f'{intR3}_frequency_error.png', dpi=300)
    # plt.clf()


'''

    print(f'Vpp_tr={np.average(V_tr):.2f} +- {np.std(V_tr):.2f} V')
    print(f'Vpp_sq={np.average(V_sq):.2f} +- {np.std(V_sq):.2f} V')
    print(f'Dc_tr={np.average(DC_tr):.2f} +- {np.std(DC_tr):.2f} V')
    print(f'base_sq={np.average(base_sq):.2f} +- {np.std(base_sq):.2f} V, top_sq={np.average(top_sq):.2f} +- {np.std(top_sq):.2f} V')
    print(f'base_tr={np.average(base_tr):.2f} +- {np.std(base_tr):.2f} V, top_tr={np.average(top_tr):.2f} +- {np.std(top_tr):.2f} V')
    
    phas2 =[]
    for i in range(len(phas)):
        if S[i] < t and epsilon[i] < t:
            phas2.append(phas[i])

    errp = np.sqrt
    print(f'phase={np.average(phas):.2f} +- {np.std(phas):.2f} deg or {np.average(phas2):.2f} +- {np.std(phas2):.2f} deg for S<{t}%')

    plt.plot(Rf/1000, f_teo, '-', lw=2, label=r'$f_{teo}$', color=color_palette[5], zorder = 2)
    plt.plot(Rf/1000, freq_sq, 's-', label=r'$f_{□,exp}$', color=color_palette[3], zorder = 3, markersize =8)
    plt.plot(Rf/1000, freq_tr, 'o-', label=r'$f_{\triangle,exp}$', color = color_palette[4], zorder = 4, markersize =5)
    plt.grid(zorder=0)
    # plt.plot(Rf/1000, (f_teo-f_teo[-1])/(f_teo[0]-f_teo[-1])*(freq_sq[0]-freq_sq[-1])+freq_sq[-1], 'k--', label='Freq_sq ajustada')

    plt.xlabel(r'$R_f$ (k$\Omega$)', fontsize=14)
    plt.ylabel(r'$f$ (Hz)', fontsize=14)
    l = '$S<10\%$'
    plot_limits(R_1[0], R_1[1], color='gray')
    # plot_limits(R_2[0], R_2[1], color='green')
    # plot_limits(R[0], R[1])
    plt.legend(fontsize=14, loc='upper right')
    plt.xlim(Rf[-1]/1000-0.8, Rf[0]/1000+0.8)
    plt.xticks(np.arange(int(Rf[-1]/1000-0.5), int(Rf[0]/1000+1.5), 7), fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(dir_out+f'{intR3}_1.png', dpi=300, bbox_inches='tight')
    plt.clf()



    plt.plot(freq_tr, V_tr, 'o-')
    plt.plot(freq_tr, V_sq, 's-')
    plt.axhline(y=10, color='red', linestyle='--')
    plt.axhline(y=10*(R3+R3s)/R2, color='blue', linestyle='--')
    plt.axhline(y=V_sq[0]*(R3+R3s)/R2, color='green', linestyle='--')
    plt.legend(['V_tr', 'V_sq', 'Vcc', 'Vcc*R3/R2', 'V_tr con V_sq real'])
    plt.xlabel('f (Hz)')
    plt.ylabel('Voltaje (V)')
    plot_limits(f_1[0], f_1[1], color='orange')

    plt.savefig(dir_out+f'{intR3}_3.png', dpi=300)
    plt.clf()

    plt.plot(freq_tr, V_tr/V_sq, 'd-')
    plt.axhline(y=(R3)/R2, color='k', linestyle='--', label='V_tr/V_sq teo')
    plt.xlabel('f (Hz)')
    plt.ylabel('V_tr/V_sq')
    plot_limits(f_1[0], f_1[1], color='orange')
    # plot_limits(f_2[0], f_2[1], color='green')
    # plot_limits(f[0], f[1])
    plt.savefig(dir_out+f'{intR3}_4.png', dpi=300)
    plt.clf()

    plt.grid(zorder=1)
    plt.plot(freq_tr, phas, 'o-', color=color_palette[3], markersize=7, zorder=2)
    plt.xlabel(r'$f$ (Hz)', fontsize=14)
    plt.ylabel(r'Desfase ($^\circ$)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plot_limits(f_1[0], f_1[1])
    # plot_limits(f_2[0], f_2[1], color='green')
    # plot_limits(f[0], f[1])
    plt.savefig(dir_out+f'{intR3}_5.png', dpi=300, bbox_inches='tight')
    plt.clf()

    plt.plot(freq_tr, DC_tr, 'o-')
    plt.plot(freq_tr, DC_sq, 's-')
    plt.legend(['DC_tr', 'DC_sq'])
    plt.xlabel('f (Hz)')
    plt.ylabel('Duty Cycle (%)')
    plot_limits(f_1[0], f_1[1], color='orange')
    # plot_limits(f_2[0], f_2[1], color='green')
    # plot_limits(f[0], f[1])
    plt.savefig(dir_out+f'{intR3}_6.png', dpi=300)
    plt.clf()

    plt.grid(zorder=1)
    plt.plot(freq_tr, t_up_sq*1e3, 's-', zorder=3, label = r'$t_{u,□}$', markersize=8, color = color_palette[-1])
    plt.plot(freq_tr, t_down_sq*1e3, 'o-', zorder=4, label = r'$t_{d,□}$', markersize=5, color = color_palette[1]) 
    plt.plot(freq_tr, t_up_tr*1e3, 's-', zorder=4, label = r'$t_{u,\triangle}$', markersize=6, color = color_palette[3]) 
    plt.plot(freq_tr, t_down_tr*1e3, 'o-', zorder=4, label = r'$t_{d,\triangle}$', markersize=6, color = color_palette[4]) 
    plt.plot(freq_tr, (1/(2*f_teo))*1e3, '-', lw=2, label=r'$t_{teo}$', zorder=2, color = color_palette[0]) 
    #plt.plot(freq_tr, (top_sq-base_sq)/(4*freq_tr*(DC_tr-base_sq))*1e3, 'k--', label=r'$up$', zorder=1)
    #plt.plot(freq_tr, (top_sq-base_sq)/(4*freq_tr*(top_sq-DC_tr))*1e3, 'k-.', label=r'$down$', zorder=1)
    plt.xlabel('$f$ (Hz)', fontsize=14) 
    plt.ylabel('$t$ (ms)', fontsize=14)
    plot_limits(f_1[0], f_1[1], color='gray')
    # plot_limits(R_2[0], R_2[1], color='green')
    # plot_limits(R[0], R[1])
    plt.legend(fontsize=14,  bbox_to_anchor=(0.95, 1))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(dir_out+f'{intR3}_7.png', dpi=300, bbox_inches='tight')
    plt.clf()

    plt.plot(freq_tr, top_tr, 'o-')
    plt.plot(freq_tr, base_tr, 'o--')
    plt.legend(['top_tr', 'base_tr'])
    plt.xlabel('f (Hz)')
    plt.ylabel('Voltage (V)')
    plot_limits(f_1[0], f_1[1], color='orange')
    # plot_limits(f_2[0], f_2[1], color='green')
    # plot_limits(f[0], f[1])
    plt.savefig(dir_out+f'{intR3}_8.png', dpi=300)
    plt.clf()

    plt.plot(freq_tr, top_sq, 's-')
    plt.plot(freq_tr, base_sq, 's--')
    plt.axhline(y=10, color='red', linestyle='--')
    plt.axhline(y=0, color='blue', linestyle='--')
    plt.legend(['top_sq', 'base_sq'])
    plt.xlabel('f (Hz)')
    plt.ylabel('Voltage (V)')
    plot_limits(f_1[0], f_1[1], color='orange')
    # plot_limits(f_2[0], f_2[1], color='green')
    # plot_limits(f[0], f[1])
    plt.savefig(dir_out+f'{intR3}_9.png', dpi=300)
    plt.clf()


elif fija == 'f':

    fLISTA = [550]
    dir = 'Wave_gen/Rf/f_fija/'

    for f in fLISTA:

        intRf, intR3, freq_tr, V_tr, DC_tr, freq_sq, V_sq, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = np.loadtxt(dir+f'{f:.2f}_avg8_Vcc10.txt', unpack=True, skiprows=1)

        R3 = intR3 / 255 * 42.0e3 + R3s
        Rf = intRf / 255 * 42.0e3 + Rfs

        K = R3/R2

        f_teo = (R2)/(4*C*Rf*R3)

     
        plt.grid(zorder=0)
        plt.plot(K, f_teo, '-', lw=2, label=r'$f_{teo}$', color=color_palette[5], zorder = 4)
        plt.plot(K, freq_sq, 's-', label=r'$f_{□,exp}$', color=color_palette[3], zorder = 2, markersize =7)
        plt.plot(K, freq_tr, 'o-', label=r'$f_{\triangle,exp}$', color = color_palette[4], zorder = 3, markersize =5)
        plt.legend()
        plt.xlabel(r'$k$', fontsize=14)
        plt.ylabel(r'$f$ (Hz)', fontsize=14)
        plt.legend(fontsize=14, loc='upper right')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12) 
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_1.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.plot(f_teo, freq_tr, 'o')
        plt.plot(f_teo, f_teo, 'k--', label='y=x')
        plt.xlabel('Freq_teo (Hz)')
        plt.ylabel('Freq_meas (Hz)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_2.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.grid(zorder=0)
        plt.plot(K, V_tr, 'o-', label=r'$V_{pp,\triangle}$', color = color_palette[4], zorder = 3, markersize =6)
        plt.plot(K, V_sq, 's-', label=r'$V_{pp,□}$', color=color_palette[3], zorder = 2, markersize =6)
        plt.axhline(y=10, color='gray', linestyle='--', zorder=1, label='$V_{cc}$')
        plt.plot(K, V_sq[0]*K, color='green', linestyle='--', label=r'$V_{pp,□}\cdot k$', zorder=4)
        plt.legend(fontsize=14, loc='lower right')
        plt.xlabel(r'$k$', fontsize=14)
        plt.ylabel(r'$V_{pp}$ (V)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_3.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.plot(K, V_tr/V_sq, 'd-')
        plt.plot(K, K, color='k', linestyle='--', label='V_tr/V_sq teo')
        plt.xlabel('K')
        plt.ylabel('V_tr/V_sq')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_4.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.grid(zorder=0)
        plt.plot(K, phas, 'o-', zorder=2, markersize=6)
        plt.xlabel(r'$k$', fontsize=14)
        plt.ylabel(r'Desfase ($^\circ$)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_5.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.plot(K, DC_tr, 'o-')
        plt.plot(K, DC_sq, 's-')
        plt.legend(['DC_tr', 'DC_sq'])
        plt.xlabel('K')
        plt.ylabel('Duty Cycle (%)')
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_6.png', dpi=300, bbox_inches='tight')
        plt.clf()

        plt.grid(zorder=0)
        plt.plot(K, t_up_sq*1e3, 's-', zorder=3, label = r'$t_{u,□}$', markersize=6, color = color_palette[-1])
        plt.plot(K, t_down_sq*1e3, 'o-', zorder=4, label = r'$t_{d,□}$', markersize=6, color = color_palette[1]) 
        plt.plot(K, t_up_tr*1e3, 's-', zorder=4, label = r'$t_{u,\triangle}$', markersize=6, color = color_palette[3]) 
        plt.plot(K, t_down_tr*1e3, 'o-', zorder=4, label = r'$t_{d,\triangle}$', markersize=6, color = color_palette[4]) 
        plt.plot(K, (1/(2*f_teo))*1e3, '-', lw=2, label=r'$t_{teo}$', zorder=2, color = color_palette[0]) 
        plt.legend(fontsize=14,  loc='center right')
        plt.xlabel(r'$k$', fontsize=14) 
        plt.ylabel(r'$t$ (ms)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_7.png', dpi=300, bbox_inches='tight')
        plt.clf()
    
        plt.grid(zorder=0)
        plt.plot(K, top_sq, 's-', markersize=6, color = color_palette[3], zorder=3, label = r'$V_{□}^{\uparrow}$')
        plt.plot(K, base_sq, 's--', zorder=4, label = r'$V_{□}^{\downarrow}$', markersize=6, color = color_palette[-1])
        plt.plot(K, top_tr, 'o-', zorder=4, label = r'$V_{\triangle}^{\uparrow}$', markersize=6, color = color_palette[4])
        plt.plot(K, base_tr, 'o--', zorder=4, label = r'$V_{\triangle}^{\downarrow}$', markersize=6, color = color_palette[1])
        plt.legend(fontsize=14, loc='center right')
        plt.xlabel(r'$k$', fontsize=14)
        plt.ylabel(r'$V$ (V)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # plt.show()
        plt.savefig(f'Graphs/f_fija/{f}_8.png', dpi=300, bbox_inches='tight')
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