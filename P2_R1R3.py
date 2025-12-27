import numpy as np
import pyvisa as pv
import serial, time


def set_pot(pot, value):
    """
    pot : 0 o 1
    value : 0-255
    """
    cmd = f"POT {pot} {value}\n"
    arduino.write(cmd.encode())

    # opcional: esperar "OK"
    resp = arduino.readline().decode().strip()
    print("Arduino:", resp)

R1 = [255-i for i in range(15)]


arduino=serial.Serial('COM6', 9600) #change COM port accordingly
time.sleep(2)  #wait for the serial connection to initialize


# Instrumento
resources=pv.ResourceManager()
resources.list_resources()
instrumento=resources.open_resource('USB0::0x0957::0x179B::MY51250756::INSTR')


# Parámetros
Vcc=10
avg=8
instrumento.timeout=5000

# Promedios
if avg>1:
    instrumento.write('acq:type average')
    instrumento.write(f'acq:count {avg}')
else:
    instrumento.write('acq:type normal')

# Archivo de datos
file=open(f'Waaatry', 'w')



instrumento.write('autoscale')
# instrumento.write(f'chan1:range {Vi*2.5}V')
# instrumento.write('chan2:offset 0')
# instrumento.write('chan1:offset 0')


# barrido en R1 (int) -> barrido en frecuencia

file.write("R1\t\tFreq_tr(Hz)\t\tV_tr(V)\t\tDC_tr(V)\t\tFreq_sq(Hz)\t\tV_sq(V)\t\tDC_sq(V)\t\tPhase(deg)\tt\trise_tr(s)\t\tfall_tr(s)\t\trise_sq(s)\t\tfall_sq(s)\n")

def mis_medidas():
    V_tr=float(instrumento.query('meas:vpp? chan1'))
    V_sq=float(instrumento.query('meas:vpp? chan2'))
    freq_tr=float(instrumento.query('meas:freq? chan1'))
    freq_sq=float(instrumento.query('meas:freq? chan2'))
    DC_tr=float(instrumento.query('meas:vav? chan1'))
    DC_sq=float(instrumento.query('meas:vav? chan2'))
    phas=float(instrumento.query('meas:phase? chan1,chan2'))
    t_up_tr=float(instrumento.query('meas:ris? chan1'))
    t_down_tr=float(instrumento.query('meas:fall? chan1'))
    t_up_sq=float(instrumento.query('meas:ris? chan2'))
    t_down_sq=float(instrumento.query('meas:fall? chan2'))
    
    return V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq


set_pot(0, 255)
time.sleep(0.1)  # esperar a que el pot se estabilice
V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq = mis_medidas()
instrumento.write(f'chan2:range {V_sq*1.5}V')  
instrumento.write(f'chan1:range {V_tr*1.5}V')
instrumento.write(f'chan1:offset {DC_tr}')
instrumento.write(f'chan2:offset {DC_sq}')

for i in R1:
    instrumento.write(f'tim:range {5/freq_tr}')
    set_pot(0, i)
    time.sleep(0.1)  # esperar a que el pot se estabilice
    V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq = mis_medidas() 
    file.write(f"{i}\t\t{freq_tr:.2f}\t\t{V_tr:.4f}\t\t{DC_tr:.4f}\t\t{freq_sq:.2f}\t\t{V_sq:.4f}\t\t{DC_sq:.4f}\t\t{phas:.2f}\t\t{t_up_tr:.6f}\t\t{t_down_tr:.6f}\t\t{t_up_sq:.6f}\t\t{t_down_sq:.6f}\n")




instrumento.close()
file.close()
arduino.close()