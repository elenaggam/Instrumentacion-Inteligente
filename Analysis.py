import numpy as np

def bandwidth_gain(freq, magn):

    #gain
    max_index = np.argmax(magn)
    max_magnitude = magn[max_index]

    #3db
    target = max_magnitude/np.sqrt(2)

    k=0
    for i in range(len(magn)):
        if magn[i]>=target:
            k=i
            break
    
    f_low = (target-magn[k-1])*(freq[k]-freq[k-1])/(magn[k]-magn[k-1])+freq[k-1]
    


    return f_low, max_magnitude


def stopband_attenuation(freq, magn):

    #gain
    magn2=20*np.log10(magn)
    max_magn=20*np.log10(np.max(magn))
    min_magn=max_magn-45

    k=0
    for i in range(len(magn)):
        if magn2[i]>=min_magn:
            k=i
            break

    f_stop = (min_magn-magn2[k-1])*(freq[k]-freq[k-1])/(magn2[k]-magn2[k-1])+freq[k-1]
    min_magn = 10**(min_magn/20)

    return f_stop, min_magn


def slope_dB_decade(freq, magn):
    f1 = freq[0]
    f2 = 0
    i=0
    for k in range(len(freq)):
        if freq[k] >= f1 * 10:
            f2 = freq[k]
            i=k
            break
    return (20*np.log10(magn[i])-20*np.log10(magn[0]))/(np.log10(freq[i])-np.log10(freq[0]))