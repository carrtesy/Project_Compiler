import sys
from lexical import scanner



class parser():
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar_path = grammar_path

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
                grammar[prime].append([])
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
                            grammar[prime].append(values[i][1:])

                        if (values[i]) in grammar[key]:
                            grammar[key].remove(values[i])
                        if not (values[j][1:]) in grammar[prime]:
                            grammar[prime].append(values[j][1:])
                        if (values[j]) in grammar[key]:
                            grammar[key].remove(values[j])
            index += 1
        return grammar

if __name__ == "__main__":
    with open("testfile.txt",'r') as test:
        code = test.read()


    scan = scanner(code)
    scan.lexical()
    tokens = scan.tokens

    parsing = parser(tokens,"grammar.txt")
    gr = parsing.grammar_to_LL()
    print(gr)
