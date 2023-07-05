# Test the ports

# Write to the port
test_dict = {"info": "Test information", "player": "Hello"}
print(f"Valor del diccionario: {json.dumps(test_dict)}")

# THIS IS HOW WE ARE WORKING
# port_COM.write(json.dumps(test_dict).encode("ascii"))
port_COM.write("Hola desde el puerto A".encode("utf-8"))
message = port_COM.readline()
print(f"Mensaje leido en el puerto B: {message.decode('utf-8')}")

port_COM.write("Hola desde el puerto B".encode("utf-8"))
message = port_COM.readline()
print(f"Mensaje leido en el puerto A: {message.decode('utf-8')}")
