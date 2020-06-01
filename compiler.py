from lexical import scanner

with open("testfile.txt", 'r') as txt:
    code = txt.read()

scan = scanner(code)
scan.lexical()
tokens = scan.tokens


if tokens[-1]:
    for i in tokens:
        print(i)



else:
    print("Error occurred in lexical analysis")


if __name__ == "__main__":