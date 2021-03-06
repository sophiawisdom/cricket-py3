import copy

from capstone import CS_GRP_RET, CS_GRP_CALL

from capstone.x86_const import *

from analysis.arch.instrmatcher import InstrMatcher
from analysis.arch.instrmatcherx86 import X86
from analysis.arch.instructionpattern import *


class AnyObject(object):
    pass

class InstructionPatternsX86:
    def __init__(self, arch):
        self.arch = arch

    def detect_cc_setup_frame_pointer(self, function):
        if self.arch.bits == 32:
            p1 = X86.PUSH(X86.EBP)
            p2 = X86.MOV(X86.EBP, X86.ESP)
            p3 = X86.POP(X86.EBP)
        else:
            p1 = X86.PUSH(X86.RBP)
            p2 = X86.MOV(X86.RBP, X86.RSP)
            p3 = X86.POP(X86.RBP)

        assert len(function.get_entry_bbs()) == 1

        first_bb = function.bbs[0]
        if len(first_bb.instructions) < 2: return None
        i1, i2 = first_bb.instructions[0], first_bb.instructions[1]

        if InstrMatcher.match(i1, p1) and InstrMatcher.match(i2, p2):
            # Found the prologue.
            bbs = function.get_exit_bbs()
            prologue_instructions = [i1, i2]
            epilogue_instructions = []
            found_in_all_exit_bbs = True
            for bb in bbs:
                assert len(bb.instructions) > 0
                if len(bb.instructions) < 2:
                    found_in_all_exit_bbs = False
                    break
                last_instr = bb.instructions[-2] # Last is "RET", one before is "POP EBP"
                # Can we find the epilogue in all exit bbs?
                if not InstrMatcher.match(last_instr, p3):
                    found_in_all_exit_bbs = False
                    break
                else:
                    epilogue_instructions.append(last_instr)

            if found_in_all_exit_bbs:
                cc = InstructionPatternSetupFramePointer(function)
                cc.setup_instructions = prologue_instructions
                cc.teardown_instructions = epilogue_instructions
                cc.matched_instructions = prologue_instructions + epilogue_instructions
                return cc

        return None


    def detect_cc_save_registers(self, function):
        # X86.PUSH(X86.EAX)
        # TODO
        pass

    def detect_cc_pic_base_register(self, function):
        if self.arch.bits != 32: return None
        assert len(function.get_entry_bbs()) == 1
        first_bb = function.bbs[0]
        if len(first_bb.instructions) < 2: return None
        i1, i2 = first_bb.instructions[0], first_bb.instructions[1]

        p1 = X86.CALL(X86.IMM(i2.addr))
        p2 = X86.POP(X86.ANY_REG)

        if InstrMatcher.match(i1, p1) and InstrMatcher.match(i2, p2):
            cc = InstructionPatternGetPICBase(function)
            cc.setup_instructions = [i1, i2]
            cc.teardown_instructions = []
            cc.register = i2.csinstr.operands[0].reg
            cc.pc_value = i2.addr
            cc.matched_instructions = cc.setup_instructions
            return cc

        if len(first_bb.instructions) < 3: return None
        i0, i1, i2 = first_bb.instructions[0], first_bb.instructions[1], first_bb.instructions[2]

        p0 = X86.PUSH(X86.EAX)
        p1 = X86.CALL(X86.IMM(i2.addr))
        p2 = X86.POP(X86.EAX)
        p3 = X86.ADD(X86.ESP, X86.IMM(4))
        if InstrMatcher.match(i0, p0) and InstrMatcher.match(i1, p1) and InstrMatcher.match(i2, p2):
            bbs = function.get_exit_bbs()
            prologue_instructions = [i0, i1, i2]
            epilogue_instructions = []
            found_in_all_exit_bbs = True
            for bb in bbs:
                assert len(bb.instructions) > 0
                last_instr = bb.instructions[len(bb.instructions) - 1]
                # Can we find the epilogue in all exit bbs?
                if not InstrMatcher.match(last_instr, p3):
                    found_in_all_exit_bbs = False
                    break
                else:
                    epilogue_instructions.append(last_instr)

            if found_in_all_exit_bbs:
                cc = InstructionPatternGetPICBase(function)
                cc.setup_instructions = prologue_instructions
                cc.teardown_instructions = epilogue_instructions
                cc.register = X86_REG_EAX
                cc.pc_value = i2.addr
                cc.matched_instructions = prologue_instructions + epilogue_instructions
                return cc

        return None

    def detect_cc_push_pop(self, function):
        assert len(function.get_entry_bbs()) == 1
        first_bb = function.bbs[0]
        if len(first_bb.instructions) < 1: return None

        i1 = first_bb.instructions[0]
        p1 = X86.PUSH(X86.ANY_REG)
        if InstrMatcher.match(i1, p1):
            p2 = X86.POP(X86.REG(i1.csinstr.operands[0].reg))
            bbs = function.get_exit_bbs()
            prologue_instructions = [i1]
            epilogue_instructions = []
            found_in_all_exit_bbs = True
            for bb in bbs:
                assert len(bb.instructions) > 0
                if len(bb.instructions) < 2:
                    found_in_all_exit_bbs = False
                    break
                last_instr = bb.instructions[-2] # Last is "RET", one before is "POP ..."
                # Can we find the epilogue in all exit bbs?
                if not InstrMatcher.match(last_instr, p2):
                    found_in_all_exit_bbs = False
                    break
                else:
                    epilogue_instructions.append(last_instr)

            if not found_in_all_exit_bbs:
                # or maybe ADD RSP, 8?
                if self.arch.bits == 32: reg = X86.ESP
                elif self.arch.bits == 64: reg = X86.RSP
                else: assert False
                p2 = X86.ADD(reg, X86.IMM(self.arch.bits / 8))
                prologue_instructions = [i1]
                epilogue_instructions = []
                found_in_all_exit_bbs = True
                for bb in bbs:
                    assert len(bb.instructions) > 0
                    if len(bb.instructions) < 2:
                        found_in_all_exit_bbs = False
                        break
                    last_instr = bb.instructions[-2] # Last is "RET", one before is "POP ..."
                    # Can we find the epilogue in all exit bbs?
                    if not InstrMatcher.match(last_instr, p2):
                        found_in_all_exit_bbs = False
                        break
                    else:
                        epilogue_instructions.append(last_instr)

            if found_in_all_exit_bbs:
                cc = InstructionPatternPushPop(function)
                cc.setup_instructions = prologue_instructions
                cc.teardown_instructions = epilogue_instructions
                cc.register = i1.csinstr.operands[0].reg
                cc.matched_instructions = prologue_instructions + epilogue_instructions
                return cc

        return None

    def detect_cc_sub_add_esp(self, function):
        if self.arch.bits == 32: reg = X86.ESP
        elif self.arch.bits == 64: reg = X86.RSP
        else: assert False

        assert len(function.get_entry_bbs()) == 1
        first_bb = function.bbs[0]
        if len(first_bb.instructions) < 1: return None

        i1 = first_bb.instructions[0]
        p1 = X86.SUB(reg, X86.ANY_IMM)
        if InstrMatcher.match(i1, p1):
            stack_frame_size = i1.csinstr.operands[1].imm
            p2 = X86.ADD(reg, X86.IMM(stack_frame_size))
            bbs = function.get_exit_bbs()
            prologue_instructions = [i1]
            epilogue_instructions = []
            found_in_all_exit_bbs = True
            for bb in bbs:
                assert len(bb.instructions) > 0
                if len(bb.instructions) < 2:
                    found_in_all_exit_bbs = False
                    break
                last_instr = bb.instructions[-2] # Last is RET, one before is "ADD ESP, ..."
                # Can we find the epilogue in all exit bbs?
                if not InstrMatcher.match(last_instr, p2):
                    found_in_all_exit_bbs = False
                    break
                else:
                    epilogue_instructions.append(last_instr)

            if found_in_all_exit_bbs:
                cc = InstructionPatternSubAddEsp(function)
                cc.setup_instructions = prologue_instructions
                cc.teardown_instructions = epilogue_instructions
                cc.register = i1.csinstr.operands[0].reg
                cc.matched_instructions = prologue_instructions + epilogue_instructions
                return cc

        return None

    def detect_cc_stack_check(self, function):
        for bb in function.bbs:
            if bb.is_exit and len(bb.instructions) == 1:
                instr = bb.instructions[0]
                if instr.csinstr.id == X86_INS_CALL and instr.csinstr.operands[0].type == X86_OP_IMM:
                    imm = instr.csinstr.operands[0].imm
                    if imm in list(function.binary.stubs.keys()):
                        stub = function.binary.stubs[imm]
                        if stub == "___stack_chk_fail":
                            assert len(bb.preds) == 1
                            branch_bb = list(bb.preds)[0]
                            cc = InstructionPatternStackCheck(function)
                            cc.check_failed_bb = bb
                            cc.branch_bb = branch_bb
                            cc.matched_instructions = [instr, branch_bb.instructions[-1]]
                            return cc

        return None

    def detect_cc_tail_call(self, function):
        for bb in function.bbs:
            if bb.is_exit:
                instr = bb.instructions[-1]
                if instr.csinstr.id == X86_INS_JMP and instr.csinstr.operands[0].type == X86_OP_IMM:
                    imm = instr.csinstr.operands[0].imm
                    if imm < function.addr or imm > function.addr + function.len:
                        cc = InstructionPatternTailCall(function)
                        cc.jump_instruction = instr
                        cc.jump_destination = imm
                        cc.indirect = False
                        cc.matched_instructions = [instr]
                        return cc
                # TODO: jmp [rip+0xf00] should be "CALL dword ptr [0xb00]" and not "CALL 0xb00"
                if instr.csinstr.id == X86_INS_JMP and instr.csinstr.operands[0].type == X86_OP_MEM:
                    if instr.csinstr.operands[0].mem.base == X86_REG_RIP and instr.csinstr.operands[0].mem.index == X86_REG_INVALID:
                        imm = self.arch.sema.pc_value_for_addr(instr, instr.addr) + instr.csinstr.operands[0].mem.disp
                        if imm < function.addr or imm > function.addr + function.len:
                            cc = InstructionPatternTailCall(function)
                            cc.jump_instruction = instr
                            cc.jump_destination = imm
                            cc.indirect = True
                            cc.matched_instructions = [instr]
                            return cc

        return None

    def detect_pattern(self, function):
        cc = self.detect_cc_setup_frame_pointer(function)
        if cc: return cc

        cc = self.detect_cc_pic_base_register(function)
        if cc: return cc

        cc = self.detect_cc_push_pop(function)
        if cc: return cc

        cc = self.detect_cc_sub_add_esp(function)
        if cc: return cc

        cc = self.detect_cc_stack_check(function)
        if cc: return cc

        cc = self.detect_cc_tail_call(function)
        if cc: return cc

        return None

    def create_assembly_instruction_mov_constant(self, instr, reg, val):
        ni = copy.deepcopy(instr)
        ni.canonicalsyntax = "mov %s, 0x%x" % (instr.csinstr.reg_name(reg), val)
        ni.csinstr = AnyObject()
        ni.csinstr.id = X86_INS_MOV
        ni.csinstr.reg_name = instr.csinstr.reg_name
        ni.csinstr.size = 1 + self.arch.bits / 8
        ni.csinstr.groups = []
        op1 = AnyObject()
        op1.type = X86_OP_REG
        op1.reg = reg
        op1.size = self.arch.bits / 8
        op2 = AnyObject()
        op2.type = X86_OP_IMM
        op2.imm = val
        op2.size = self.arch.bits / 8
        ni.csinstr.operands = [op1, op2]
        return ni

    def create_assembly_instruction_call_constant(self, instr, imm, indirect):
        ni = copy.deepcopy(instr)
        if not indirect:
            ni.canonicalsyntax = "call 0x%x" % (imm)
        else:
            ni.canonicalsyntax = "call %s ptr [0x%x]" % ("dword" if self.arch.bits == 32 else "qword", imm)
        ni.csinstr = AnyObject()
        ni.csinstr.id = X86_INS_CALL
        ni.csinstr.reg_name = instr.csinstr.reg_name
        ni.csinstr.size = 1 + self.arch.bits / 8
        ni.csinstr.groups = [CS_GRP_CALL]
        op1 = AnyObject()
        if not indirect:
            op1.type = X86_OP_IMM
            op1.imm = imm
        else:
            op1.type = X86_OP_MEM
            op1.mem = AnyObject()
            op1.mem.base = X86_REG_INVALID
            op1.mem.index = X86_REG_INVALID
            op1.mem.disp = imm
        op1.size = self.arch.bits / 8
        ni.csinstr.operands = [op1]
        return ni

    def create_assembly_instruction_ret(self, instr):
        ni = copy.deepcopy(instr)
        ni.canonicalsyntax = "ret"
        ni.csinstr = AnyObject()
        ni.csinstr.id = X86_INS_RET
        ni.csinstr.reg_name = instr.csinstr.reg_name
        ni.csinstr.size = 1
        ni.csinstr.operands = []
        ni.csinstr.groups = [CS_GRP_RET]
        return ni

    def remove_pattern(self, function, cc):
        if isinstance(cc, InstructionPatternSetupFramePointer):
            for instr in cc.setup_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            for instr in cc.teardown_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            return

        if isinstance(cc, InstructionPatternGetPICBase):
            place_to_insert = cc.setup_instructions[0]
            bb = place_to_insert.bb
            idx = bb.instructions.index(place_to_insert)

            instr = self.create_assembly_instruction_mov_constant(place_to_insert, cc.register, cc.pc_value)
            #instr = UCodeMov(UCodeConstant(cc.pc_value), self.get_uregister(place_to_insert, cc.register))
            instr.addr = place_to_insert.addr
            instr.bb = bb
            bb.instructions.insert(idx, instr)

            for instr in cc.setup_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            for instr in cc.teardown_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            return

        if isinstance(cc, InstructionPatternPushPop):
            for instr in cc.setup_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            for instr in cc.teardown_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            return

        if isinstance(cc, InstructionPatternSubAddEsp):
            for instr in cc.setup_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            for instr in cc.teardown_instructions:
                bb = instr.bb
                bb.instructions = [i for i in bb.instructions if i != instr]
            return

        if isinstance(cc, InstructionPatternStackCheck):
            bb_idx = function.bbs.index(cc.check_failed_bb)
            del function.bbs[bb_idx]
            del cc.branch_bb.instructions[-1]
            cc.branch_bb.succs.remove(cc.check_failed_bb)
            # TODO: renumber BBs
            return

        if isinstance(cc, InstructionPatternTailCall):
            place_to_insert = cc.jump_instruction
            bb = place_to_insert.bb
            instr = self.create_assembly_instruction_call_constant(place_to_insert, cc.jump_destination, cc.indirect)
            instr2 = self.create_assembly_instruction_ret(place_to_insert)
            idx = bb.instructions.index(place_to_insert)
            bb.instructions.insert(idx, instr)
            bb.instructions.insert(idx + 1, instr2)
            instr.bb = bb
            instr2.bb = bb
            bb.instructions = [i for i in bb.instructions if i != cc.jump_instruction]
            return

        # Unknown CC.
        assert False
