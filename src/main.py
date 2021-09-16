import sys

sys.path.insert(1, '../')
from InputProgram import InputProgram

from utils.Graph import CFG
from utils.Knuth import Knuth

def activate(code):
    blocks = []

    input_program = InputProgram(code)
    input_program.basic_blocks = input_program.divide_into_basic_blocks(input_program.instructions)

    block_id = 1
    block_stack = input_program.get_block_stack()
    for block in input_program.basic_blocks:
        blocks.append(block)
        block_id += 1

    cfg = CFG(block_stack)

    graph = cfg.getGraph()
    spanning_tree = cfg.spanning_tree()

    knuth = Knuth(cfg)
    inv_spanning_tree, calculate_weights_steps = knuth.set_edge_weights()
    
    return [blocks, graph, spanning_tree, inv_spanning_tree, calculate_weights_steps]

