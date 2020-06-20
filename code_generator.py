from lexical import scanner
from parse import parser
from parse_tree import Node
from semantic import semantic

if __name__ == "__main__":
    # open test file
    with open("testfiles/testfile_1.txt", 'r') as test:
        code = test.read()

    # scanner : print tokens
    scan = scanner(code)
    scan.lexical()
    tokens = scan.tokens
    for token in tokens:
        print(token)
    print()

    # LL parser
    parsing = parser(tokens, "grammar2.txt")

    # LL Grammar
    print("LL Grammar")
    for i in parsing.grammar:
        for j in parsing.grammar[i]:
            if j[0]=='':
                print(i, '->', "''")
            else:
                print(i,'->',' '.join(j))
    parsing.get_FIRST()
    parsing.get_FOLLOW()

    # Get First Set
    print("\nFIRST")
    for i in parsing.first:
        print(i, parsing.first[i])

    # Get Follow Set
    print("\nFOLLOW")
    for i in parsing.follow:
        print(i, parsing.follow[i])

    # Based on First & Follow, get Parsing Table
    parsing.get_Table()

    # Terminals
    print("\n terminals")
    print(parsing.terminal)

    # Non-Terminals
    print("\n non terminals")
    print(parsing.non_terminal)

    # Parsing Table
    print("\nTable")
    print(parsing.non_terminal + ['$'])
    for i in range(len(parsing.table)):
        print(parsing.terminal[i], parsing.table[i])
    print()

    # Abstract Syntax Tree
    input_list = parsing.tokens_to_input(tokens)
    asdf = parsing.parsing(input_list)
    if asdf:
        print(asdf)
        slist = asdf.get_node_with_keyword("stat")
        for stat in slist:
            print(stat)
            bst = stat.get_binarySyntaxTree()
            print(bst)
    else:
        print("input not accepted")

    print("\n")
    parsing.get_symbol_table()
    print("Symbol Table\nsymbol, type, scope, size")
    for s in parsing.symbol_table:
        print(s)

    # Sementic Analysis
    asdf = semantic(parsing)
    asdf.type_check()