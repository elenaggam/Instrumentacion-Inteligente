import numpy as np

def bandwidth(frequency, magnitude):

    # identificamos la mayor ganancia (magnitud)
    max_index = np.argmax(magnitude)
    max_magnitude = magnitude[max_index]

    # calculamos el valor objetivo a -3 dB
    target = max_magnitude/np.sqrt(2)

    # puntos donde la magnitud es la máxima o mayor que el objetivo
    indices = np.where(magnitude >= target)
    #ver si queremos interpolar o algo más sofisticado
    f_low = frequency[indices[0]]
    f_high = frequency[indices[-1]]

    bandwidth = f_high - f_low
    return bandwidth


    