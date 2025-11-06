import numpy as np
import matplotlib.pyplot as plt
import Analysis

#diagramas bode: respuesta en frecuencia
def bode_magnitude(freq, magn, directory=None, show=True, f_low=None, max_magn=None, f_cut=None, min_magn=None):
    log_magn=20*np.log10(magn)

    if max_magn is not None:
        log_max_magn=20*np.log10(max_magn)
    if min_magn is not None:
        log_min_magn=20*np.log10(min_magn)

    plt.figure()
    # plt.title('Diagrama de Bode - Magnitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    ax = plt.gca()
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    plt.tick_params(axis='both', which='major', labelsize=12)

    plt.grid(zorder=-1)
    plt.plot(freq, log_magn, marker='o', linestyle='-')

    if f_low is not None:
        plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    if max_magn is not None:
        plt.axhline(log_max_magn - 3, color='red', linestyle='--', label=f'{log_max_magn - 3:.2f} dB')
    if f_cut is not None:
        plt.axvline(f_cut, color='black', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    if min_magn is not None:
        plt.axhline(log_min_magn, color='black', linestyle='--', label=f'{min_magn:.2f} dB')
    # plt.legend()
    plt.xscale('log')

    x=np.log(np.logspace(np.log10(min(freq)), np.log10(1e4), 100))
    #plt.plot(x, 20*x)

    if directory is not None:
        plt.savefig(directory+'Bode_Magnitud.png')
    if show:
        plt.show()

    return

def bode_phase(freq, phase, directory=None, show=True, f_low=None, f_cut=None):

    plt.figure()
    # plt.title('Diagrama de Bode - Fase')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    ax = plt.gca()
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(zorder=-1)
    plt.plot(freq, phase, marker='o', linestyle='-')
    plt.xscale('log')
    if f_low is not None:
        plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    # if f_cut is not None:
    #     plt.axvline(f_cut, color='black', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    # plt.legend()

    if directory is not None:
        plt.savefig(directory+'Bode_Fase.png')
    if show:
        plt.show()

    return

def bode_plots(freq, magn, phase, directory=None, show=True, f_low=None, max_magn=None, f_cut=None, min_magn=None):
    bode_magnitude(freq, magn, directory, show=False, f_low=f_low, max_magn=max_magn, f_cut=f_cut, min_magn=min_magn)
    bode_phase(freq, phase, directory, show, f_low=f_low, f_cut=f_cut)

    return


#añadir pendientes, bw, etc