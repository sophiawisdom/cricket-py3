from abc import abstractmethod

import capstone

from analysis.source import ast2


class Sema():
    def __init__(self, arch):
        self.arch = arch

    def is_jump(self, instruction):
        return capstone.CS_GRP_JUMP in instruction.csinstr.groups or \
            capstone.CS_GRP_RET in instruction.csinstr.groups

    @abstractmethod
    def is_call(self, csinstr):
        assert False

    @abstractmethod
    def call_destination(self, csinstr):
        assert False

    @abstractmethod
    def guess_pointers(self, csinstr, lookahead, min_addr, max_addr):
        assert False

    @abstractmethod
    def looks_like_a_function_start(self, address, instructions):
        assert False

    @abstractmethod
    def is_unconditional_jump(self, instruction):
        assert False

    @abstractmethod
    def is_unconditional_jump_csinstr(self, csinstr):
        assert False

    @abstractmethod
    def is_conditional_jump(self, instruction):
        assert False

    @abstractmethod
    def jump_condition(self, instruction):
        return ast2.Todo() # TODO

    @abstractmethod
    def is_nop(self, instruction):
        assert False

    @abstractmethod
    def is_nop_csinstr(self, instruction):
        assert False

    def is_return(self, instruction):
        return capstone.CS_GRP_RET in instruction.csinstr.groups

    @abstractmethod
    def op_const_value(self, csinstr, op):
        assert False

    def unconditional_jump_destination_csinstr(self, csinstr):
        assert len(csinstr.operands) == 1
        op = csinstr.operands[0]
        if op.type == capstone.CS_OP_IMM:
            return op.imm
        elif op.type == capstone.CS_OP_MEM:
            # Maybe it's a "JMP RIP+0x...", we can calculate the actual value...
            val = self.op_const_value(csinstr, op)
            if val:
                return val
        elif op.type == capstone.CS_OP_REG:
            # "JMP RAX", damn...
            return None
        else:
            # Wut? Ok.
            return None

    def jump_destination(self, instruction):
        if self.is_unconditional_jump(instruction):
            return self.unconditional_jump_destination_csinstr(instruction.csinstr)

        if self.is_conditional_jump(instruction):
            if len(instruction.csinstr.operands) == 1:
                op = instruction.csinstr.operands[0]
                assert op.type == capstone.CS_OP_IMM  # TODO for other types
                return op.imm
            elif len(instruction.csinstr.operands) == 2:
                # "CBZ x0, 0xf00"
                op = instruction.csinstr.operands[1]
                assert op.type == capstone.CS_OP_IMM
                return op.imm
            elif len(instruction.csinstr.operands) == 3:
                # "TBZ x0, 0x10, 0xf00"
                op = instruction.csinstr.operands[2]
                assert op.type == capstone.CS_OP_IMM
                return op.imm

        return None  # e.g. "RET" doesn't have a destination

    @abstractmethod
    def detect_pattern(self, function):
        pass

    @abstractmethod
    def generate_ucode(self, function, instruction):
        assert False

    def function_start_from_addr(self, addr):
        return addr

    @abstractmethod
    def sp_register(self):
        assert False

    @abstractmethod
    def base_register(self):
        assert False

    @abstractmethod
    def pc_register(self):
        assert False

    @abstractmethod
    def retval_location(self, return_type):
        assert False

    @abstractmethod
    def call_arg_locations(self, param_types):
        assert False

    @abstractmethod
    def input_arg_locations(self, param_types):
        assert False

    @abstractmethod
    def detect_stack_variables(self, function):
        assert False

    @abstractmethod
    def get_uregister(self, ufunction, reg_name):
        assert False

    @abstractmethod
    def guess_call_prototype(self, call_instruction, native_register_writes, stack_args_offsets, register_read_after):
        assert False

    @abstractmethod
    def match_switch_jump_points(self, instrs):
        assert False

    @abstractmethod
    def detect_pic(self, function):
        assert False
