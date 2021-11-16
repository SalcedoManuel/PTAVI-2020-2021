#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


class Calculadora:
    """A simple class"""

    def __init__(self, first, second, result):
        """Function to init the class"""
        self.first = first
        self.second = second
        self.result = result

    def suma(self):
        """ Function to sum the operands. Ops have to be ints """
        self.result = self.first + self.second

    def resta(self):
        """ Function to substract the operands """
        self.result = self.first - self.second

    def print_result(self):
        print(self.result)


if __name__ == "__main__":
    try:
        operando1 = int(sys.argv[1])
        operando2 = int(sys.argv[3])
    except ValueError:
        sys.exit("Error: Non numerical parameters")

    operacion = Calculadora(operando1, operando2, 0)
    if sys.argv[2] == "suma":
        operacion.suma()
    elif sys.argv[2] == "resta":
        operacion.resta()
    else:
        sys.exit('Operación sólo puede ser sumar o restar.')

    print(operacion.result)
