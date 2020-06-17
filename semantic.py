from lexical import scanner
from parse import parser

class semantic():
    def __init__(self,ps):
        self.ps = ps

    def type_check(self):
        symbol = [s[0] for s in self.ps.symbol_table]
        types = [s[1] for s in self.ps.symbol_table]
        if len(symbol) != len(set(symbol)):
            print("\nsame variable declared more than twice")
            return 0

        st = {s[0]: s[1] for s in self.ps.symbol_table}
        node = self.ps.parse_tree
        while len(node.children) != 0:
            node = node.children[0]
        node = node.get_next()
        ck = True
        while node.parent != None:
            if node.data == "[a-zA-Z]*":
                if ck:
                    cur_type = st[node.id]
                    ck = False
                elif cur_type != st[node.id]:
                    print("Type error occured")
                    return 0
            elif node.data in [";", "THEN", "{"]:
                ck = True
            node = node.get_next()
        print()




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

    print("LL Grammar")
    for i in parsing.grammar:
        for j in parsing.grammar[i]:
            if j[0]=='':
                print(i, '->', "''")
            else:
                print(i,'->',' '.join(j))
    parsing.get_FIRST()
    parsing.get_FOLLOW()

    print("\nFIRST")
    for i in parsing.first:
        print(i, parsing.first[i])

    print("\nFOLLOW")
    for i in parsing.follow:
        print(i, parsing.follow[i])

    parsing.get_Table()
    print("\n terminals")
    print(parsing.terminal)
    print("\n non terminals")
    print(parsing.non_terminal)

    print("\nTable")
    print(parsing.non_terminal + ['$'])
    for i in range(len(parsing.table)):
        print(parsing.terminal[i], parsing.table[i])

    print()
    input_list =parsing.tokens_to_input(tokens)
    asdf = parsing.parsing(input_list)
    if asdf:
        parsing.parse_tree.node_print()
    else:
        print("input not accecpted")

    print("\n")
    parsing.get_symbol_table()
    print("symbol Table\nsymbol, type")
    for s in parsing.symbol_table:
        print(s)

    asdf = semantic(parsing)
    asdf.type_check()