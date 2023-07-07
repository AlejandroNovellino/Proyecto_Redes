import sys
import argparse
import time

# Imports for serial
import serial
import json
import pickle

# Imports for dominoes
import dominoes

# Test the ports
port_COM_A = serial.Serial(port="COM1", baudrate=115200, timeout=2, write_timeout=2)
port_COM_B = serial.Serial(port="COM2", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_C = serial.Serial(port="COM3", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_D = serial.Serial(port="COM4", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_E = serial.Serial(port="COM5", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_F = serial.Serial(port="COM6", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_G = serial.Serial(port="COM7", baudrate=115200, timeout=0.1, write_timeout=0.1)
port_COM_H = serial.Serial(port="COM8", baudrate=115200, timeout=0.1, write_timeout=0.1)

# Puerto A escribe al bus
port_COM_A.write("Hola desde el puerto A".encode("utf-8"))
time.sleep(0.15)
# Puerto B lee del bus
message = port_COM_B.readline()
print(f"Mensaje leido desde el puerto B: {message.decode('utf-8')}")

# Puerto C escribe al bus
port_COM_C.write("Hola desde el puerto C".encode("utf-8"))
time.sleep(0.15)
# Puerto D lee del bus
message = port_COM_D.readline()
print(f"Mensaje leido desde el puerto D: {message.decode('utf-8')}")

# Puerto E escribe al bus
port_COM_E.write("Hola desde el puerto E".encode("utf-8"))
time.sleep(0.15)
# Puerto F lee del bus
message = port_COM_F.readline()
print(f"Mensaje leido desde el puerto F: {message.decode('utf-8')}")

# Puerto G escribe al bus
port_COM_G.write("Hola desde el puerto G".encode("utf-8"))
time.sleep(0.15)
# Puerto H lee del bus
message = port_COM_H.readline()
print(f"Mensaje leido desde el puerto H: {message.decode('utf-8')}")

# Clear all the ports
port_COM_A.reset_input_buffer()
port_COM_A.reset_output_buffer()


port_COM_B.reset_input_buffer()
port_COM_B.reset_output_buffer()

port_COM_C.reset_input_buffer()
port_COM_C.reset_output_buffer()

port_COM_D.reset_input_buffer()
port_COM_D.reset_output_buffer()

port_COM_E.reset_input_buffer()
port_COM_E.reset_output_buffer()

port_COM_F.reset_input_buffer()
port_COM_F.reset_output_buffer()

port_COM_G.reset_input_buffer()
port_COM_G.reset_output_buffer()

port_COM_H.reset_input_buffer()
port_COM_H.reset_output_buffer()

# Close all the ports
port_COM_A.close()
port_COM_B.close()
port_COM_C.close()
port_COM_D.close()
port_COM_E.close()
port_COM_F.close()
port_COM_G.close()
port_COM_H.close()
