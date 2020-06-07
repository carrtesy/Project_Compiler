import sys
from lexical import scanner
from parse_tree import Node

class parser():
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar_path = grammar_path
        self.grammar = self.grammar_to_LL()
        self.classify_symbol()



    def grammar_to_LL(self):
        grammar = self.set_grammar()
        Recursion_Removed_grammar = self.Remove_Left_Recursion(grammar)
        Factoring_Removed_grammar = self.Remove_Left_factoring(Recursion_Removed_grammar)

        return grammar

    def get_FIRST(self):
        self.first = dict()
        keys = list(self.grammar.keys())
        for key in keys:
            self.first[key] = self.FIRST(key)

    def get_FOLLOW(self):
        self.follow = dict()
        keys = list(self.grammar.keys())
        for key in keys:
            self.follow[key] = set([])
        self.follow[keys[0]] = self.follow[keys[0]].union({"$"})
        for key in keys:
            self.FOLLOW(key)

    def get_Table(self):
        self.table = []
        for i, terminal in enumerate(self.terminal):
            self.table.append([])
            for non_terminal in (self.non_terminal + ["$"]):
                self.table[i].append(0)

        for left in list(self.grammar.keys()):
            index = self.terminal.index(left)
            first = self.first[left]
            follow = self.follow[left]
            for right in self.grammar[left]:
                first2 = self.First(right)
                for i in first2:
                    if i != '':
                        self.table[index][self.non_terminal.index(i)] = right
                if '' in right:
                    for i in follow:
                        if i == '$':
                            self.table[index][-1] = right
                        else:
                            self.table[index][self.non_terminal.index(i)] = right
                    if '$' in follow:
                        self.table[index][-1] = right

    def parsing(self,input_txt):
        terminal = {key : word for word, key in enumerate(self.terminal)}
        non_terminal = { key : word for word, key in enumerate(self.non_terminal)}
        non_terminal['$'] = len(non_terminal)
        input_txt.append("$")
        stack = [self.terminal[0],'$']
        self.parse_tree = Node(stack[-1],None,0)
        check = False
        while len(stack) != 1:
            top = stack[0]
            stack = stack[1:]
            # print(stack, input_txt)
            symbol = input_txt[0]
            if top in non_terminal:
                if symbol == top:
                    input_txt = input_txt[1:]
                    self.parse_tree = self.parse_tree.get_next()
                else:
                    check = True
                    break
            else:
                push = self.table[terminal[top]][non_terminal[symbol]]
                if push != 0 :
                    if push != ['']:
                        stack = push + stack
                        self.parse_tree.set_child(push)
                        self.parse_tree = self.parse_tree.children[0]
                    else:
                        self.parse_tree.set_child([''])
                        self.parse_tree = self.parse_tree.get_next()
                else:
                    check = True
                    break
        if check:
            return None
        else:
            self.parse_tree = self.parse_tree.get_root()
            return self.parse_tree








    def set_grammar(self):
        with open(self.grammar_path, 'r', encoding="utf-8") as g:
            grammar_txt = g.read()
        grammar_list = grammar_txt.strip().split(";\n")
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

    def First(self,key):
        symbol = key[0];
        result = set()
        if symbol in self.grammar.keys():
            if list(self.first[symbol])=={''}:
                if len(key)==1:
                    result = result.union({''})
                else:
                    result = result.union(self.First(key[1:]))
            else:
                result = result.union(self.first[symbol])
        else:
            result = result.union({symbol})
        return result



    def FOLLOW(self,symbol):
        keys = list(self.grammar.keys())
        for key in keys:
            for values in self.grammar[key]:
                for i in range(len(values)):
                    if values[i] == symbol:
                        if i < (len(values) - 1):
                            if values[i+1] in keys:
                                next_first = self.first[values[i+1]]
                            else:
                                next_first = {values[i+1]}
                            if '' in next_first and key != symbol:
                                if not key in list(self.follow.keys()):
                                    self.FOLLOW(key)
                                self.follow[symbol] = self.follow[symbol].union(self.follow[key])
                            self.follow[symbol] = self.follow[symbol].union(next_first-{''})

                        else:
                            if key!=symbol:
                                if not key in list(self.follow.keys()):
                                    self.FOLLOW(key)
                                self.follow[symbol] = self.follow[symbol].union(self.follow[key])

    def classify_symbol(self):
        self.terminal = list(self.grammar.keys())
        self.non_terminal = set()
        for terminal in self.terminal:
            for values in self.grammar[terminal]:
                for value in values:
                    if not value in (self.terminal + ['']):
                        self.non_terminal = self.non_terminal.union({value})
        self.non_terminal = list(self.non_terminal)
        self.non_terminal.sort()


if __name__ == "__main__":
    with open("testfile.txt", 'r') as test:
        code = test.read()

    scan = scanner(code)
    scan.lexical()
    tokens = scan.tokens
    for token in tokens:
        print(token)
    print()

    parsing = parser(tokens, "grammar2.txt")
    parsing.get_FIRST()
    parsing.get_FOLLOW()
    parsing.get_Table()
    print("LL Grammar")
    for i in parsing.grammar:
        print(i, parsing.grammar[i])
    print("\nFIRST")
    for i in parsing.first:
        print(i, parsing.first[i])

    print("\nFOLLOW")
    for i in parsing.follow:
        print(i, parsing.follow[i])
    print("\n terminals")
    print(parsing.terminal)
    print("\n non terminals")
    print(parsing.non_terminal)

    print("\nTable")
    print(parsing.non_terminal + ['$'])
    for i in range(len(parsing.table)):
        print(parsing.terminal[i], parsing.table[i])

    print()
    asdf = parsing.parsing(["word", '"("', '")"'])
    if asdf:
        parsing.parse_tree.node_print()
    else:
        print("input not accecpted")


