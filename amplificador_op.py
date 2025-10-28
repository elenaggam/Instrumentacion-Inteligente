import numpy as np
import pyvisa as pv
import time as t
import matplotlib.pyplot as plt

pasos=20
medida=np.zeros(pasos)
freq=np.logspace(np.log10(100), np.log10(1e7), pasos)

resources=pv.ResourceManager()
resources.list_resources()

# USB0::0x0957::0x179B::MY51250756::INSTR
instrument=resources.open_resource('visa://155.210.95.128/USB0::0x0957::0x179B::MY51250757::INSTR')

#no poner espacio tras :::::::
instrument.write('wgen:outp 1')
instrument.write('wgen:func sin;volt 1;freq 1000;volt:offs 0')


for i in range (pasos):
    instrument.write(f'wgen:freq {freq[i]}')
    instrument.write('autoscale')
    t.sleep(0.1)
    medida[i]=float(instrument.query('meas:vpp? chan2'))
    #t.sleep(0.1)
    #print(f'Frecuencia: {freq[i]:.2f} Hz - Vpp: {medida[i]:.3f} V')


instrument.close()

freq=20*np.log(freq)
medida=20*np.log(medida)
plt.grid()
plt.scatter(freq, medida)
# plt.xscale('log')
# plt.yscale('log')

first_height = float(medida[0])
y_val = -3+first_height
if y_val <= 0:
    y_val = np.finfo(float).tiny  # garantizar valor > 0 para escala log
plt.axhline(y=y_val, color='red', linestyle='--', linewidth=1)

plt.show()

input("Pulsa una tecla para finalizar")