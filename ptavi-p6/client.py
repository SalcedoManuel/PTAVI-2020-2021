#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
Autor: Manuel Salcedo Alonso
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = 'localhost'
PORT = int(sys.argv[2].split(":")[-1])
METHOD = sys.argv[1]
# Contenido que vamos a enviar
MESSAGE = sys.argv[2].split(":")[-2]
USER = sys.argv[2].split('@')[-2]
IP = (MESSAGE.split("@")[-1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    if METHOD == "INVITE":
        # Enviamos el INVITE
        message_invite = METHOD + " sip:" + MESSAGE + " SIP/2.0\r\n"
        my_socket.send(bytes(message_invite, 'utf-8'))
        # Esperamos a recibir la respuesta del Servidor.
        data = my_socket.recv(1024)
        # Enviamos el ACK al Servidor
        message_ack = "ACK sip:" + MESSAGE + " SIP/2.0\r\n"
        my_socket.send(bytes(message_ack, 'utf-8'))
        # Esperamos a recibir el archivo de audio
        data = my_socket.recv(1024)
    elif METHOD == "BYE":
        # Enviamos el BYE
        message_bye = METHOD + " sip:" + MESSAGE + " SIP/2.0\r\n"
        my_socket.send(bytes(message_bye, 'utf-8'))
        # Esperamos a recibir el 200 OK
        data = my_socket.recv(1024)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 client.py method receiver@IP:SIPport")
