import enum


class BasicBlock:
    def __init__(self, lead, b_id, b_type):
        self.lead = lead
        self.instructions = []
        self.id = b_id
        self.type = b_type

    def __eq__(self, other):
        return self.id == other.get_id() and self.type == other.get_type() and self.lead == other.get_lead()

    def __str__(self):
        return self.lead + " " + str(self.id) + " " + str(self.type)
    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def get_instructions(self):
        return self.instructions

    def set_instructions(self, instructions):
        self.instructions = instructions

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_lead(self):
        return self.lead

    def stringify_block(self):
        ret_str = f"# -BEGIN BLOCK id: {self.get_id()} type: {self.get_type().value}\n"
        for instr in self.instructions:
            if instr != "":
                ret_str += instr + "\n"
        ret_str += f"# -END BLOCK id: {self.get_id()}"

        return ret_str

    class BlockType(enum.Enum):
        ROOT = 'root'
        ORDINARY = 'ordinary'
        IF_THEN = 'if then'
        ELSE = 'else'
        ELIF = 'elif'
        FUNCTION = 'function'
        FOR = 'for'
        ENDING = 'ending'
