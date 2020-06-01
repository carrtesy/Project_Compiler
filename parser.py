import sys
from lexical import scanner



class parser():
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar_path = grammar_path
        self.grammar = self.grammar_to_LL()

    def set_grammar(self):
        with open(self.grammar_path, 'r', encoding="utf-8") as g:
            grammar_txt = g.read()
        grammar_list = grammar_txt.split(";\n")
        grammar = dict()

        for trans in grammar_list:
            key, value = trans.split("->")
            key = key.strip()
            grammar[key] = []
            value = value.split("|")
            for val in value:
                val = val.split()
                if len(val):
                    grammar[key].append(val)
                else:
                    grammar[key].append([""])

        return grammar



    def grammar_to_LL(self):
        grammar = self.set_grammar()
        Recursion_Removed_grammar = self.Remove_Left_Recursion(grammar)
        Factoring_Removed_grammar = self.Remove_Left_factoring(Recursion_Removed_grammar)

        return grammar

    def Remove_Left_Recursion(self, grammar):
        keys = list(grammar.keys())

        for key in keys:
            values = list(grammar[key])
            recursion = []
            non_recursion = []

            for value in values:
                if key == value[0]:
                    recursion.append(value[1:])
                    grammar[key].remove(value)
                else:
                    non_recursion.append(value)

            if len(recursion):
                grammar[key] = list()
                prime = key + "'"
                grammar[prime] = list()
                for val in non_recursion:
                    grammar[key].append(val+[prime])

                for val in recursion:
                    grammar[prime].append(val + [prime])
                grammar[prime].append([""])
        return grammar


    def Remove_Left_factoring(self, grammar):
        keys = list(grammar.keys())
        length = len(keys)
        index = 0
        while ((index + 1) < len(list(grammar.keys()))):
            key = list(grammar.keys())[index]
            values = list(grammar[key])
            prime = key + '"'
            len_values = len(values)

            for i in range(len_values-1):
                check = False
                for j in range(i+1,len_values):
                    if not (values[i] and values[j]):
                        continue
                    if values[i][0] == values[j][0]:

                        value = values[i][0]
                        if not prime in list(grammar.keys()):
                            grammar[prime] = []

                        if not ([value, prime]) in grammar[key]:
                            grammar[key].append([value,prime])

                        if not (values[i][1:]) in grammar[prime]:
                            if values[i][1:]:
                                grammar[prime].append(values[i][1:])
                            elif not [""] in grammar[prime]:
                                grammar[prime].append([""])

                        if (values[i]) in grammar[key]:
                            grammar[key].remove(values[i])
                        if not (values[j][1:]) in grammar[prime]:
                            if values[j][1:]:
                                grammar[prime].append(values[j][1:])
                            elif not [""] in grammar[prime]:
                                grammar[prime].append([""])

                        if (values[j]) in grammar[key]:
                            grammar[key].remove(values[j])
            index += 1
        return grammar

    def get_FIRST(self):
        self.first = dict()
        keys = list(self.grammar.keys())
        for key in keys:
            self.first[key] = self.FIRST(key)

    def FIRST(self,key):
        keys = list(self.grammar.keys())
        values = self.grammar[key]
        first = set()
        for value in values:

            if value[0] in keys:
                for symbol in value:
                    fst = self.FIRST(symbol)
                    if len(fst) != 0:
                        first = first.union(fst)
                        break

            else:
                first = first.union({value[0]})
        return first

    def get_FOLLOW(self):
        self.follow = dict()
        keys = list(self.grammar.keys())
        for key in keys:
            self.follow[key] = self.FOLLOW(key)
    def FOLLOW(self,key):
        keys = list(self.grammar.keys())
        values = self.grammar[key]
        follow = set()
        if key == keys[0]:
            follow.union({"$"})
        for value in values:
            for i in range(len(value)):
                symbol = value[i]

                first = self.FIRST()
                if i < len(value):
                    follow.union(self.FIRST())






if __name__ == "__main__":
    with open("testfile.txt",'r') as test:
        code = test.read()


    scan = scanner(code)
    scan.lexical()
    tokens = scan.tokens

    parsing = parser(tokens,"grammar.txt")
    parsing.get_FIRST()
    print(parsing.grammar)
    print(parsing.first)
