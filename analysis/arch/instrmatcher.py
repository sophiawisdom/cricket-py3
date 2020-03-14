from capstone import *




class InstrMatcher:
    @staticmethod
    def match(instr, pattern):
        if not hasattr(instr, "csinstr"): return False

        if instr.csinstr.id != pattern.id: return False
        if len(instr.csinstr.operands) != len(pattern.ops): return False
        for idx in range(0, len(pattern.ops)):
            if instr.csinstr.operands[idx].type == CS_OP_REG:
                if pattern.ops[idx].type != "reg": return False
                if pattern.ops[idx].reg == None: continue # ANY_REG
                if instr.csinstr.operands[idx].reg != pattern.ops[idx].reg: return False
            elif instr.csinstr.operands[idx].type == CS_OP_IMM:
                if pattern.ops[idx].type != "imm": return False
                if pattern.ops[idx].imm == None: continue # ANY_IMM
                if instr.csinstr.operands[idx].imm != pattern.ops[idx].imm: return False
            else:
                return False

        return True
