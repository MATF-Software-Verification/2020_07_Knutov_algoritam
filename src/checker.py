import ast
import traceback

#function that is used in main.py to check the validity of input code
#it returns True if input code is valid or False if it's not
def check_validity(input_file):
    with open(input_file) as f:
        source = f.read()
#return value of this function
    valid = True
    try:
#parse() generates an abstract syntax tree
#if the parsing was successful it means that the input file is valid
        ast.parse(source)
    except SyntaxError:
#throws an exception if the parsing was not successful and sets valid to false
        valid = False
        traceback.print_exc()
    return valid
