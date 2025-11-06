import numpy as np
import matplotlib.pyplot as plt
import Analysis

#diagramas bode: respuesta en frecuencia
def bode_magnitude(freq, magn, directory=None, show=True, f_low=None, max_magn=None, f_cut=None, min_magn=None):
    log_magn=20*np.log10(magn)
    log_max_magn=20*np.log10(max_magn)

    plt.figure()
    plt.title('Diagrama de Bode - Magnitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(zorder=-1)
    plt.plot(freq, log_magn, marker='o', linestyle='-')

    plt.axvline(f_low, color='green', linestyle='--', label=f'fc={f_low:.2f} Hz')
    plt.axhline(log_max_magn - 3, color='green', linestyle='--', label=f'{log_max_magn - 3:.2f} dB')
    plt.axvline(f_cut, color='red', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    plt.axhline(min_magn, color='red', linestyle='--', label=f'{min_magn:.2f} dB')
    plt.legend()
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
    plt.title('Diagrama de Bode - Fase')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    plt.grid(zorder=-1)
    plt.plot(freq, phase, marker='o', linestyle='-')
    plt.xscale('log')
    plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    plt.axvline(f_cut, color='green', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    plt.legend()

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