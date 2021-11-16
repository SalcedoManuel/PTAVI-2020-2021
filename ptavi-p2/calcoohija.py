#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoo


class CalculadoraHija(calcoo.Calculadora):
    pass

    def multi(self):
        self.result = self.first * self.second

    def division(self):
        if self.second == 0:
            self.result = 0
            sys.exit('Division by zero is not allowed')
        else:
            self.result = self.first / self.second


if __name__ == "__main__":
    try:
        operando1 = int(sys.argv[1])
        operando2 = int(sys.argv[3])
    except ValueError:
        sys.exit("Error: Non numerical parameters")

    operacion = CalculadoraHija(operando1, operando2, 1)
    if sys.argv[2] == "suma":
        operacion.suma()
    elif sys.argv[2] == "resta":
        operacion.resta()
    elif sys.argv[2] == "multiplicacion":
        operacion.multi()
    elif sys.argv[2] == "division":
        operacion.division()
    else:
        sys.exit('Operación sólo puede ser sumar o restar.')

    print(operacion.result)
