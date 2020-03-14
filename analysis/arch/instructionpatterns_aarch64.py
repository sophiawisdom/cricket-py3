import copy
import re

from capstone import *
from capstone.arm64_const import *

from analysis.arch.instructionpattern import InstructionPattern


class AnyObject(object):
    pass


class InstructionPatternsAArch64:
    def __init__(self, arch):
        self.arch = arch

    def create_assembly_instruction_call_constant(self, instr, imm):
        ni = copy.deepcopy(instr)
        ni.addr = instr.addr
        ni.bb = instr.bb
        ni.canonicalsyntax = "bl #0x%x" % (imm)
        ni.csinstr = AnyObject()
        ni.csinstr.id = ARM64_INS_BL
        ni.csinstr.reg_name = instr.csinstr.reg_name
        ni.csinstr.size = 4
        ni.csinstr.groups = [CS_GRP_CALL]
        ni.csinstr.cc = ARM64_CC_INVALID
        op1 = AnyObject()
        op1.type = ARM64_OP_IMM
        op1.imm = imm
        op1.size = 8
        ni.csinstr.operands = [op1]
        return ni

    def create_assembly_instruction_ret(self, instr):
        ni = copy.deepcopy(instr)
        ni.addr = instr.addr
        ni.bb = instr.bb
        ni.canonicalsyntax = "ret"
        ni.csinstr = AnyObject()
        ni.csinstr.id = ARM64_INS_RET
        ni.csinstr.reg_name = instr.csinstr.reg_name
        ni.csinstr.size = 4
        ni.csinstr.operands = []
        ni.csinstr.groups = [CS_GRP_RET]
        ni.csinstr.cc = ARM64_CC_INVALID
        return ni

    def all_instructions_startwith(self, instrs, s):
        for instr in instrs:
            if not instr.canonicalsyntax.startswith(s): return False
        return True

    def all_instructions_match(self, instrs, r):
        for instr in instrs:
            if not re.match(r, instr.canonicalsyntax): return False
        return True

    def detect_pattern(self, function):
        first_instr = function.bbs[0].instructions[0]

        last_instrs = []
        for bb in function.bbs:
            if bb.is_exit:
                last_instr = bb.instructions[-1]
                if len(bb.instructions) >= 2:
                    if last_instr.mnem == "ret": last_instr = bb.instructions[-2]
                    elif last_instr.mnem == "b": last_instr = bb.instructions[-2]
                last_instrs.append(last_instr)

        if first_instr.canonicalsyntax.startswith("sub sp, sp,"):
            if self.all_instructions_startwith(last_instrs, "add sp, sp,"):
                p = InstructionPattern()
                p.matched_instructions = [first_instr] + last_instrs
                p.name = "Make space for local variables"
                return p

        if first_instr.canonicalsyntax.startswith("stp x29, x30, [sp,"):
            if self.all_instructions_startwith(last_instrs, "ldp x29, x30, ["):
                p = InstructionPattern()
                p.matched_instructions = [first_instr] + last_instrs
                p.name = "Save SP and LR"
                return p

        if first_instr.canonicalsyntax.startswith("mov x29, sp"):
            if self.all_instructions_startwith(last_instrs, "mov sp, x29"):
                p = InstructionPattern()
                p.matched_instructions = [first_instr] + last_instrs
                p.name = "Setup FP"
                return p

        if first_instr.canonicalsyntax.startswith("sub sp, sp,"):
            p = InstructionPattern()
            p.matched_instructions = [first_instr]
            p.name = "Make space for local variables"
            return p

        m = re.match("^stp x([0-9]+), x([0-9]+), \\[sp", first_instr.canonicalsyntax)
        if m:
            if self.all_instructions_match(last_instrs, "^ldp x([0-9]+), x([0-9]+), \\[sp"):
                p = InstructionPattern()
                p.matched_instructions = [first_instr] + last_instrs
                p.name = "Save preserved registers"
                return p

        if first_instr.canonicalsyntax.startswith("add x29, sp,"):
            if self.all_instructions_startwith(last_instrs, "sub sp, x29,"):
                p = InstructionPattern()
                p.matched_instructions = [first_instr] + last_instrs
                p.name = "Setup FP"
                return p

        for bb in function.bbs:
            if bb.is_exit:
                very_last_instr = bb.instructions[-1]
                if very_last_instr.csinstr.id == ARM64_INS_B and very_last_instr.csinstr.operands[0].type == ARM64_OP_IMM:
                    imm = very_last_instr.csinstr.operands[0].imm
                    if imm < function.addr or imm > function.addr + function.len:
                        p = InstructionPattern()
                        p.jump_instruction = very_last_instr
                        p.jump_destination = imm
                        p.matched_instructions = [very_last_instr]
                        p.instructions_to_insert = [
                            self.create_assembly_instruction_call_constant(very_last_instr, p.jump_destination),
                            self.create_assembly_instruction_ret(very_last_instr)
                        ]
                        return p

        return None

    def remove_pattern(self, function, cc):
        idx = 0
        for i in cc.matched_instructions:
            bb = i.bb
            idx = bb.instructions.index(i)
            del bb.instructions[idx]

        if len(cc.instructions_to_insert) > 0:
            assert len(cc.matched_instructions) == 1
            for i in cc.instructions_to_insert:
                bb = i.bb
                bb.instructions.insert(idx, i)
                idx += 1
