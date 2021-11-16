#!/usr/bin/python3
# -*- coding: utf-8 -*-
from xml.sax import make_parser
from smallsmilhandler import SmallSMILLHandler
from urllib.request import urlretrieve
import sys
import json


class KaraokeLocal:
    # Definimos el init
    def __init__(self, filename):
        parser = make_parser()
        SmallSmill = SmallSMILLHandler()
        parser.setContentHandler(SmallSmill)
        parser.parse(open(filename))
        # Obtenemos las etiquetas usando la función get_tags
        self.tag_list = SmallSmill.get_tags()

    def __str__(self):
        # Creamos la variable shell que mostrará por la shell la lista
        shell = ""
        # Bucle que buscará en la lista la etiqueta correspondiente
        for tag_list in self.tag_list:
            # Pasamos a la shell la etiqueta y el tabulador
            shell += tag_list['tag'] + '\t'
            # Ahora pasamos los atributos y
            # el contenido de los atributos de la etiqueta
            for attribute in tag_list:
                # Si el atributo No está vacío y tiene contenido
                if attribute != "tag" and tag_list[attribute]:
                    shell += attribute + "=" + '"'\
                             + tag_list[attribute] + '"' + "\t"
            # Añadimos el salto de línea
            shell = shell[:-1] + '\n'
        # Devolvemos el valor para imprimir
        return shell

    def do_json(self, file_smil, file_json=''):
        # Si filejson está vacío convertimos filesmil a filejson
        if not file_json:
            file_json = file_smil.replace(".smil", ".json")
        # file será filejson y se guardará NO SUBIR
        with open(file_json, "w") as file:
            json.dump(self.tag_list, file)

    def do_local(self):
        # Buscamos el contenido de los atributos
        for tag_list in self.tag_list:
            for attribute in tag_list:
                # Atributos no vacíos y
                # que el contenido del atributo empiece así
                if attribute != "tag" and\
                        tag_list[attribute].startswith("http://"):
                    # Obtenemos la url
                    url = tag_list[attribute]
                    # Sacamos el nombre del archivo
                    archive = url.split("/")[-1]
                    # Descargamos el archivo
                    urlretrieve(url, archive)
                    # Sustituimos la url por el nombre
                    tag_list[attribute] = archive


if __name__ == '__main__':

    try:
        # Si no hay dos argumentos deberá saltar la excepción.
        if len(sys.argv) == 2:
            # El fichero smil es el último argumento
            filename_smil = sys.argv[1]
        else:
            sys.exit("Usage: python3 karaoke.py file.smil")
    except IndexError:
        sys.exit("Usage: python3 karaoke.py file.smil")

    # Instanciamos un objeto de la clase KaraokeLocal
    Karaoke_Program = KaraokeLocal(filename_smil)
    # Imprimimos el objeto
    print(Karaoke_Program)
    # Llamamos a do_json pero usando el fichero .smil
    Karaoke_Program.do_json(filename_smil)
    # Llamamos a do_local
    Karaoke_Program.do_local()
    # Llamamos a do_json pero .json deberá ser local.json
    Karaoke_Program.do_json("local.json")
    # Imprimimos de nuevo el objeto
    print(Karaoke_Program)
