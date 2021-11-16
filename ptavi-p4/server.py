#!/usr/bin/python3
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json
import os.path as path

dicc = {}


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """handle method of the server class"""
        # Enviamos al cliente el mensaje de confirmación
        self.wfile.write(b"SIP/2.0 200 OK")
        # Bucle
        for line in self.rfile:
            # Sacamos la linea del mensaje recibido
            line = line.decode('utf-8')
            # Si la etiqueta es REGISTER
            if line[0:8] == "REGISTER":
                # Obtenemos el usuario
                username = line.split(" ")[-2]
            # Si la etiqueta es EXPIRES
            elif line[0:8] == "Expires:":
                # Obtenemos el valor de expire
                expire = int(line.split()[-1])
                if expire > 0:  # Añadimos el nuevo cliente.
                    expires_time = time.time() + expire
                    expires_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.gmtime(expires_time))
                    # Añadimos el usuario en la lista.
                    user_list[username] = [self.client_address[0],
                                           expires_time]
                    # Comprobamos si hay fichero y registramos en el fichero
                    self.json2register()

                else:  # Borrar cliente. Expire = 0
                    del user_list[username]
                # Guardamos en el fichero la lista.
                self.register2json()

    def register2json(self):
        """Registramos los valores """
        # Escribimos el diccionario en el fichero .json
        with open("registered.json", "w") as outfile:
            json.dump(user_list, outfile, indent=1)

    def json2register(self):
        """register dictionary"""
        username = ""
        try:
            if path.exits("registered.json"):
                with open("registered.json", "r") as data_file:
                    user_list[username] = json.load(data_file)
        except Exception:
            pass


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    # La lista de usuarios
    user_list = {}

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
