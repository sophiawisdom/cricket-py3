import capstone
from capstone.arm_const import *

from analysis.arch.sema import Sema


class SemaArmV7(Sema):
    def __init__(self, arch):
        Sema.__init__(self, arch)
        self.arch = arch

    def is_branch(self, instruction):
        # We only do THUMB now
        assert ARM_GRP_THUMB in instruction.csinstr.groups \
            or ARM_GRP_THUMB2 in instruction.csinstr.groups


        assert instruction.csinstr.cc != ARM_CC_INVALID

        return instruction.csinstr.id in [  # list from capstone.arm_const
            ARM_INS_BL,
            ARM_INS_BLX,
            ARM_INS_BX,
            ARM_INS_BXJ,
            ARM_INS_B,
            # TODO CMBZ Compare and Branch on Zero, etc.
        ]

    def is_branch_lr(self, instruction):
        is_branch = self.is_branch(instruction)

        # Treat "bx lr" as a return
        if is_branch:
            assert len(instruction.csinstr.operands) == 1
            op = instruction.csinstr.operands[0]
            if op.type == capstone.CS_OP_REG:
                if op.reg == ARM_REG_LR:
                    return True
        return False

    def is_blx(self, instruction):
        return instruction.csinstr.id == ARM_INS_BLX

    def is_unconditional_jump(self, instruction):
        is_branch_always = self.is_branch(instruction) and instruction.csinstr.cc == ARM_CC_AL
        is_branch_lr = self.is_branch_lr(instruction)
        is_blx = self.is_blx(instruction)
        return is_branch_always and not is_branch_lr and not is_blx

    def is_conditional_jump(self, instruction):
        # We only do THUMB now
        assert ARM_GRP_THUMB in instruction.csinstr.groups \
            or ARM_GRP_THUMB2 in instruction.csinstr.groups

        assert instruction.csinstr.cc != ARM_CC_INVALID

        return self.is_branch(instruction) and instruction.csinstr.cc != ARM_CC_AL

    def is_return(self, instruction):
        if capstone.CS_GRP_RET in instruction.csinstr.groups:
            return True

        # Treat a "POP PC" as a return
        if instruction.csinstr.id == ARM_INS_POP:
            for op in instruction.csinstr.operands:
                if op.type == ARM_OP_REG:
                    if op.reg == ARM_REG_PC:
                        return True

        is_branch_always = self.is_branch(instruction) and instruction.csinstr.cc == ARM_CC_AL
        is_branch_lr = self.is_branch_lr(instruction)
        return is_branch_always and is_branch_lr

    def is_nop(self, instruction):
        return instruction.csinstr.id == ARM_INS_NOP

    def function_start_from_addr(self, addr):
        return addr & ~(0x1)

    def retval_location(self):
        return "r0"

    def arg_location(self, index, offset, variadic_index=-1):
        regs = "r0,r1,r2,r3".split(",")
        if index < 4: return regs[index]
        n = ((index-4)*4)
        return ("[sp + 0x%x]" % n, n)

    def detect_stack_variables(self, function):
        function.stack_variables = []
        # TODO

    def generate_ucode(self, function, instr):
        assert False
