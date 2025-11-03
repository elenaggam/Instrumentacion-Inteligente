import numpy as np
import matplotlib.pyplot as plt
import Analysis

#diagramas bode: respuesta en frecuencia
def bode_magnitude(freq, magn, directory=None, show=True):
    log_magn=20*np.log10(magn)

    plt.figure()
    plt.title('Diagrama de Bode - Magnitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(zorder=-1)
    plt.plot(freq, log_magn, marker='o', linestyle='-')
    plt.xscale('log')

    x=np.log(np.logspace(np.log10(min(freq)), np.log10(1e4), 100))
    #plt.plot(x, 20*x)

    if directory is not None:
        plt.savefig(directory+'Bode_Magnitud.png')
    if show:
        plt.show()

    return

def bode_phase(freq, phase, directory=None, show=True):

    plt.figure()
    plt.title('Diagrama de Bode - Fase')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    plt.grid(zorder=-1)
    plt.plot(freq, phase, marker='o', linestyle='-')
    plt.xscale('log')

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