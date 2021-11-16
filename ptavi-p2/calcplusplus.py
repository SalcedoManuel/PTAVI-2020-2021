#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import sys
import calcoohija

resultado = 0

with open(sys.argv[1], newline='') as csvfile:
    operatorreader = csv.reader(csvfile)
    for row in operatorreader:
        operador = row[0]
        if len(row) > 0:
            numeros = row[1:]
        if len(numeros) > 0:
            resultado = int(numeros[0])
            numeros = numeros[1:]

        if operador == "suma":
            for number in numeros:
                operacion = calcoohija.CalculadoraHija(resultado,
                                                       int(number), resultado)
                operacion.suma()
                resultado = operacion.result

        elif operador == "resta":
            for number in numeros:
                operacion = calcoohija.CalculadoraHija(resultado,
                                                       int(number), resultado)
                operacion.resta()
                resultado = operacion.result

        elif operador == "multiplica":
            for number in numeros:
                operacion = calcoohija.CalculadoraHija(resultado,
                                                       int(number), resultado)
                operacion.multi()
                resultado = operacion.result

        elif operador == "divide":
            for number in numeros:
                operacion = calcoohija.CalculadoraHija(resultado,
                                                       int(number), resultado)
                operacion.division()
                resultado = operacion.result
        print("La operación: " + operador +
              " nos da el resultado =  " + str(resultado))
