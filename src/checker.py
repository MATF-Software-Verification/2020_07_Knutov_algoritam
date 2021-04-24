import ast
import traceback


def check_validity(input_file):
    with open(input_file) as f:
        source = f.read()
    valid = True
    try:
        ast.parse(source)
    except SyntaxError:
        valid = False
        traceback.print_exc()
    return valid
