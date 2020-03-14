import re

from capstone.arm64_const import *

from analysis.arch.cg_aarch64 import CodeGenAArch64
from analysis.function import FunctionVariable
from analysis.arch.instructionpatterns_aarch64 import InstructionPatternsAArch64
from analysis.arch.sema import Sema
from analysis.types import IntegerType, PointerType, VariadicArguments


class SemaAArch64(Sema):
    def __init__(self, arch):
        Sema.__init__(self, arch)
        self.arch = arch
        self.instruction_patterns = InstructionPatternsAArch64(arch)

    def is_call(self, csinstr):
        # TODO, a tail call can be a "B 0x..."
        return csinstr.id in [ ARM64_INS_BL ]

    def call_destination(self, csinstr):
        assert csinstr.id in [ ARM64_INS_BL ]
        if len(csinstr.operands) != 1: return None
        op = csinstr.operands[0]
        if not op.type == ARM64_OP_IMM: return None
        return op.imm

    def guess_pointers(self, csinstr, lookahead, min_addr, max_addr):
        ret = []
        if csinstr.id in [ARM64_INS_ADR, ARM64_INS_ADRP]:
            assert csinstr.operands[0].type == ARM64_OP_REG
            assert csinstr.operands[1].type == ARM64_OP_IMM
            imm = csinstr.operands[1].imm
            if imm >= min_addr and imm < max_addr:
                ret.append(imm)

            # AArch64: also detect the -O0 "adrp x8, #0x100008000; add x8, x8, #0xc50" as a pointer to 0x100008c50
            if lookahead is not None and len(lookahead) >= 1:
                csinstr2 = lookahead[0]
                if csinstr2.id == ARM64_INS_ADD:
                    if csinstr2.operands[0].type == ARM64_OP_REG \
                            and csinstr2.operands[1].type == ARM64_OP_REG \
                            and csinstr2.operands[2].type == ARM64_OP_IMM \
                            and csinstr2.operands[0].reg == csinstr.operands[0].reg \
                            and csinstr2.operands[0].reg == csinstr2.operands[1].reg:
                        imm2 = imm + csinstr2.operands[2].imm
                        if imm2 >= min_addr and imm2 < max_addr:
                            ret.append(imm2)

        return ret

    def looks_like_a_function_start(self, address, instructions):
        if len(instructions) < 2: return False  # Non-decodable instructions.

        return False  # TODO

    def is_branch(self, instruction):
        return instruction.csinstr.id in [  # list from capstone.arm64_const
            ARM64_INS_B,
            ARM64_INS_BL,
            ARM64_INS_BLR,
            ARM64_INS_BR,
            ARM64_INS_CBZ,
            ARM64_INS_CBNZ,
            ARM64_INS_TBZ,
            ARM64_INS_TBNZ,
        ]

    def is_bl(self, instruction):
        return instruction.csinstr.id == ARM64_INS_BL

    def is_unconditional_jump(self, instruction):
        is_branch = self.is_branch(instruction)
        is_unconditional = instruction.csinstr.cc == ARM64_CC_INVALID or instruction.csinstr.cc == ARM64_CC_AL
        if instruction.csinstr.id in [ARM64_INS_CBZ, ARM64_INS_CBNZ, ARM64_INS_TBZ, ARM64_INS_TBNZ]: is_unconditional = False
        is_bl = self.is_bl(instruction)
        return is_branch and is_unconditional and not is_bl

    def is_unconditional_jump_csinstr(self, csinstr):
        is_unconditional = csinstr.cc == ARM64_CC_INVALID or csinstr.cc == ARM64_CC_AL
        return is_unconditional and csinstr.id in [ARM64_INS_B,
            ARM64_INS_BLR,
            ARM64_INS_BR]

    def is_conditional_jump(self, instruction):
        is_branch = self.is_branch(instruction)
        is_unconditional = instruction.csinstr.cc == ARM64_CC_INVALID or instruction.csinstr.cc == ARM64_CC_AL
        if instruction.csinstr.id in [ARM64_INS_CBZ, ARM64_INS_CBNZ, ARM64_INS_TBZ, ARM64_INS_TBNZ]: is_unconditional = False
        return is_branch and not is_unconditional

    def is_return(self, instruction):
        return instruction.csinstr.id == ARM64_INS_RET

    def is_nop(self, instruction):
        return instruction.csinstr.id == ARM64_INS_NOP

    def is_nop_csinstr(self, csinstr):
        return csinstr.id == ARM64_INS_NOP

    def retval_location(self, return_type):
        return "x0"

    def _arg_locations(self, param_types):
        result = []
        int_slots = "x0,x1,x2,x3,x4,x5,x6,x7".split(",")
        stack_offset = 0
        for i in range(0, len(param_types)):
            if isinstance(param_types[i], IntegerType) or isinstance(param_types[i], PointerType):
                if len(int_slots) > 0:
                    reg = int_slots.pop(0)
                    subreg = None
                    result.append((reg, subreg, None))
                    continue

            if isinstance(param_types[i], VariadicArguments):
                int_slots = []
                result.append((None, None, None))
                continue

            # Otherwise it's on the stack.
            result.append((None, None, stack_offset))
            stack_offset += 8

        return result

    def call_arg_locations(self, param_types):
        return self._arg_locations(param_types)

    def input_arg_locations(self, param_types):
        return self._arg_locations(param_types)

    def looks_like_stack_var_access(self, instr):
        base = None

        if instr.csinstr.id in [ARM64_INS_STR, ARM64_INS_STUR, ARM64_INS_LDR, ARM64_INS_LDUR, ARM64_INS_STRB, ARM64_INS_LDRB, ARM64_INS_LDRSW]:
            if len(instr.csinstr.operands) == 2:
                ptr_op = instr.csinstr.operands[1]
                if ptr_op.type == ARM64_OP_MEM:
                    base = ptr_op.mem.base
                    index = ptr_op.mem.disp
                elif ptr_op.type == ARM64_OP_REG:
                    base = ptr_op.reg
                    index = 0
            if len(instr.csinstr.operands) == 3:
                base_op = instr.csinstr.operands[1]
                index_op = instr.csinstr.operands[2]
                if base_op.type == ARM64_OP_REG and index_op.type == ARM64_OP_IMM:
                    base = base_op.reg
                    index = index_op.imm

        if base == ARM64_REG_X29:
            if index < 0:
                return index
        if base == ARM64_REG_SP:
            if index >= 0:
                return index

        return None

    def detect_stack_variables(self, function):
        indices = set()
        for instr in function.instructions:
            idx = self.looks_like_stack_var_access(instr)
            if idx is not None: indices.add(idx)

        prev_offset = 4
        function.stack_variables = []
        for i in list(reversed(sorted(indices))):
            if i < 0:
                v = FunctionVariable("var_%x" % -i, -i - prev_offset, "int", "[%s - 0x%x]" % (self.base_register(), -i), i, False, None, None)
                function.stack_variables.append(v)
                prev_offset = -i
            else:
                v = FunctionVariable("var_sp_%x" % i, 8, "long", "[sp + 0x%x]" %i, i, False, None, None)
                v.sp_offset = i
                function.stack_variables.append(v)

    def generate_ucode(self, function, instr):
        cg = CodeGenAArch64(function)
        cg.process_instruction(instr)
        return cg.get_ucode()

    def base_register(self):
        return "x29"

    def pc_register(self):
        return "pc"

    def sp_register(self):
        return "sp"

    def get_uregister(self, ufunction, reg_name):
        if reg_name in "x0,x1,x2,x3,x4,x5,x6,x7": return ufunction.get_native_register(reg_name)
        assert False

    def detect_pattern(self, function):
        return self.instruction_patterns.detect_pattern(function)

    def remove_pattern(self, function, cc):
        self.instruction_patterns.remove_pattern(function, cc)

    def match_switch_jump_points(self, instrs):
        pts = []

        for (idx, instruction) in enumerate(instrs):
            if instrs[idx].csinstr.mnemonic == "add":
                m = re.match("^(x[0-9]+), (x[0-9]+), (x[0-9]+)$", instrs[idx].csinstr.op_str)
                if m is not None:
                    reg1 = m.group(1)
                    reg2 = m.group(1)
                    reg3 = m.group(1)
                    if reg1 == reg2:
                        for idx2 in range(idx, min(idx+3, len(instrs))):
                            if instrs[idx2].csinstr.mnemonic == "br":
                                if instrs[idx2].csinstr.op_str == reg1:
                                    pts.append((instrs[idx2], "r8"))  # TODO, find real register to switch on
                                    break

        return pts

    def detect_pic(self, function):
        return
