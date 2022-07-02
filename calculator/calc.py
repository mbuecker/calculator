"""
Calculator
"""
import math

Parservars = [("pi", math.pi),
              ("e", math.e),
              ("tau", math.tau)
              ]


class Parser:
    s_formel = ""
    pos = 0
    maxpos = 0
    errorFlag = False
    errorText = ""
    result = 0.0
    lasttokenisvar = False
    lastvartoken = ""

    def __init__(self, s_formel):
        self.setformel(s_formel)

    def setformel(self, s_formel):
        self.s_formel = s_formel
        self.pos = 0
        self.maxpos = len(self.s_formel)
        self.errorFlag = False
        self.result = 0.0
        self.lasttokenisvar = False
        self.lastvartoken = ""

    def printformel(self):
        print(self.s_formel)

    def printerror(self):
        if self.errorFlag:
            print("errorFlag:", self.errorFlag)
            print("errorText:", self.errorText)
            print(self.s_formel)
            for i in range(self.pos):
                print("-", end='')
            print('^')

    def getformeltail(self):
        s = self.s_formel[self.pos: self.maxpos]
        return s

    def get_clamped_value(self):
        cntbracket = 1
        cntintern = 0
        self.pos += 1
        while self.pos < self.maxpos:
            if self.s_formel[self.pos] == '(':
                cntbracket += 1
            elif self.s_formel[self.pos] == ')':
                cntbracket -= 1

            self.pos += 1
            cntintern += 1

            if cntbracket == 0:
                break

        if cntbracket != 0:
            self.errorFlag = True
            self.errorText = "clamp error"
            value = 0
        else:
            r_formel = self.s_formel[self.pos - cntintern:self.pos - 1]
            r_p = Parser(r_formel)
            value = r_p.parse()

        return value

    def getvalue(self):

        negflag = 1
        value = 0.0
        self.lasttokenisvar = False

        # jump over spaces
        while self.pos < self.maxpos and self.s_formel[self.pos].isspace():
            self.pos += 1

        # +/-
        if self.pos < self.maxpos:
            if self.s_formel[self.pos] == '-':
                negflag = -1
                self.pos += 1
            elif self.s_formel[self.pos] == '+':
                self.pos += 1
        else:
            self.errorFlag = True
            self.errorText = "end unexpected"

        # digits
        if self.pos < self.maxpos:
            if self.s_formel[self.pos].isdigit():
                cntdigit = 0
                while self.pos < self.maxpos:
                    if self.s_formel[self.pos].isdigit() or self.s_formel[self.pos] == '.':
                        self.pos += 1
                        cntdigit += 1
                    else:
                        break

                value = float(self.s_formel[self.pos - cntdigit:self.pos])

            elif self.s_formel[self.pos].isalpha():
                # variable or function
                cntalnum = 0
                while self.pos < self.maxpos:
                    if self.s_formel[self.pos].isalnum():
                        self.pos += 1
                        cntalnum += 1
                    else:
                        break

                tok = self.s_formel[self.pos - cntalnum:self.pos]

                if self.pos < self.maxpos and self.s_formel[self.pos] == '(':
                    # it's a function

                    value = self.get_clamped_value()

                    if not self.errorFlag:
                        if tok == "sqrt":  # Wurzel
                            value = math.sqrt(value)
                        elif tok == "ceil":  # aufrunden auf ganze Zahl
                            value = math.ceil(value)
                        elif tok == "floor":  # runden auf ganze Zahl
                            value = math.floor(value)
                        else:
                            self.errorFlag = True
                            self.errorText = "Unbekante Funktion", tok
                            value = 0

                else:
                    # it's a variable
                    value = 0
                    self.lasttokenisvar = True
                    self.lastvartoken = tok

                    for v in Parservars:
                        if v[0] == tok:
                            value = v[1]
                            break

            elif self.s_formel[self.pos] == '(':

                value = self.get_clamped_value()

            else:
                self.errorFlag = True
                self.errorText = "value, variable or function expected"

        else:
            self.errorFlag = True
            self.errorText = "value, variable or function expected"

        return float(value * negflag)

    @property
    def getoperator(self):

        # jump over spaces
        while self.pos < self.maxpos and self.s_formel[self.pos].isspace():
            self.pos += 1

        # +/-
        if self.pos < self.maxpos:
            if self.s_formel[self.pos] == '-':
                self.pos += 1
                return '-'
            elif self.s_formel[self.pos] == '+':
                self.pos += 1
                return '+'
            elif self.s_formel[self.pos] == '*':
                self.pos += 1
                return '*'
            elif self.s_formel[self.pos] == '/':
                self.pos += 1
                return '/'
            elif self.s_formel[self.pos] == '=' and self.lasttokenisvar:
                self.pos += 1
                return '='

        self.errorFlag = True
        self.errorText = "no operator found"
        return ''

    def parse(self):
        val1 = self.getvalue()
        if self.errorFlag:
            # print(self.errorText)
            pass
        else:
            # print(tetst"Value1:", v  al1)

            o = self.getoperator
            if self.errorFlag:
                self.errorFlag = False
                self.errorText = "reached the end of the expression"
                self.result += val1
            else:
                if o == '=':
                    r_formel = self.getformeltail()
                    r_p = Parser(r_formel)
                    val3 = r_p.parse()
                    self.errorFlag = r_p.errorFlag
                    self.errorText = r_p.errorText
                    self.result = 0
                    if not self.errorFlag:
                        self.result = val3
                        Parservars.insert(0, (self.lastvartoken, val3))
                    return self.result

                val2 = self.getvalue()
                if self.errorFlag:
                    return self.result
                else:

                    # ist ein weiterer Operator gegeben
                    op2 = self.getoperator
                    if not self.errorFlag:
                        # print("Weiterer Operator:", op2)

                        if o == '*':
                            val2 = val1 * val2
                            val1 = 0
                        if o == '/':
                            if val2 == 0:
                                self.errorFlag = True
                                self.errorText = "division by 0"
                                self.result = 0
                                return self.result
                            else:
                                val2 = val1 / val2
                                val1 = 0

                        # print("Starte Rekursion")
                        r_formel = self.getformeltail()
                        r_p = Parser(r_formel)
                        val3 = r_p.parse()

                        if not r_p.errorFlag:
                            if op2 == '+':
                                val2 += val3
                            if op2 == '-':
                                val2 -= val3
                            if op2 == '*':
                                val2 *= val3
                            if op2 == '/':
                                if val3 == 0:
                                    self.errorFlag = True
                                    self.errorText = "division by 0"
                                    self.result = 0
                                    return self.result
                                else:
                                    val2 /= val3
                        else:
                            # print( rp.errorText)
                            self.errorFlag = r_p.errorFlag
                            self.errorText = r_p.errorText

                        # print("Ende Rekursion")
                    else:
                        if self.pos < self.maxpos:
                            self.errorText = "exprssion error"
                            return 0

                        self.errorFlag = False
                        self.errorText = ""
                        if o == '*':
                            val2 *= val1
                        if o == '/':
                            if val2 == 0:
                                self.errorFlag = True
                                self.errorText = "division by 0"
                                self.result = 0
                                return self.result
                            else:
                                val2 = val1 / val2

                    if not self.errorFlag:
                        if o == '+':
                            self.result = val1 + val2
                        if o == '-':
                            self.result = val1 - val2
                        if o == '*':
                            self.result = val2
                        if o == '/':
                            self.result = val2
                    else:
                        # print( self.errorText)
                        pass

            return self.result
