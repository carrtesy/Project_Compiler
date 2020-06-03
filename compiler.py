from lexical import scanner
import os

dir = os.path.dirname(__file__)
tnum = input("Enter testfile number (1 ~ 15): ")
fname = os.path.join(dir, 'testfiles/' + 'testfile_' + tnum + '.txt') #will change into parameter parsing w. various options later -지영현

with open(fname, 'r') as txt:
    code = txt.read()

scan = scanner(code)
scan.lexical()
token = scan.tokens

if token[-1]:
    for i in token:
        print(i)
else:
    print("Error occurred in lexical analysis")