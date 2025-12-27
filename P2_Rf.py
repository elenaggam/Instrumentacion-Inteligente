import numpy as np
import pyvisa as pv
import serial, time


def set_pot(value1, value2):
   
    cmd = f"{value1},{value2}\n"
    arduino.write(cmd.encode())

    # opcional: esperar "OK"
    resp = arduino.readline().decode().strip()
    print("Arduino:", resp)



dirk = 'Wave_gen/Rf/k_fija/'
dirf = 'Wave_gen/Rf/f_fija/'

c = 9.290e-9  # in Farads
R2 = 98500
Rf_s= 32800
R3_s= 67800
pot = 0

# Usuario
f = [1000,2000] # in hz
k = [10.]  # constante de proporcionalidad square vs triangle

Rf = [255-i for i in np.arange(0, 256, 5)] 
R3 = [int(255-i) for i in np.arange(0, 256, 5)]

# Cálculos para el potenciómetro kOhms to int
# for i in f:
#     for j in k:
#         Rf.append(int(255*(j/(4*i*c)-Rf_s)/42000)) 
#         R3.append(int(255*(j*R2-R3_s)/42000))


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
file=open(f'Wave_gen/Rf/avg{avg}_Vcc{Vcc}.txt', 'w')


instrumento.write('autoscale')



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
    top_tr=float(instrumento.query('meas:vtop? chan1'))
    base_tr=float(instrumento.query('meas:vbas? chan1'))
    top_sq=float(instrumento.query('meas:vtop? chan2'))
    base_sq=float(instrumento.query('meas:vbas? chan2'))
    
    return V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq


set_pot(55, 127)
time.sleep(0.1)  # esperar a que el pot se estabilice
V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = mis_medidas()
instrumento.write(f'chan2:range {V_sq*1.5}V')  
instrumento.write(f'chan1:range {V_tr*1.5}V')
instrumento.write(f'chan1:offset {DC_tr}')
instrumento.write(f'chan2:offset {DC_sq}')
instrumento.write(f'tim:range {5/freq_tr}')



# for j in R3:
#     file=open(dirk+f'{j}_avg{avg}_Vcc{Vcc}.txt', 'w')
#     file.write("Rf\t\tFreq_tr(Hz)\t\tV_tr(V)\t\tDC_tr(V)\t\tFreq_sq(Hz)\t\tV_sq(V)\t\tDC_sq(V)\t\tPhase(deg)\t\tt_rise_tr(s)\t\tt_fall_tr(s)\t\tt_rise_sq(s)\t\tt_fall_sq(s)\ttop_tr(V)\tbase_tr(V)\ttop_sq(V)\tbase_sq(V)\n")
#     start = time.time()
#     for i in Rf:
#         instrumento.write(f'tim:range {5/freq_tr}')
#         set_pot(i, j)
#         time.sleep(0.02)  # esperar a que el pot se estabilice
#         V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = mis_medidas() 
#         file.write(f"{i}\t\t{freq_tr:.2f}\t\t{V_tr:.4f}\t\t{DC_tr:.4f}\t\t{freq_sq:.2f}\t\t{V_sq:.4f}\t\t{DC_sq:.4f}\t\t{phas:.2f}\t\t{t_up_tr:.6f}\t\t{t_down_tr:.6f}\t\t{t_up_sq:.6f}\t\t{t_down_sq:.6f}\t\t{top_tr:.4f}\t\t{base_tr:.4f}\t\t{top_sq:.4f}\t\t{base_sq:.4f}\n")
#     print(f"\nR3={j} done in {time.time()-start:.2f} seconds\n")
#     file.close()


# frecs = np.arange(330, 1100, 20)  # in hz
# for f in frecs:
#     file=open(dirf+f'{f:.2f}_avg{avg}_Vcc{Vcc}.txt', 'w')
#     file.write("Rf\t\tR3\t\tFreq_tr(Hz)\t\tV_tr(V)\t\tDC_tr(V)\t\tFreq_sq(Hz)\t\tV_sq(V)\t\tDC_sq(V)\t\tPhase(deg)\t\tt_rise_tr(s)\t\tt_fall_tr(s)\t\tt_rise_sq(s)\t\tt_fall_sq(s)\ttop_tr(V)\tbase_tr(V)\ttop_sq(V)\tbase_sq(V)\n")
#     start = time.time()

#     prod = R2/(4*c*f) #(Rf*R3)
    
#     for j in R3: #R3 de 0 a 255
#         Rf = prod/(R3_s + (42000*j/255)) - Rf_s
#         Rf_int = int(255*Rf/42000)

#         if Rf_int < 0 or Rf_int > 255:
#             continue

#         instrumento.write(f'tim:range {5/freq_tr}')
#         set_pot(Rf_int, j)
#         time.sleep(0.02)  # esperar a que el pot se estabilice
#         V_tr, V_sq, freq_tr, freq_sq, DC_tr, DC_sq, phas, t_up_tr, t_down_tr, t_up_sq, t_down_sq, top_tr, base_tr, top_sq, base_sq = mis_medidas() 
#         file.write(f"{Rf_int}\t\t{j}\t\t{freq_tr:.2f}\t\t{V_tr:.4f}\t\t{DC_tr:.4f}\t\t{freq_sq:.2f}\t\t{V_sq:.4f}\t\t{DC_sq:.4f}\t\t{phas:.2f}\t\t{t_up_tr:.6f}\t\t{t_down_tr:.6f}\t\t{t_up_sq:.6f}\t\t{t_down_sq:.6f}\t\t{top_tr:.4f}\t\t{base_tr:.4f}\t\t{top_sq:.4f}\t\t{base_sq:.4f}\n")
    
#     print(f"\nf={f:.2f}Hz done in {time.time()-start:.2f} seconds\n")


#     file.close()





instrumento.close()
arduino.close()