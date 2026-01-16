import numpy as np
import pyvisa as pv


# Instrumento
resources=pv.ResourceManager()
resources.list_resources()
instrumento=resources.open_resource('visa://155.210.95.128/USB0::0x0957::0x179B::MY51250757::INSTR')


# Parámetros
pasos1=50
pasos2=20
pasos = pasos1+pasos2
Vi=1
f1=1000
fmid=40000
f2=5e5
freq=np.concatenate((np.logspace(np.log10(f1), np.log10(fmid), pasos1), np.logspace(np.log10(fmid), np.log10(f2), pasos2)))
avg=8

instrumento.timeout=5000


# Archivo de datos
file=open(f'Bode/DEF_flog{f1:.0f}-{fmid:.0f}-{f2:.0f}_steps{pasos}_avg{avg}_Vin{Vi}.txt', 'w')


# Generar señal
instrumento.write('wgen:outp 1')
instrumento.write(f'wgen:func sin;volt {Vi};freq {freq[0]};volt:offs 0')
instrumento.write('autoscale')
instrumento.write(f'chan1:range {Vi*2.5}V')
instrumento.write('chan2:offset 0')
instrumento.write('chan1:offset 0')


# Promedios
if avg>1:
    instrumento.write('acq:type average')
    instrumento.write(f'acq:count {avg}')
else:
    instrumento.write('acq:type normal')

Vo=float(instrumento.query('meas:vpp? chan2'))


# Barrido en frecuencia
for i in range(pasos):
    instrumento.write(f'wgen:freq {freq[i]}')

    # Escalas
    instrumento.write(f'chan2:range {Vo*3}V')    
    instrumento.write(f'tim:range {5/freq[i]}')

    # Medidas 
    Vo=float(instrumento.query('meas:vpp? chan2'))
    fase=float(instrumento.query('meas:phas? chan2, chan1'))
    Vi=float(instrumento.query('meas:vpp? chan1'))

    # Guardar datos
    file.write(f'{freq[i]:.3f}\t{Vi:.3f}\t{Vo:.3f}\t{fase:.1f}\n')


instrumento.close()
file.close()
