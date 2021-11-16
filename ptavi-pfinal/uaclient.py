#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa User Agent Client
Autor: Manuel Salcedo Alonso
"""

import socket
import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time


# Cliente UDP simple.
def register_message(transmitter, expires_time):
    message_register = "REGISTER sip:" + str(transmitter) +\
                       ":" + port_uaserver + " SIP/2.0\r\n" \
                       + "Expires: " + expires_time + "\r\n"
    return message_register


def invite_message(receiver, transmitter, ip_origin):
    username = transmitter.split(":")[0]
    description_invite = "v=0\r\no=" + str(username) + " "\
                         + str(ip_origin) + "\r\n" + \
                         "s=misesion\r\nt=0\r\nm=audio 34543 RTP\r\n"

    head_invite = "INVITE sip:" + str(receiver)\
                  + " SIP/2.0\r\n"\
                  + "Content-Type: application/sdp\r\nContent-Length: "
    length = str(len(bytes(head_invite + description_invite, 'utf-8')))
    message_invite = head_invite + length + "\r\n\r\n" + description_invite
    return message_invite


def ack_message(receiver):
    message_ack = "ACK sip:" + receiver + " SIP/2.0\r\n"
    return message_ack


def bye_message(receiver):
    message_bye = "BYE sip:" + receiver + " SIP/2.0\r\n"
    return message_bye


def write_log(message, case, server, port, log_path):
    """
    Editamos/Creamos en el fichero de log
    """
    date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
    seconds_hour = int(time.strftime('%H', time.localtime(time.time())))
    seconds_minute = int(time.strftime('%M', time.localtime(time.time())))
    seconds = int(time.strftime('%S', time.localtime(time.time())))
    seconds = seconds_hour * 3600 + seconds_minute * 60 + seconds
    if case == "Sent to" or case == "Received from":
        message = date + str(seconds) + " " + case + " " + server + ":"\
                  + str(port) + " " \
                  + message.replace("\r\n", " ") + "\r\n"
    elif case == "Error":
        message = date + str(seconds) + " " + "Error: No server listening at" \
                  + server + " port " + str(port) + "\r\n"
    else:
        message = date + str(seconds) + " " + message + "\r\n"
    with open(log_path, 'a') as log_file:
        log_file.write(message)


class XMLHandler(ContentHandler):
    """
    Clase para manejar los XML
    """

    def __init__(self):
        """
        Constructor. Inicializamos la lista.
        """
        self.tags = {
            "account": ['username', 'passwd'],
            "uaserver": ['ip', 'puerto'],
            "rtpaudio": ['puerto'],
            "regproxy": ['ip', 'puerto'],
            "log": ['path'],
            "audio": ['path']
        }
        self.tag_list = []

    def startElement(self, name, attrs):
        """
        Método que se llama cuando se abre una etiqueta
        """
        if name in self.tags:
            # Creamos una lista
            tag_list = {}
            tag_list["tag"] = name
            for attribute in self.tags[name]:
                tag_list[attribute] = attrs.get(attribute, "")
            self.tag_list.append(tag_list)

    def get_tags(self):
        return self.tag_list


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 uaclient.py config method option")

    parser = make_parser()
    XMLClass = XMLHandler()
    parser.setContentHandler(XMLClass)
    parser.parse(open(str(sys.argv[1])))
    attributes = XMLClass.get_tags()

    # ACCOUNT
    att = attributes[0]
    username = att["username"]
    passwd = att["passwd"]
    # UASERVER
    att = attributes[1]
    ip_uaserver = att["ip"]
    port_uaserver = att["puerto"]
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
    if str(sys.argv[2]) == "REGISTER":
        expires_time = sys.argv[3]
    if str(sys.argv[2]) == "INVITE":
        receiver = sys.argv[3]
    if str(sys.argv[2]) == "BYE":
        receiver = sys.argv[3]
    if len(sys.argv) != 4:
        print("Usage: python3 client.py method receiver@IP:SIPport")
    method = sys.argv[2]
    # Creamos el socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((server_proxy_ip, server_proxy_port))

        if method == "REGISTER":
            write_log("Starting...", "Start", "",
                      server_proxy_port, log_path)
            message = register_message(username,
                                       expires_time)
            write_log(message, "Sent to", server_proxy_ip,
                      server_proxy_port, log_path)

        elif method == "INVITE":
            message = invite_message(receiver, username, ip_uaserver)
            write_log(message, "Sent to", server_proxy_ip,
                      server_proxy_port, log_path)

        elif method == "BYE":
            message = bye_message(receiver)
            write_log(message, "Sent to", server_proxy_ip,
                      server_proxy_port, log_path)
            write_log("Finishing...", "Finish", "",
                      server_proxy_port, log_path)

        try:
            my_socket.send(bytes(message, 'utf-8'))
        except ConnectionRefusedError:
            write_log("", "Error", server_proxy_ip,
                      server_proxy_port, log_path)
            write_log("Finishing...", "Finish", server_proxy_ip,
                      server_proxy_port, log_path)
            sys.exit("Finishing...")
