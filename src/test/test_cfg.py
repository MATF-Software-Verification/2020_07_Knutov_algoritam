from pathlib import Path
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from InputProgram import InputProgram
from blocks.BasicBlock import  BasicBlock
with open(Path('./test_input.py'), 'r') as input_file:
    code = input_file.read()
input_program = InputProgram(code)

with open(Path('./test1.py'), 'r') as input_file:
    code1 = input_file.read()
input_program1 = InputProgram(code1)


class TestCFG(unittest.TestCase):
    def test_make_instractions(self):
        self.assertSequenceEqual(input_program.get_instructions(), [
                                 "a = 10", "b = 2", "if a > b:", "    h = 12", "else:", "    c = 20", "for i in range(10):",
        "    c += 1", "    if c == 1:", "        break", "print(a)", "c = 1"], "test_input")


    def test_leaders(self):
        self.assertSequenceEqual(input_program.get_leaders(input_program.get_instructions()), [
                                 "a = 10", "if a > b:", "    h = 12", "else:", "    c = 20", "for i in range(10):",
        "    c += 1", "    if c == 1:", "        break", "print(a)", "c = 1"])


    def test_basic_block_equal(self):
        self.assertEqual(BasicBlock("if a > b:", 1, BasicBlock.BlockType.IF_THEN),BasicBlock("if a > b:", 1, BasicBlock.BlockType.IF_THEN), "Basic block equal failed")
    def test_basic_block_str(self):
        self.assertEqual(str(BasicBlock("if a > b:", 1, BasicBlock.BlockType.IF_THEN)), "if a > b: 1 BlockType.IF_THEN")

    def test_divide_into_basic_blocks(self):
        self.assertSequenceEqual(input_program.get_basic_blocks(), [BasicBlock("a = 10", 1, BasicBlock.BlockType.ORDINARY), BasicBlock("if a > b:", 2, BasicBlock.BlockType.IF_THEN), BasicBlock("    h = 12", 3, BasicBlock.BlockType.ORDINARY), BasicBlock("else:", 4, BasicBlock.BlockType.ELSE), BasicBlock("    c = 20", 5, BasicBlock.BlockType.ORDINARY), BasicBlock("for i in range(10):", 6, BasicBlock.BlockType.FOR), BasicBlock("    c += 1", 7, BasicBlock.BlockType.ORDINARY), BasicBlock("    if c == 1:", 8, BasicBlock.BlockType.IF_THEN), BasicBlock("        break", 9, BasicBlock.BlockType.ORDINARY), BasicBlock("print(a)", 10, BasicBlock.BlockType.FUNCTION), BasicBlock("c = 1", 11, BasicBlock.BlockType.ORDINARY)])

    def test_generate_graph(self):
        return True


if __name__ == '__main__':
    unittest.main()
