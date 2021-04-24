import sys
import os
from pathlib import Path

sys.path.insert(1, '../')
from InputProgram import InputProgram
from checker import check_validity

from utils.Graph import CFG
from utils.Knuth import Knuth

def activate(code):
    block_stack = []
    blocks = []

    input_program = InputProgram(code)
    input_program.basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)

    block_id = 1
    block_stack = input_program.get_block_stack()
    for block in input_program.basic_blocks:
        blocks.append(block)
        block_id += 1

    from pprint import pprint
    cfg = CFG(block_stack)

    graph = cfg.getGraph()
    spanning_tree = cfg.spanning_tree()

    knuth = Knuth(cfg)
    inv_spanning_tree, calculate_weights_steps = knuth.set_edge_weights()
    
    return [blocks, graph, spanning_tree, inv_spanning_tree, calculate_weights_steps]


def main():
    if not check_validity(Path('./test_input.py')):
        print('Input code not valid', file=sys.stderr)
        sys.exit(1)

    code = []
    with open(Path('./test_input.py'), 'r') as input_file:
        code = input_file.read()

    blocks = activate(code)

    with open(Path('./output.py'), 'w') as output:
        for block in blocks:
            output.write(block.stringify_block())
            output.write('\n')

        output.flush()


if __name__ == '__main__':
    main()
