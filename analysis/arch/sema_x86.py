import re

from capstone.x86_const import *

from analysis.arch.cg_x86 import CodeGenX86
from analysis.function import FunctionVariable
from analysis.arch.instructionpatterns_x86 import InstructionPatternsX86
from analysis.types import IntegerType, PointerType, FloatingPointType, VariadicArguments
from analysis.arch.sema import Sema


class SemaX86(Sema):
    def __init__(self, arch):
        Sema.__init__(self, arch)
        self.arch = arch
        self.instruction_patterns = InstructionPatternsX86(arch)

    def is_call(self, csinstr):
        # Treat "CALL $+5; POP EAX" as not a call. Detect "CALL EIP" with encoding E8 00 00 00 00.
        if list(csinstr.bytes) == [0xe8, 0, 0, 0, 0]: return False

        return csinstr.id in [ X86_INS_CALL ]

    def call_destination(self, csinstr):
        assert csinstr.id in [ X86_INS_CALL ]
        if len(csinstr.operands) != 1: return None
        op = csinstr.operands[0]
        if not op.type == X86_OP_IMM: return None
        return op.imm

    def guess_pointers(self, csinstr, lookahead, min_addr, max_addr):
        if csinstr.id == X86_INS_LEA:
            assert csinstr.operands[0].type == X86_OP_REG
            if csinstr.operands[1].type == X86_OP_IMM:
                imm = csinstr.operands[1].imm
                if imm >= min_addr and imm < max_addr:
                    return [imm]
            if csinstr.operands[1].type == X86_OP_MEM:
                if csinstr.operands[1].mem.base != X86_REG_RIP: return []
                if csinstr.operands[1].mem.index != X86_REG_INVALID: return []
                imm = csinstr.address + csinstr.size + csinstr.operands[1].mem.disp
                if imm >= min_addr and imm < max_addr:
                    return [imm]

        return []

    def looks_like_a_function_start(self, address, instructions):
        if len(instructions) < 2: return False  # Non-decodable instructions.

        if instructions[0].mnemonic == "push" and re.match("^(r|e)bp$", instructions[0].op_str):
            if instructions[1].mnemonic == "mov" and re.match("^(r|e)bp, (r|e)sp$", instructions[1].op_str):
                return True

        return False

    def is_unconditional_jump(self, instruction):
        return instruction.csinstr.id == X86_INS_JMP

    def is_unconditional_jump_csinstr(self, csinstr):
        return csinstr.id == X86_INS_JMP

    def is_conditional_jump(self, instruction):
        return instruction.csinstr.id in [  # list from capstone.x86_const
                                            X86_INS_JAE,
                                            X86_INS_JA,
                                            X86_INS_JBE,
                                            X86_INS_JB,
                                            X86_INS_JCXZ,
                                            X86_INS_JECXZ,
                                            X86_INS_JE,
                                            X86_INS_JGE,
                                            X86_INS_JG,
                                            X86_INS_JLE,
                                            X86_INS_JL,
                                            # X86_INS_JMP,
                                            X86_INS_JNE,
                                            X86_INS_JNO,
                                            X86_INS_JNP,
                                            X86_INS_JNS,
                                            X86_INS_JO,
                                            X86_INS_JP,
                                            X86_INS_JRCXZ,
                                            X86_INS_JS,
                                            ]

    def is_nop(self, instruction):
        return instruction.csinstr.id == X86_INS_NOP

    def is_nop_csinstr(self, csinstr):
        return csinstr.id == X86_INS_NOP

    def detect_pattern(self, function):
        return self.instruction_patterns.detect_pattern(function)

    def remove_pattern(self, function, cc):
        self.instruction_patterns.remove_pattern(function, cc)

    def generate_ucode(self, function, instr):
        cg = CodeGenX86(function)
        cg.process_instruction(instr)
        return cg.get_ucode()

    def op_const_value(self, csinstr, op):
        if op.type == X86_OP_MEM:
            if op.mem.base == X86_REG_RIP:
                assert op.mem.index == X86_REG_INVALID  # TODO
                return csinstr.address + op.mem.disp

    def base_register(self):
        if self.arch.bits == 32:
            return "ebp"
        else:
            return "rbp"

    def sp_register(self):
        if self.arch.bits == 32:
            return "esp"
        else:
            return "rsp"

    def pc_register(self):
        if self.arch.bits == 32:
            return "eip"
        else:
            return "rip"

    def retval_location(self, return_type):
        if self.arch.bits == 32:
            return "eax"
        else:
            if isinstance(return_type, FloatingPointType): return "xmm0"
            return "rax"

    def _arg_locations(self, param_types, default_stack_offset):
        result = []
        if self.arch.bits == 32:
            stack_offset = default_stack_offset
            for i in range(0, len(param_types)):
                if isinstance(param_types[i], VariadicArguments):
                    result.append((None, None, None))
                    continue

                result.append((None, None, stack_offset))
                stack_offset += 4
        else:
            int_slots = "rdi,rsi,rdx,rcx,r8,r9".split(",")
            subregs_4 = { "rdi": "edi", "rsi": "esi", "rdx": "edx", "rcx": "ecx", "r8": "r8d", "r9": "r9d" }
            subregs_2 = { "rdi": "di",  "rsi": "si",  "rdx": "dx",  "rcx": "cx",  "r8": "r8w", "r9": "r9w" }
            subregs_1 = { "rdi": "dil", "rsi": "sil", "rdx": "dl",  "rcx": "cl",  "r8": "r8b", "r9": "r9b" }
            fp_slots = "xmm0,xmm1,xmm2,xmm3,xmm4,xmm5,xmm6,xmm7".split(",")
            stack_offset = default_stack_offset
            for i in range(0, len(param_types)):
                if isinstance(param_types[i], IntegerType) or isinstance(param_types[i], PointerType):
                    if len(int_slots) > 0:
                        reg = int_slots.pop(0)
                        subreg = None
                        if param_types[i].byte_size == 8: pass
                        elif param_types[i].byte_size == 4: subreg = subregs_4[reg]
                        elif param_types[i].byte_size == 2: subreg = subregs_2[reg]
                        elif param_types[i].byte_size == 1: subreg = subregs_1[reg]
                        else: assert False

                        result.append((reg, subreg, None))
                        continue
                if isinstance(param_types[i], FloatingPointType):
                    if len(fp_slots) > 0:
                        result.append((fp_slots.pop(0), None, None))
                        continue

                # Otherwise it's on the stack.
                result.append((None, None, stack_offset))
                stack_offset += 8

        return result

    def call_arg_locations(self, param_types):
        return self._arg_locations(param_types, 0)

    def input_arg_locations(self, param_types):
        return self._arg_locations(param_types, 16 if self.arch.bytes() == 8 else 8)

    def looks_like_stack_var_access(self, op):
        if op.type == X86_OP_MEM:
            if op.mem.base == X86_REG_EBP or op.mem.base == X86_REG_RBP:
                if not op.mem.index == X86_REG_INVALID: return False
                if op.mem.disp < 0:
                    return op.mem.disp
            if op.mem.base == X86_REG_ESP or op.mem.base == X86_REG_RSP:
                if not op.mem.index == X86_REG_INVALID: return False
                if op.mem.disp >= 0:
                    return op.mem.disp

        return False

    def detect_stack_frame_size(self, function):
        for instr in function.instructions:
            if instr.csinstr.id == X86_INS_SUB:
                if instr.csinstr.operands[0].type == X86_OP_REG and instr.csinstr.operands[0].reg in [X86_REG_RSP, X86_REG_ESP]:
                    if instr.csinstr.operands[1].type == X86_OP_IMM:
                        function.stack_frame_size = instr.csinstr.operands[1].imm
                        return

    def is_block_flags_stack_item(self, instr):
        if instr.csinstr.id == X86_INS_MOV:
            if instr.csinstr.operands[1].type == X86_OP_IMM:
                if instr.csinstr.operands[1].imm == 0xc2000000:
                    return True

        return False

    def detect_stack_variables(self, function):
        self.detect_stack_frame_size(function)

        indices = set()
        idx_to_instr_map = {}
        for instr in function.instructions:
            for op in instr.csinstr.operands:
                idx = self.looks_like_stack_var_access(op)
                if idx is not False:
                    indices.add(idx)
                    idx_to_instr_map[idx] = instr

        prev_offset = 0
        function.stack_variables = []
        for i in list(reversed(sorted(indices))):
            if i < 0:
                instr = idx_to_instr_map[i]
                block_flags_stack_item = self.is_block_flags_stack_item(instr)

                v = FunctionVariable("var_%x" % -i, -i - prev_offset, "int", "[%s - 0x%x]" % (self.base_register(), -i), i, False, None, None)
                v.block_flags_stack_item = block_flags_stack_item
                function.stack_variables.append(v)
                prev_offset = -i
            else:
                v = FunctionVariable("var_sp_%x" % i, self.arch.bytes(), "long", "[%s + 0x%x]" % (self.sp_register(), i), i, False, None, None)
                v.sp_offset = i
                function.stack_variables.append(v)

    def pc_value_for_addr(self, instr, addr):
        return addr + instr.csinstr.size

    def get_uregister(self, ufunction, reg_name):
        if self.arch.bytes() == 8 and reg_name in CodeGenX86.REGS_X64_8: return ufunction.get_native_register(reg_name)
        if self.arch.bytes() == 8 and reg_name in CodeGenX86.REGS_X64_XMM: return ufunction.get_native_extra_register(reg_name, 16)
        if self.arch.bytes() == 4 and reg_name in CodeGenX86.REGS_X32_4: return ufunction.get_native_register(reg_name)
        assert False

    def guess_call_prototype(self, call_instruction, native_register_writes, stack_args_offsets, register_read_after):
        param_types = []
        if "rdi" in native_register_writes: param_types.append("long")
        if "rsi" in native_register_writes: param_types.append("long")
        if "rdx" in native_register_writes: param_types.append("long")
        if "rcx" in native_register_writes: param_types.append("long")
        return_type = "long"

        return (param_types, return_type)

    def match_switch_jump_points(self, instrs):
        pts = []

        for (idx, instruction) in enumerate(instrs):
            if instrs[idx].csinstr.mnemonic == "add":
                m = re.match("^([re][abcds0-9][xi]?), ([re][abcds0-9][xi]?)$", instrs[idx].csinstr.op_str)
                if m is not None:
                    reg = m.group(1)
                    for idx2 in range(idx, min(idx+3, len(instrs))):
                        if instrs[idx2].csinstr.mnemonic == "jmp":
                            if instrs[idx2].csinstr.op_str == reg:
                                pts.append((instrs[idx2], "rcx"))  # TODO, find real register to switch on
                                break

        return pts

    def detect_pic(self, function):
        pic_register = None
        pic_value = None

        instrs = function.instructions
        for (idx, instruction) in enumerate(instrs):
            if instrs[idx].csinstr.mnemonic == "call":
                a = instrs[idx].csinstr.address + instrs[idx].csinstr.size
                if instrs[idx].csinstr.op_str == ("0x%x" % a):
                    if instrs[idx+1].csinstr.mnemonic == "pop":
                        pic_register = instrs[idx+1].csinstr.op_str
                        pic_value = a
                        # print "PIC register: %s" % pic_register
                        break

        if pic_register is None: return

        function.pic_info = (pic_register, pic_value)

        for (idx, instruction) in enumerate(instrs):
            s = instrs[idx].csinstr.op_str
            instruction.pointer_hints = []
            for m in re.findall("ptr \\[%s \\+ ([a-z0-9*]+ \\+)? (0x[0-9a-f]+)\\]" % pic_register, s):
                offset = m[1]
                a = int(offset, 16)
                a = pic_value + a
                instruction.pointer_hints.append(a)

                # print instruction
                # print "ptr to 0x%x" % a
