import numpy as np
import pyvisa as pv
import serial, time

# Instrumento
resources=pv.ResourceManager()
resources.list_resources()
instrumento=resources.open_resource('USB0::0x0957::0x179B::MY51250756::INSTR')


# Parámetros
pasos1=30
pasos2=50
pasos = pasos1+pasos2
Vi=5
f1=100
fmid=10000
f2=6e5
freq=np.concatenate((np.logspace(np.log10(f1), np.log10(fmid), pasos1), np.logspace(np.log10(fmid), np.log10(f2), pasos2)))
avg=8

instrumento.timeout=5000


# Archivo de datos
file_tr=open(f'Wave_gen/tr_flog{f1:.0f}-{fmid:.0f}-{f2:.0f}_steps{pasos}_avg{avg}_Vref{Vi}.txt', 'w')
file_sq=open(f'Wave_gen/sq_flog{f1:.0f}-{fmid:.0f}-{f2:.0f}_steps{pasos}_avg{avg}_Vref{Vi}.txt', 'w')


# Generar señal
instrumento.write('wgen:outp 1')
instrumento.write(f'wgen:func sin;volt {Vi};freq {freq[0]};volt:offs 1')
instrumento.write('autoscale')


# instrumento.write(f'chan1:range {Vi*2.5}V')
# instrumento.write(f'chan2:offset {Vi}V')
# instrumento.write(f'chan1:offset {Vi}V')



# Promedios
if avg>1:
    instrumento.write('acq:type average')
    instrumento.write(f'acq:count {avg}')
else:
    instrumento.write('acq:type normal')

Vo=float(instrumento.query('meas:vpp? chan2'))











instrumento.close()
file_tr.close()
file_sq.close()