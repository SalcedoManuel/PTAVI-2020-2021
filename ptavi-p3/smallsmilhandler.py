#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILLHandler(ContentHandler):

    # Definimos el init
    def __init__(self):
        # Guardamos todas las etiquetas y sus atributos
        self.tags = {
            # etiqueta = root-layout
            "root-layout": ['width', "height", "background-color"],
            # etiqueta = region
            "region": ["id", "top", "bottom", "left", "right"],
            # etiqueta = img
            "img": ["src", "begin", "dur"],
            # etiqueta = audio
            "audio": ["src", "begin", "dur"],
            # etiqueta = textstream
            "textstream": ["src", "region"]
        }
        self.tag_list = []

    def startElement(self, name, attrs):
        # Si name está dentro de self.tags
        if name in self.tags:
            # Creamos una lista de etiquetas
            tag_list = {}
            # Asignamos el nombre de la etiqueta
            tag_list["tag"] = name
            # Bucle que saca los atributos y los guarda en el array
            for attribute in self.tags[name]:
                tag_list[attribute] = attrs.get(attribute, "")
            # Agregamos la etiqueta a la lista de etiquetas
            self.tag_list.append(tag_list)

    # Obtener todas las etiquetas
    def get_tags(self):
        return self.tag_list


if __name__ == '__main__':

    parser = make_parser()
    SmallSmill = SmallSMILLHandler()
    parser.setContentHandler(SmallSmill)
    parser.parse(open('karaoke.smil'))
    print(SmallSmill.get_tags())
