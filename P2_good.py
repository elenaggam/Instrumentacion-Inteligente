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

R1 = [255-i for i in range(256)]


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
file=open(f'Wave_gen/avg{avg}_Vcc{Vcc}.txt', 'w')



instrumento.write('autoscale')
# instrumento.write(f'chan1:range {Vi*2.5}V')
# instrumento.write('chan2:offset 0')
# instrumento.write('chan1:offset 0')


# barrido en R1 (int) -> barrido en frecuencia
for i in R1:
    set_pot(0, i)
    time.sleep(0.1)  # esperar a que el pot se estabilice

    # V_tr=float(instrumento.query('meas:vpp? chan1'))
    # V_sq=float(instrumento.query('meas:vpp? chan2'))
    # freq_tr=float(instrumento.query('meas:freq? chan1'))
    # freq_sq=float(instrumento.query('meas:freq? chan2'))
    # DC_tr=float(instrumento.query('meas:volt:dc? chan1'))
    # DC_sq=float(instrumento.query('meas:volt:dc? chan2'))
    # phas=float(instrumento.query('meas:phase? chan1,chan2'))

    # file.write(f"{i}\t{freq_tr:.2f}\t{V_tr:.4f}\t{DC_tr:.4f}\t{freq_sq:.2f}\t{V_sq:.4f}\t{DC_sq:.4f}\t{phas:.2f}\n")
    # print(f"R1={i*50/255}, freq_tr={freq_tr:.2f} Hz, Vtr={V_tr:.4f} V, freq_sq={freq_sq:.2f} Hz, Vsq={V_sq:.4f} V")

instrumento.close()
file.close()
arduino.close()