#!/usr/bin/python3
"""
Programa cliente UDP que abre un socket a un servidor
Autor: Manuel Salcedo
"""

import socket
import sys

# Constantes y variables a usar
SERVER = sys.argv[1]        # CONSTANTE de la IP
PORT = int(sys.argv[2])     # CONSTANTE del Puerto
REGISTER_SIP = sys.argv[4]  # CONSTATE de REGISTRO
EXPIRES = sys.argv[5]       # CONSTANTE de Expiración


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))  # Conectamos con el Servidor
    # Enviamos la secuencia de bytes por el socket
    my_socket.send(bytes("REGISTER sip: " + REGISTER_SIP + " SIP/2.0\r\n" +
                         "Expires: " + sys.argv[5] + "\r\n\r\n", 'utf-8'))
    # Leemos del socket. Buffer = 1024
    data = my_socket.recv(1024)
    # Imprimimos lo recibido.
    print(data.decode('utf-8'))
    # Salimos del programa.

if __name__ == "__main__":

    try:
        if len(sys.argv) != 6:
            print("Usage: client.py ip puerto register" +
                  " sip_address expires_value")
            sys.exit()

    except IndexError:
        sys.exit()
