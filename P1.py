import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv




# Instrumento
resources=pv.ResourceManager()
resources.list_resources()
instrumento=resources.open_resource('visa://155.210.95.128/USB0::0x0957::0x179B::MY51250757::INSTR')


# Parámetros de la medición
pasos = 10




# Generar señal
instrumento.write('wgen:outp 1')
instrumento.write('wgen:func sin;volt 1;freq 1000;volt:offs 0')
    # instrumento.write(f'wgen:freq {freq[i]}')
    # instrumento.write(f'wgen:volt {volt[i]}')



# Escalar ejes, ciclos, promedios ... 
instrumento.write('autoscale')
instrumento.write('chan1:scale 0.5')
instrumento.write('chan1:offset 0')
instrumento.write('tim:range 0.001')
instrumento.write('chan2:scale 0.5')
instrumento.write('chan2:offset 0')



# Medidas
medida1=float(instrumento.query('meas:vpp? chan2'))
medida2=float(instrumento.query('meas:freq? chan2'))
medida3=float(instrumento.query('meas:phas? chan1, chan2'))


#ficherooos