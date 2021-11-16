#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import simplertp
import secrets


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        invite_method = False
        bye_method = False
        ack_method = False
        not_allowed_method = False
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line = line.decode('utf-8')
            if line[0:7] == "INVITE ":
                invite_method = True
                origen = line.split(":")[1]
                origen = origen.split("@")[0]
            elif line[0:4] == "BYE ":
                bye_method = True
            elif line[0:4] == "ACK ":
                ack_method = True
            else:
                if not invite_method and not bye_method and ack_method:
                    not_allowed_method = True
            # Si no hay más líneas salimos del bucle infinito

            if not line:
                break
        if invite_method:
            message = "SIP/2.0 100 Trying\r\n\r\nSIP/2.0 180 Ringing\r\n\r\n"
            message_ok = "SIP/2.0 200 OK\r\n\r\n"
            description = "\r\n\r\nv=0\r\n" + "o=" + origen + " 127.0.0.1\r\n"\
                          + "s=mysesion\r\n" + "t=0\r\n" + "m=audio "\
                          + str(PORT) + " RTP\r\n\r\n"
            longitud = "Content-Length: "\
                       + str(len(bytes(message+message_ok+description,
                                       'utf-8')))
            self.wfile.write(bytes(message + longitud + description, 'utf-8'))
        elif bye_method:
            message_bye = "SIP/2.0 200 OK \r\n"
            self.wfile.write(bytes(message_bye, 'utf-8'))
        elif ack_method:
            self.wfile.write(b"Viene el RTP\r\n")
            BIT = secrets.randbelow(1)
            RTP_header = simplertp.RtpHeader()
            RTP_header.set_header(version=2, marker=BIT,
                                  payload_type=14, ssrc=200002)
            audio = simplertp.RtpPayloadMp3(AUDIO_FILE)
            ip = "127.0.0.1"
            port = 23032
            simplertp.send_rtp_packet(RTP_header, audio, ip, port)
        elif not_allowed_method:
            message_not_allowed_method = "SIP/2.0 405 Method Not Allowed\r\n"
            self.wfile.write(bytes(message_not_allowed_method, 'utf-8'))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 server.py IP  port audio_file")
        sys.exit()
    try:
        PORT = int(sys.argv[2])
        IP = sys.argv[1]
        AUDIO_FILE = sys.argv[3]
        # Creamos servidor de eco y escuchamos
        serv = socketserver.UDPServer((IP, PORT), EchoHandler)
        print("Listening...")
        serv.serve_forever()
    except ValueError:
        print("Usage: python3 server.py IP  port audio_file")
