import numpy as np
import matplotlib.pyplot as plt
import Analysis

#diagramas bode: respuesta en frecuencia
def bode_magnitude(freq, magn, directory=None, show=True):
    log_magn=20*np.log10(magn)
    log_freq=np.log10(freq)

    plt.figure()
    plt.title('Diagrama de Bode - Magnitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(zorder=-1)
    plt.plot(log_freq, log_magn)

    if directory is not None:
        plt.savefig(directory+'Bode_Magnitud.png')
    if show:
        plt.show()

    return

def bode_phase(freq, phase, directory=None, show=True):
    log_freq=np.log10(freq)

    plt.figure()
    plt.title('Diagrama de Bode - Fase')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    plt.grid(zorder=-1)
    plt.plot(log_freq, phase)

    if directory is not None:
        plt.savefig(directory+'Bode_Fase.png')
    if show:
        plt.show()

    return

def bode_plots(freq, magn, phase, directory=None, show=True):
    bode_magnitude(freq, magn, directory, show=False)
    bode_phase(freq, phase, directory, show)

    return


#añadir pendientes, bw, etc