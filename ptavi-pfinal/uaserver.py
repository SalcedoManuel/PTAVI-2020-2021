#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import socket
import sys
import simplertp
import secrets
import random
from xml.sax import make_parser
from uaclient import write_log, XMLHandler

ip_rtp_destination = ""
port_rtp_destination = 5555
rtp_destination = {}


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):

        while 1:

            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line = line.decode('utf-8')
            information = line.split('\r\n')
            try:
                pass
            except UnicodeDecodeError:
                break
            if line:
                if line[0:6] == "INVITE":
                    ip_rtp_destination = information[5].split()[-1]
                    port_rtp_destination = int(information[8].split()[-2])
                    rtp_destination[1] = [ip_rtp_destination,
                                          port_rtp_destination]
                    write_log(line, "Received from:",
                              ip_rtp_destination, port_rtp_destination,
                              log_path)
                    headboard = "SIP/2.0 100 Trying\r\nSIP/2.0 180 Ringing"\
                                + "\r\nSIP/2.0 200 OK\r\n"\
                                + "Content-Type: application/sdp\r\n"\
                                + "Content-Length: "
                    description = "\r\n\r\nv=0\r\no=" + username + " "\
                                  + ip_uaserver + "\r\n"\
                                  + "s=misesion\r\nt=0\r\nm=audio "\
                                  + str(port_uaserver) + " RTP\r\n"
                    length = str(len(bytes(headboard + description,
                                           'utf-8')))

                    message = headboard + length + description
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
                            as my_socket:
                        my_socket.setsockopt(socket.SOL_SOCKET,
                                             socket.SO_REUSEADDR, 1)
                        my_socket.connect((server_proxy_ip,
                                           server_proxy_port))
                        my_socket.send(bytes(message, 'utf-8'))
                        write_log(message, "Sent to", ip_uaserver,
                                  port_uaserver, log_path)

                if line[0:3] == "ACK":

                    ip_rtp_destination = rtp_destination[1][0]
                    port_rtp_destination = rtp_destination[1][1]

                    BIT = secrets.randbelow(1)
                    ALEAT = random.randint(1, 15)
                    j = 0
                    csrc = []
                    while j < ALEAT:
                        rand = random.randint(0, 99999)
                        csrc.append(rand)
                        j += 1
                    RTP_header = simplertp.RtpHeader()
                    RTP_header.set_header(version=2, marker=BIT,
                                          payload_type=14, cc=ALEAT)
                    RTP_header.setCSRC(csrc)
                    audio = simplertp.RtpPayloadMp3(audio_path.split('\n')[0])
                    simplertp.send_rtp_packet(RTP_header, audio,
                                              ip_rtp_destination,
                                              port_rtp_destination)

                if line[0:7] == "SIP/2.0" and len(information) == 12:
                    rtp_client_ip = information[7].split()[-1]
                    rtp_client_port = int(information[10].split()[-2])
                    receptor = information[7].split()[-2]
                    receptor = receptor[2:]
                    ack_message = "ACK sip:" + receptor + " SIP/2.0\r\n"
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
                            as my_socket:
                        my_socket.setsockopt(socket.SOL_SOCKET,
                                             socket.SO_REUSEADDR, 1)
                        my_socket.connect((server_proxy_ip,
                                           server_proxy_port))
                        my_socket.send(bytes(ack_message,
                                             'utf-8'))

                    BIT = secrets.randbits(1)
                    ALEAT = random.randint(1, 15)
                    j = 0
                    csrc = []
                    while j < ALEAT:
                        rand = random.randint(0, 99999)
                        csrc.append(rand)
                        j += 1
                    RTP_header = simplertp.RtpHeader()
                    RTP_header.set_header(version=2, marker=BIT,
                                          payload_type=14, cc=ALEAT)
                    RTP_header.setCSRC(csrc)
                    audio = simplertp.RtpPayloadMp3(audio_path.split('\n')[0])
                    simplertp.send_rtp_packet(RTP_header, audio,
                                              rtp_client_ip, rtp_client_port)
                if line[0:3] == "BYE":
                    message = "SIP/2.0 200 OK"
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\
                            as my_socket:
                        my_socket.setsockopt(socket.SOL_SOCKET,
                                             socket.SO_REUSEADDR, 1)
                        my_socket.connect((server_proxy_ip,
                                           server_proxy_port))
                        my_socket.send(bytes(message,
                                             'utf-8'))
                        write_log(message, "Sent to", ip_uaserver,
                                  port_uaserver, log_path)

            else:
                break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 uaserver.py config")
        sys.exit()
    else:
        XML_FILE = str(sys.argv[1])
        parser = make_parser()
        XMLClass = XMLHandler()
        parser.setContentHandler(XMLClass)
        parser.parse(open(XML_FILE))
        attributes = XMLClass.get_tags()
        # ACCOUNT
        att = attributes[0]
        username = att["username"]
        passwd = att["passwd"]
        # UASERVER
        att = attributes[1]
        ip_uaserver = att["ip"]
        port_uaserver = int(att["puerto"])
        # RTPAUDIO
        att = attributes[2]
        puerto_rtp = att["puerto"]
        # REGPROXY
        att = attributes[3]
        server_proxy_ip = att["ip"]
        server_proxy_port = int(att["puerto"])
        # LOG
        att = attributes[4]
        log_path = att["path"]
        # AUDIO
        att = attributes[5]
        audio_path = att["path"]
        rtp_destination = {}
        # Creamos servidor de eco y escuchamos
        serv = socketserver.UDPServer((ip_uaserver, port_uaserver),
                                      EchoHandler)
        print("Listening...")
        write_log("Listening...", "Starting", ip_uaserver,
                  port_uaserver, log_path)
    try:
        serv.serve_forever()
    except ValueError or TypeError or KeyboardInterrupt:
        print("Usage: python3 uaserver.py config")
