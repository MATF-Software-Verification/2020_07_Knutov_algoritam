from pathlib import Path
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.Graph import CFG


from InputProgram import InputProgram
from blocks.BasicBlock import BasicBlock
with open(Path('../test_input.py'), 'r') as input_file:
    code = input_file.read()
input_program = InputProgram(code)

with open(Path('../block_test.py'), 'r') as input_file:
    code_block = input_file.read()
input_code_block = InputProgram(code_block)

with open(Path('../for_test.py'), 'r') as input_file:
    code_for = input_file.read()
input_code_for = InputProgram(code_for)

with open(Path('../if_test.py'), 'r') as input_file:
    code_if = input_file.read()
input_code_if = InputProgram(code_if)



class TestCFG(unittest.TestCase):
    def test_make_instractions(self):
        self.assertSequenceEqual(input_code_block.get_instructions(), ["a = 10","b = 12", "c = 0", "g = 0", "h = 0", "f = 0"])
        self.assertSequenceEqual(input_program.get_instructions(), [
                                 "a = 10", "b = 2", "if a > b:", "    h = 12", "else:", "    c = 20", "for i in range(10):",
        "    c += 1", "print(a)", "print(b)", "c = 1"], "test_input")
        self.assertSequenceEqual(input_code_for.get_instructions(), ["t=f=1", "for i in range(10):", "    t = 10", "    f += t", "print(f)"])
        self.assertSequenceEqual(input_code_if.get_instructions(), ["a = b = 10", "if a > b:", "    h = 12", "    g = 11", "else:",
                                                                    "    c = 20", "    f = 12", "if a == 10:", "    b = 1", "elif a < 10:",
                                                                    "    b = 2", "elif a > 10:", "    b = 3"])



    def test_leaders(self):
        self.assertSequenceEqual(input_code_block.get_leaders(input_code_block.get_instructions()), ["a = 10"])
        self.assertSequenceEqual(input_program.get_leaders(input_program.get_instructions()), [
                                 "a = 10", "if a > b:", "    h = 12", "else:", "    c = 20", "for i in range(10):",
        "    c += 1", "print(a)", "print(b)"])
        self.assertSequenceEqual(input_code_for.get_leaders(input_code_for.get_instructions()), ["t=f=1", "for i in range(10):", "    t = 10", "print(f)"])
        self.assertSequenceEqual(input_code_if.get_leaders(input_code_if.get_instructions()),
                                 ["a = b = 10", "if a > b:", "    h = 12",  "else:", "    c = 20", "if a == 10:",
                                  "    b = 1", "elif a < 10:", "    b = 2", "elif a > 10:", "    b = 3" ])


    def test_basic_block_equal(self):
        self.assertEqual(BasicBlock("if a > b:", 1, BasicBlock.BlockType.IF_THEN),
                         BasicBlock("if a > b:", 1, BasicBlock.BlockType.IF_THEN),
                         "Basic block equal failed")
    def test_basic_block_str(self):
        self.assertEqual(str(BasicBlock("if a > b:", 1,
                            BasicBlock.BlockType.IF_THEN)),
                            "if a > b: 1 BlockType.IF_THEN")

    def test_divide_into_basic_blocks(self):
        self.assertSequenceEqual(input_program.get_basic_blocks(),
                                 [BasicBlock("a = 10", 1, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("if a > b:", 2, BasicBlock.BlockType.IF_THEN),
                                  BasicBlock("    h = 12", 3, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("else:", 4, BasicBlock.BlockType.ELSE),
                                  BasicBlock("    c = 20", 5, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("for i in range(10):", 6, BasicBlock.BlockType.FOR),
                                  BasicBlock("    c += 1", 7, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("print(a)", 8, BasicBlock.BlockType.FUNCTION),
                                  BasicBlock("print(b)", 9, BasicBlock.BlockType.ORDINARY)])
        self.assertSequenceEqual(input_code_block.get_basic_blocks(),
                                 [BasicBlock("a = 10", 1, BasicBlock.BlockType.ORDINARY)])
        self.assertSequenceEqual(input_code_for.get_basic_blocks(),
                                 [BasicBlock("t=f=1", 1, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("for i in range(10):", 2, BasicBlock.BlockType.FOR),
                                  BasicBlock("    t = 10", 3, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("print(f)", 4, BasicBlock.BlockType.ORDINARY)])
        self.assertSequenceEqual(input_code_if.get_basic_blocks(),
                                 [BasicBlock("a = b = 10", 1, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("if a > b:", 2, BasicBlock.BlockType.IF_THEN),
                                  BasicBlock("    h = 12", 3, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("else:", 4, BasicBlock.BlockType.ELSE),
                                  BasicBlock("    c = 20", 5, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("if a == 10:", 6, BasicBlock.BlockType.IF_THEN),
                                  BasicBlock("    b = 1", 7, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("elif a < 10:", 8, BasicBlock.BlockType.ELIF),
                                  BasicBlock("    b = 2", 9, BasicBlock.BlockType.ORDINARY),
                                  BasicBlock("elif a > 10:", 10, BasicBlock.BlockType.ELIF),
                                  BasicBlock("    b = 3", 11, BasicBlock.BlockType.ORDINARY)])
    def test_get_block_stack(self):
        self.assertSequenceEqual(input_program.get_block_stack(),
                                 [["ORDINARY", 1, 0, False],
                                  ["IF_THEN", 2, 0, False],
                                  ["ORDINARY", 3, 0, False],
                                  ["ELSE", 4, 0, False],
                                  ["ORDINARY", 5, 0, False],
                                  ["FOR", 6, 1, False],
                                  ["ORDINARY", 7, 0, False],
                                  ["FUNCTION", 8, 2, False],
                                  ["ORDINARY", 9, 0, False]])
        self.assertSequenceEqual(input_code_block.get_block_stack(),
                                 [["ORDINARY", 1, 0, False]])
        self.assertSequenceEqual(input_code_for.get_block_stack(),[
                                ["ORDINARY", 1, 0, False],
                                ["FOR", 2, 0, False],
                                ["ORDINARY", 3, 0, False],
                                ["ORDINARY", 4, 2, False ]
        ])
        self.assertSequenceEqual(input_code_if.get_block_stack(), [
                                ["ORDINARY", 1, 0, False],
                                ["IF_THEN", 2, 0, False],
                                ["ORDINARY", 3, 0, False],
                                ["ELSE", 4, 0, False],
                                ["ORDINARY", 5, 0, False],
                                ["IF_THEN", 6, 1, False],
                                ["ORDINARY", 7, 0, False],
                                ["ELIF", 8, 0, False],
                                ["ORDINARY", 9, 0, False],
                                ["ELIF", 10, 0, False],
                                ["ORDINARY", 11, 0, False],
        ])
    def test_generate_graph(self):
        # input_program
        graph = {}
        blocks = input_program.get_block_stack()
        for block in blocks:
            graph[block[1]] = []
        graph["START"] = [[blocks[0][1], 1]]
        graph["EXIT"] = [["START", 1]]
        graph[blocks[-1][1]].append(["EXIT", 1])
        graph[blocks[0][1]].append([blocks[1][1], 1])
        graph[blocks[1][1]].append([blocks[3][1], 1])
        graph[blocks[1][1]].append([blocks[2][1], 1])
        graph[blocks[2][1]].append([blocks[5][1], 1])
        graph[blocks[3][1]].append([blocks[4][1], 1])
        graph[blocks[4][1]].append([blocks[5][1], 1])
        graph[blocks[5][1]].append([blocks[6][1], 1])
        graph[blocks[5][1]].append([blocks[7][1], 1])
        graph[blocks[6][1]].append([blocks[5][1], 1])
        graph[blocks[7][1]].append([blocks[8][1], 1])
        cfg = CFG(blocks)
        self.assertEqual(graph, cfg.getGraph())

        # if_test
        graph = {}
        blocks = input_code_if.get_block_stack()
        for block in blocks:
            graph[block[1]] = []

        graph["START"] = [[blocks[0][1], 1]]
        graph["EXIT"] = [["START", 1]]
        graph[blocks[-1][1]].append(["EXIT", 1])
        graph[blocks[0][1]].append([blocks[1][1], 1])
        graph[blocks[1][1]].append([blocks[3][1], 1])
        graph[blocks[1][1]].append([blocks[2][1], 1])
        graph[blocks[2][1]].append([blocks[5][1], 1])
        graph[blocks[3][1]].append([blocks[4][1], 1])
        graph[blocks[4][1]].append([blocks[5][1], 1])
        graph[blocks[5][1]].append([blocks[7][1], 1])
        graph[blocks[5][1]].append([blocks[6][1], 1])
        graph[blocks[7][1]].append([blocks[9][1], 1])
        graph[blocks[7][1]].append([blocks[8][1], 1])
        graph[blocks[9][1]].append([blocks[10][1], 1])
        cfg = CFG(blocks)
        self.assertEqual(graph, cfg.getGraph())

        # test code for
        graph = {}
        blocks = input_code_for.get_block_stack()
        for block in blocks:
            graph[block[1]] = []

        graph["START"] = [[blocks[0][1], 1]]
        graph["EXIT"] = [["START", 1]]
        graph[blocks[-1][1]].append(["EXIT", 1])
        graph[blocks[0][1]].append([blocks[1][1], 1])
        graph[blocks[1][1]].append([blocks[2][1], 1])
        graph[blocks[1][1]].append([blocks[3][1], 1])
        graph[blocks[2][1]].append([blocks[1][1], 1])
        cfg = CFG(blocks)
        self.assertEqual(graph, cfg.getGraph())

        # test code for block
        graph = {}
        blocks = input_code_block.get_block_stack()
        for block in blocks:
            graph[block[1]] = []

        graph["START"] = [[blocks[0][1], 1]]
        graph["EXIT"] = [["START", 1]]
        graph[blocks[-1][1]].append(["EXIT", 1])

        cfg = CFG(blocks)
        self.assertEqual(graph, cfg.getGraph())

    def test_spanning_tree(self):
        blocks = input_program.get_block_stack()
        cfg = CFG(blocks)
        self.assertTrue(cfg.isTree())
        blocks = input_code_if.get_block_stack()
        cfg = CFG(blocks)
        self.assertTrue(cfg.isTree())
        blocks = input_code_for.get_block_stack()
        cfg = CFG(blocks)
        self.assertTrue(cfg.isTree())
        blocks = input_code_block.get_block_stack()
        cfg = CFG(blocks)
        self.assertTrue(cfg.isTree())


if __name__ == '__main__':
    unittest.main()
