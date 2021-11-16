#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class ChistesHandler(ContentHandler):
    """
    Clase para manejar chistes malos
    """

    def __init__(self):
        """
        Constructor. Inicializamos las variables
        """
        self.calificacion = ""
        self.pregunta = ""
        self.inPregunta = False
        self.respuesta = ""
        self.inRespuesta = False

    def startElement(self, name, attrs): # Inicio de Etiqueta NAME = Nombre de la etiqueta, attrs = Diccionario
        """
        Método que se llama cuando se abre una etiqueta
        """
        # Solo hará cosas mientras la etiqueta sea como pone.
        if name == 'chiste':
            # De esta manera tomamos los valores de los atributos
            self.calificacion = attrs.get('calificacion', "") #Nos quedamos con el atributo de calificación
            self.calificacion = attrs.get('risa', "")
        elif name == 'pregunta':
            self.inPregunta = True   # He encontrado una etiqueta pregunta.
        elif name == 'respuesta':
            self.inRespuesta = True  # He encontrado una etiqueta respuesta.

    def endElement(self, name):  # Final de Etiqueta
        """
        Método que se llama al cerrar una etiqueta
        """
        if name == 'pregunta':
            # guardar el contenido en una variable self.content
            self.pregunta = ""
            self.inPregunta = False # Ya no estamos en la etiqueta.
        if name == 'respuesta':
            self.respuesta = ""
            self.inRespuesta = False

    def characters(self, char):  # Entre Etiquetas
        """
        Método para tomar contenido de la etiqueta
        """
        if self.inPregunta: # Si estoy dentro de la pregunta
            self.pregunta = self.pregunta + char
        if self.inRespuesta: # Si estoy dentro de la respuesta
            self.respuesta += char


if __name__ == "__main__":
    """
    Programa principal
    """
    parser = make_parser()  # parser va leyendo línea a línea.
    cHandler = ChistesHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open('chistes2.xml')) # Este es el fichero que va a parsear.
