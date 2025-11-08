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

    plt.tight_layout()

    if directory is not None:
        plt.savefig(directory+'Bode_Magnitud.png')
    if show:
        plt.show(block=False)

    return

def bode_phase(freq, phase, deltaTicks=45, directory=None, show=True, f_low=None, f_cut=None):

    phase = np.asarray(phase, dtype=float)
    phase = np.where(phase > 180, phase - 360, phase)
    phase = np.where(phase < -180, phase + 360, phase)
    plt.figure()
    # plt.title('Diagrama de Bode - Fase')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    plt.ylim(top=180)
    ax = plt.gca()
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    plt.tick_params(axis='both', which='major', labelsize=12)
    ymin = np.min(phase)
    ymax = np.max(phase)
    yt_min = np.floor(ymin / deltaTicks) * deltaTicks
    yt_max = np.ceil(ymax / deltaTicks) * deltaTicks
    yticks = np.arange(yt_min, yt_max + 1e-6, deltaTicks)
    ax.set_yticks(yticks)
    plt.grid(zorder=-1)
    plt.plot(freq, phase, marker='o', linestyle='-')
    plt.xscale('log')
    if f_low is not None:
        plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    if f_cut is not None:
        plt.axvline(f_cut, color='black', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    # plt.legend()

    plt.tight_layout()
    
    if directory is not None:
        plt.savefig(directory+'Bode_Fase.png')
    if show:
        plt.show(block=False)

    return


#añadir pendientes, bw, etc



def bode_diagrams(freq, magn, phase, freq2=None,magn2=None, phase2=None, label1=None, label2=None, directory=None, show=True, deltaTicks=90, infLim=None, f_low=None, max_magn=None, f_cut=None, min_magn=None):
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))

    plt.sca(ax1)

    ax = plt.gca()
    ax.yaxis.label.set_size(12)
    plt.ylabel('Magnitud (dB)', labelpad=10)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.xscale('log')
    plt.grid(zorder=-1)
    
    log_magn=20*np.log10(magn)
    plt.plot(freq, log_magn, marker='o', linestyle='-')
    if magn2 is not None:
        log_magn2=20*np.log10(magn2)
        plt.plot(freq2, log_magn2, marker='o', markersize=3)

    if f_low is not None:
        plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    if max_magn is not None:
        log_max_magn=20*np.log10(max_magn)
        plt.axhline(log_max_magn - 3, color='red', linestyle='--', label=f'{log_max_magn - 3:.2f} dB')
    if f_cut is not None:
        plt.axvline(f_cut, color='black', linestyle='--', label=f'fc={f_cut:.2f} Hz')
    if min_magn is not None:
        log_min_magn=20*np.log10(min_magn)
        plt.axhline(log_min_magn, color='black', linestyle='--', label=f'{min_magn:.2f} dB')

    plt.tight_layout()

    if show:
        plt.show(block=False)


    plt.sca(ax2)

    ax = plt.gca()
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase ($^\\circ$)')
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.xscale('log')
    plt.grid(zorder=-1)
    ymin = np.min(phase)
    ymax = np.max(phase)
    yt_min = np.floor(ymin / deltaTicks) * deltaTicks
    yt_max = np.ceil(ymax / deltaTicks) * deltaTicks
    yticks = np.arange(yt_min, yt_max + 1e-6, deltaTicks)
    ax.set_yticks(yticks)
    plt.ylim(top=180)
    if infLim is not None:
        plt.ylim(bottom=infLim)
    
    phase = np.asarray(phase, dtype=float)
    phase = np.where(phase > 180, phase - 360, phase)
    phase = np.where(phase < -180, phase + 360, phase)
    plt.plot(freq, phase, marker='o', linestyle='-')
    if phase2 is not None:
        phase2 = np.asarray(phase2, dtype=float)
        phase2 = np.where(phase2 > 180, phase2 - 360, phase2)
        phase2 = np.where(phase2 < -180, phase2 + 360, phase2)
        plt.plot(freq2, phase2, marker='o', markersize=3)

    if f_low is not None:
        plt.axvline(f_low, color='red', linestyle='--', label=f'fc={f_low:.2f} Hz')
    if f_cut is not None:
        plt.axvline(f_cut, color='black', linestyle='--', label=f'fc={f_cut:.2f} Hz')

    if label1 is not None and label2 is not None:
        plt.legend([label1, label2], fontsize=12)

    plt.tight_layout()
    
    if show:
        plt.show(block=False)

    if directory is not None:
        plt.savefig(directory+'.png')

    return