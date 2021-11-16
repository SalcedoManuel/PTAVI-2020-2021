#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoohija

# Abrimos el fichero
fich = open(sys.argv[1])
# Leemos todas las líneas y las guardamos en una lista
lineas = fich.readlines()

# Bucle de longitud la cantidad de lineas
for linea in lineas:
    # Tipo de Operación
    operator = linea[:linea.find(',')]

    # Ahora pondremos la lista de los números
    numbers = linea[linea.find(',') + 1:]
    if linea.find('\n') > 0:
        numbers = linea[linea.find(',')+1:linea.find('\n')]
        numbers = numbers.split(',')
    else:
        numbers = numbers.split(',')
    result = int(numbers[0])
    numbers = numbers[1:]
    for number in numbers:
        if operator == "suma":
            operacion = calcoohija.CalculadoraHija(result,
                                                   int(number), result)
            operacion.suma()
            result = operacion.result

        elif operator == "resta":

            operacion = calcoohija.CalculadoraHija(result,
                                                   int(number), result)
            operacion.resta()
            result = operacion.result

        elif operator == "multiplica":
            operacion = calcoohija.CalculadoraHija(result,
                                                   int(number), result)
            operacion.multi()
            result = operacion.result

        elif operator == "divide":
            operacion = calcoohija.CalculadoraHija(result,
                                                   int(number), result)
            operacion.division()
            result = operacion.result
    print("El resultado de la operación es = " +
          str(result))
# Cerramos el fichero
fich.close()
