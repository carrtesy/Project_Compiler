import csv

class parser():
    def __init__(self, code: list):
        self.code = code
        self.code.insert(0, "$")
        self.length = len(code)
        self.stack = ["$", "0"]
        self.terminals = ["word", "num", "int", "char",
                      "{", "}", "IF", "ELSE", "THEN",
                      "WHILE", "RETURN", ";", "(", ")",
                      "=", "==", ",", ">", "+", "*", "$"
                      ]
        self.nonterminals = ["prog", "decl", "decls", "cond",
                         "vtype", "words", "slist", "stat",
                         "expr", "term", "fact", "block"
                         ]
        self.rules = [
            [["prog_"], ["prog"]],
            [["prog"], ["word", "(", ")", "block"]],
            [["decls"], ["decls", "decl"]],
            [["decl"], ["vtype", "words", ";"]],
            [["words"], ["words", ",", "word"]],
            [["words"], ["word"]],
            [["vtype"], ["int"]],
            [["vtype"], ["char"]],
            [["block"], ["{", "decls", "slist", "}"]],
            [["slist"], ["slist", "stat"]],
            [["slist"], ["stat"]],
            [["stat"], ["IF", "cond", "THEN", "block", "ELSE", "block"]],
            [["stat"], ["WHILE", "cond", "block"]],
            [["stat"], ["word", "=", "expr", ";"]],
            [["stat"], ["RETURN", "expr", ";"]],
            [["cond"], ["expr", ">", "expr"]],
            [["cond"], ["expr", "==", "expr"]],
            [["expr"], ["term"]],
            [["expr"], ["term", "+", "term"]],
            [["term"], ["fact"]],
            [["term"], ["fact", "*", "fact"]],
            [["fact"], ["num"]],
            [["fact"], ["word"]],
            [["decls"], ["decl"]],
        ]

        self.numstates = 52
        self.actiontable = []
        self.gototable = []

    def initactiontable(self):
        f = open("action.csv", "r")
        rdr = csv.reader(f)
        for line in rdr:
            self.actiontable.append(line)
        f.close()

    def initgototable(self):
        f = open("goto.csv", "r")
        rdr = csv.reader(f)
        for line in rdr:
            self.gototable.append(line)
        f.close()

    def printactiontable(self):
        print("===ACTION TABLE===")
        for t in self.terminals:
            print("%7s" % t, end = "")
        print("")

        for row, state in enumerate(self.actiontable):
            for col, action in enumerate(state):
                print("%7s" % self.actiontable[row][col], end = "")
            print("")
        print("")

    def printgototable(self):
        print("===GOTO TABLE===")
        for t in self.nonterminals:
            print("%7s" % t, end = "")
        print("")

        for row, state in enumerate(self.gototable):
            for col, action in enumerate(state):
                print("%7s" % self.gototable[row][col], end = "")
            print("")
        print("")

    def printcode(self):
        for i in self.code:
            print(i, end = " ")

    def printstack(self):
        for i in self.stack:
            print(i, end = " ")

    def parse(self):
        self.initactiontable()
        self.initgototable()
        #debug
        self.printactiontable()
        self.printgototable()
        self.printcode()

        print("\nmain code")
        count = 0
        while(True):
            print("round ",  count+1)
            pstval = self.stack[-1] # value in parser stack
            cstval = self.code[-1] # value in code stack
            pstidx = int(pstval)
            cstidx = self.terminals.index(cstval)
            #print("")
            #print("pst {} cst {} val {}".format(pstval, cstval, self.actiontable[pstidx][cstidx]))

            tbval = self.actiontable[pstidx][cstidx]

            if(tbval == "" or tbval == None):
                print("not accepted")
                return False
            else:
                if(tbval == "accept"):
                    print("accepted")
                    return True
                else:
                    action = tbval[0]
                    number = int(tbval[1:])
                    if (action == "s"):
                        print("shift")
                        tmp = self.code.pop()
                        self.stack.append(tmp)
                        self.stack.append(str(number))
                    elif (action == "r"):
                        print("reduce")
                        # pop twice
                        refer = str(number)
                        syntax = self.rules[number][1]
                        for i in reversed(syntax):
                            self.stack.pop()
                            token = self.stack.pop()
                            if(i != token):
                                print("sth wrong")
                                return False
                        state = int(self.stack[-1])
                        nt = self.rules[number][0][0]
                        ntidx = self.nonterminals.index(nt)
                        self.stack.append(nt)
                        self.stack.append(self.gototable[state][ntidx])
                    else:
                        print("unexpected error")
                        return False

            #print(action, " ", number)


            print("stack: ", end = "")
            self.printstack()
            print("\n")
            count += 1
            if (count == 40):
                break


if __name__ == "__main__":
    #simple example
    code = ["word", "(", ")", "{", "int", "word", ";", "word", "=", "num", ";", "RETURN", "word", ";", "}"]
    input = []
    for i in code:
        input.insert(0, i)
    p = parser(input)
    p.parse()
