import numpy as np
import pyvisa as pv
import time as t
import matplotlib.pyplot as plt
import Plotting as P

pasos=30
medida=np.zeros(pasos)
freq=np.logspace(np.log10(100), np.log10(1e7), pasos)

resources=pv.ResourceManager()
resources.list_resources()

# USB0::0x0957::0x179B::MY51250756::INSTR
instrument=resources.open_resource('visa://155.210.95.128/USB0::0x0957::0x179B::MY51250757::INSTR')

#no poner espacio tras :::::::
instrument.write('wgen:outp 1')
instrument.write('wgen:func sin;volt 1;freq 1000;volt:offs 0')

phase = np.zeros(pasos)
for i in range (pasos):
    instrument.write(f'wgen:freq {freq[i]}')
    instrument.write('autoscale')
    instrument.write('chan2:offset 0')
    instrument.write('chan1:offset 0')
    #t.sleep(0.1)
    medida[i]=float(instrument.query('meas:vpp? chan2'))
    phase[i]=float(instrument.query('meas:phas? chan1, chan2'))
    #t.sleep(0.1)
    #print(f'Frecuencia: {freq[i]:.2f} Hz - Vpp: {medida[i]:.3f} V')


instrument.close()

P.bode_magnitude(freq, medida, directory=None, show=True)
P.bode_phase(freq, phase, directory=None, show=True)

