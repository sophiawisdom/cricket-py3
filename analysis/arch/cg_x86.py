from capstone.x86_const import *

from analysis.asm.assembly import AssemblyInstruction
from analysis.types import VoidType
from analysis.ucode.ucode import *


class OperandValue:
    TYPE_REG = 1
    TYPE_CONSTANT = 2
    TYPE_POINTER = 3

    def __init__(self, type, size, value):
        self.type = type
        self.size = size
        self.value = value


class CodeGenX86:

    def __init__(self, function):
        self.sema = function.arch.sema
        self.arch = function.arch
        self.function = function
        self.ucode = []
        self.bit_size = function.arch.bits
        self.byte_size = function.arch.bits / 8

    def get_native_register_or_subregister_by_name(self, instr, size, reg_name):
        if self.byte_size == 8 and reg_name in self.REGS_X64_8: return self.function.ufunction.get_native_register(reg_name)
        if self.byte_size == 8 and reg_name in self.REGS_X64_XMM: return self.function.ufunction.get_native_extra_register(reg_name, 16)
        if self.byte_size == 4 and reg_name in self.REGS_X32_4: return self.function.ufunction.get_native_register(reg_name)
        return self.function.ufunction.get_native_subregister(reg_name, size)

    def get_native_register_or_subregister(self, instr, size, reg_num):
        name = instr.csinstr.reg_name(reg_num)
        return self.get_native_register_or_subregister_by_name(instr, size, name)

    def emit(self, uinstr, instr):
        uinstr.addr = instr.addr
        uinstr.pc_value = self.sema.pc_value_for_addr(instr, instr.addr)
        self.ucode.append(uinstr)
        return uinstr

    def ucode_for_operand(self, instr, op, size=None):
        if size is None: size = op.size

        if op.type == X86_OP_IMM:
            const_size = size
            return OperandValue(OperandValue.TYPE_CONSTANT, const_size, UCodeConstant(const_size, op.imm))
        if op.type == X86_OP_REG:
            assert op.size == size
            return OperandValue(OperandValue.TYPE_REG, op.size, self.get_native_register_or_subregister(instr, op.size, op.reg))
        if op.type == X86_OP_MEM:
            if op.mem.base == X86_REG_INVALID and op.mem.index == X86_REG_INVALID:
                return OperandValue(OperandValue.TYPE_POINTER, op.size, UCodeConstant(self.byte_size, op.mem.disp))
            base_reg = None
            if op.mem.base != X86_REG_INVALID:
                base_reg = self.get_native_register_or_subregister(instr, self.byte_size, op.mem.base)
            disp = op.mem.disp
            if op.mem.index == X86_REG_INVALID:
                t = self.function.ufunction.create_temp_register(self.byte_size)
                self.emit(UCodeAdd(self.byte_size, base_reg, UCodeConstant(self.byte_size, disp), t), instr)
                return OperandValue(OperandValue.TYPE_POINTER, op.size, t)

            index_reg = self.get_native_register_or_subregister(instr, self.byte_size, op.mem.index)

            t1 = self.function.ufunction.create_temp_register(self.byte_size)
            t2 = self.function.ufunction.create_temp_register(self.byte_size)
            t3 = self.function.ufunction.create_temp_register(self.byte_size)
            self.emit(UCodeMul(self.byte_size, index_reg, UCodeConstant(self.byte_size, op.mem.scale), t1), instr)
            if base_reg is not None:
                self.emit(UCodeAdd(self.byte_size, base_reg, t1, t2), instr)
            else:
                t2 = t1
            self.emit(UCodeAdd(self.byte_size, t2, UCodeConstant(self.byte_size, disp), t3), instr)
            return OperandValue(OperandValue.TYPE_POINTER, op.size, t3)

    def ucode_for_operand_load(self, instr, op, size=None):
        if size is None: size = op.size

        v = self.ucode_for_operand(instr, op, size)
        if v.type == OperandValue.TYPE_CONSTANT: return v.value
        elif v.type == OperandValue.TYPE_REG:
            src = self.subregister_load(instr, v.size, v.value)
            return src
        assert v.type == OperandValue.TYPE_POINTER
        t = self.function.ufunction.create_temp_register(v.size)
        uinstr = self.emit(UCodeLoad(v.size, v.value, t), instr)
        return t

    def ucode_for_operand_store(self, instr, op, value_to_store):
        v = self.ucode_for_operand(instr, op)
        if v.type == OperandValue.TYPE_REG:
            r = v.value
            if v.size > value_to_store.size:
                t = self.function.ufunction.create_temp_register(r.size)
                self.emit(UCodeExtend(r.size, value_to_store, t), instr)
                value_to_store = t
            elif v.size < value_to_store.size:
                t = self.function.ufunction.create_temp_register(r.size)
                self.emit(UCodeTruncate(r.size, value_to_store, t), instr)
                value_to_store = t
            uinstr = self.emit(UCodeMov(v.size, value_to_store, r), instr)
            self.subregister_store(instr, uinstr)
            return

        assert v.type == OperandValue.TYPE_POINTER
        if v.size > value_to_store.size:
            t = self.function.ufunction.create_temp_register(v.size)
            self.emit(UCodeExtend(v.size, value_to_store, t), instr)
            value_to_store = t
        elif v.size < value_to_store.size:
            t = self.function.ufunction.create_temp_register(v.size)
            self.emit(UCodeTruncate(v.size, value_to_store, t), instr)
            value_to_store = t
        self.emit(UCodeStore(v.size, v.value, value_to_store), instr)

    REGS_X64_8 = "rax,rbx,rcx,rdx,rdi,rsi,rbp,rsp,r8,r9,r10,r11,r12,r13,r14,r15".split(",")
    REGS_X64_4 = "eax,ebx,ecx,edx,edi,esi,ebp,esp,r8d,r9d,r10d,r11d,r12d,r13d,r14d,r15d".split(",")
    REGS_X64_2 = "ax,bx,cx,dx,di,si,sp,bp,r8w,r9w,r10w,r11w,r12w,r13w,r14w,r15w".split(",")
    REGS_X64_1 = "al,bl,cl,dl,dil,sil,bpl,spl,r8b,r9b,r10b,r11b,r12b,r13b,r14b,r15b".split(",")
    REGS_X64_1H = "ah,bh,ch,dh".split(",")

    REGS_X32_4 = "eax,ebx,ecx,edx,edi,esi,ebp,esp".split(",")
    REGS_X32_2 = "ax,bx,cx,dx,di,si,sp,bp".split(",")
    REGS_X32_1 = "al,bl,cl,dl".split(",")

    REGS_X64_XMM = "xmm0,xmm1,xmm2,xmm3,xmm4,xmm5,xmm6,xmm7".split(",")
    REGS_X32_XMM = "xmm0,xmm1,xmm2,xmm3,xmm4,xmm5,xmm6,xmm7".split(",")

    def subregister_load(self, instr, size, reg):
        assert isinstance(reg, UCodeRegister)
        if self.byte_size == 8:
            if reg.name in self.REGS_X64_8:
                return reg
            if reg.name in self.REGS_X64_XMM:
                return reg

            if reg.name in self.REGS_X64_4:
                idx = self.REGS_X64_4.index(reg.name)
            elif reg.name in self.REGS_X64_2:
                idx = self.REGS_X64_2.index(reg.name)
            elif reg.name in self.REGS_X64_1:
                idx = self.REGS_X64_1.index(reg.name)
            elif reg.name in self.REGS_X64_1H:
                idx = self.REGS_X64_1H.index(reg.name)
                src = self.get_native_register_or_subregister_by_name(instr, 8, self.REGS_X64_8[idx])
                shifted = self.function.ufunction.create_temp_register(8)
                self.emit(UCodeShiftRight(size, src, UCodeConstant(8, 8), shifted), instr)
                dst2 = self.function.ufunction.create_temp_register(size)
                self.emit(UCodeTruncate(size, shifted, dst2), instr)
                return dst2
            else:
                assert False, "Invalid register size/name."

            src = self.get_native_register_or_subregister_by_name(instr, 8, self.REGS_X64_8[idx])
            dst = self.function.ufunction.create_temp_register(size)
            self.emit(UCodeTruncate(size, src, dst), instr)
            return dst

        else:  # self.byte_size == 4
            if reg.name in self.REGS_X32_4:
                return reg
            if reg.name in self.REGS_X32_XMM:
                return reg

            if reg.name in self.REGS_X32_2:
                idx = self.REGS_X32_2.index(reg.name)
            elif reg.name in self.REGS_X32_1:
                idx = self.REGS_X32_1.index(reg.name)
            else:
                assert False, "Invalid register size/name."

            src = self.get_native_register_or_subregister_by_name(instr, 4, self.REGS_X32_4[idx])
            dst = self.function.ufunction.create_temp_register(size)
            self.emit(UCodeTruncate(size, src, dst), instr)
            return dst

    def subregister_store(self, instr, uinstr):
        if self.byte_size == 8:
            if uinstr.size == 16: return  # XMM
            if uinstr.size == 8: return

            if uinstr.size == 4:  # Special case for 4-byte write, because the upper half of the register is set to 0.
                reg = uinstr.destination()
                assert isinstance(reg, UCodeRegister)
                idx = self.REGS_X64_4.index(reg.name)
                full_reg = self.get_native_register_or_subregister_by_name(instr, 8, self.REGS_X64_8[idx])
                self.emit(UCodeExtend(8, reg, full_reg), instr)
                return

            reg = uinstr.destination()
            assert isinstance(reg, UCodeRegister)
            if uinstr.size == 2:
                idx = self.REGS_X64_2.index(reg.name)
                const = 0xffffffffffff0000
            elif uinstr.size == 1:
                idx = self.REGS_X64_1.index(reg.name)
                const = 0xffffffffffffff00
            else:
                assert False, "Invalid register size/name."

            full_reg = self.get_native_register_or_subregister_by_name(instr, 8, self.REGS_X64_8[idx])
            t1 = self.function.ufunction.create_temp_register(8)
            t2 = self.function.ufunction.create_temp_register(8)
            self.emit(UCodeAnd(8, full_reg, UCodeConstant(8, const), t1), instr)
            self.emit(UCodeExtend(8, reg, t2), instr)
            self.emit(UCodeOr(8, t1, t2, full_reg), instr)
            return

        else:  # self.byte_size == 4
            if uinstr.size == 16: return  # XMM
            if uinstr.size == 4: return

            reg = uinstr.destination()
            assert isinstance(reg, UCodeRegister)

            if uinstr.size == 2:
                idx = self.REGS_X32_2.index(reg.name)
                const = 0xffffffffffff0000
            elif uinstr.size == 1:
                idx = self.REGS_X32_1.index(reg.name)
                const = 0xffffffffffffff00
            else:
                assert False, "Invalid register size/name."

            full_reg = self.get_native_register_or_subregister_by_name(instr, 4, self.REGS_X32_4[idx])
            t1 = self.function.ufunction.create_temp_register(4)
            t2 = self.function.ufunction.create_temp_register(4)
            self.emit(UCodeAnd(4, full_reg, UCodeConstant(4, const), t1), instr)
            self.emit(UCodeExtend(4, reg, t2), instr)
            self.emit(UCodeOr(4, t1, t2, full_reg), instr)
            return

    TWO_OP_INSTRUCTION_MAP = {
        X86_INS_ADD: (UCodeAdd, UCodeSetFlag.OPERATION_ADD),
        X86_INS_SUB: (UCodeSub, UCodeSetFlag.OPERATION_SUB),
        X86_INS_IMUL: (UCodeMul, None),  # TODO flags
        X86_INS_XOR: (UCodeXor, UCodeSetFlag.OPERATION_XOR),
        X86_INS_OR: (UCodeOr, UCodeSetFlag.OPERATION_OR),
        X86_INS_AND: (UCodeAnd, UCodeSetFlag.OPERATION_AND),
        X86_INS_SHL: (UCodeShiftLeft, None),
        X86_INS_SHR: (UCodeShiftRight, None),
        X86_INS_SAR: (UCodeShiftRight, None),
    }

    TWO_OP_XMM_INSTRUCTION_MAP = {
        X86_INS_ADDPD: UCodeAdd,
        X86_INS_ADDPS: UCodeAdd,
        X86_INS_ADDSD: UCodeAdd,
        X86_INS_ADDSS: UCodeAdd,
        X86_INS_SUBPD: UCodeSub,
        X86_INS_SUBPS: UCodeSub,
        X86_INS_SUBSD: UCodeSub,
        X86_INS_SUBSS: UCodeSub,
        X86_INS_MULPD: UCodeMul,
        X86_INS_MULPS: UCodeMul,
        X86_INS_MULSD: UCodeMul,
        X86_INS_MULSS: UCodeMul,
        X86_INS_DIVPD: UCodeDiv,
        X86_INS_DIVPS: UCodeDiv,
        X86_INS_DIVSD: UCodeDiv,
        X86_INS_DIVSS: UCodeDiv,
    }

    def emit_arithmetic_op(self, instr, ocode_op, uflag_op, op_count, implicit_value):
        size = instr.csinstr.operands[0].size
        if op_count == 2:
            src1 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0], size)
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[1], size)
        elif op_count == 1:
            src1 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0], size)
            src2 = implicit_value
        elif op_count == 3:
            src1 = self.ucode_for_operand_load(instr, instr.csinstr.operands[1], size)
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[2], size)
        else:
            assert False
        assert src1.size == size
        if src2.size != size:
            if size > src2.size:
                t = self.function.ufunction.create_temp_register(size)
                self.emit(UCodeExtend(size, src2, t), instr)
                src2 = t
            elif size < src2.size:
                t = self.function.ufunction.create_temp_register(size)
                self.emit(UCodeTruncate(size, src2, t), instr)
                src2 = t
        cond = self.function.ufunction.create_temp_register(src1.size)
        self.emit(ocode_op(cond.size, src1, src2, cond), instr)
        self.ucode_for_operand_store(instr, instr.csinstr.operands[0], cond)

        if uflag_op is not None:
            self.emit_flags(instr, src1, src2, uflag_op)

    def emit_flags(self, instr, src1, src2, uflag_op):
        self.emit(UCodeSetFlag(self.zf(), UCodeSetFlag.TYPE_ZERO, src1, src2, uflag_op), instr)
        self.emit(UCodeSetFlag(self.of(), UCodeSetFlag.TYPE_OVERFLOW, src1, src2, uflag_op), instr)
        self.emit(UCodeSetFlag(self.cf(), UCodeSetFlag.TYPE_CARRY, src1, src2, uflag_op), instr)
        self.emit(UCodeSetFlag(self.sf(), UCodeSetFlag.TYPE_SIGN, src1, src2, uflag_op), instr)
        self.emit(UCodeSetFlag(self.af(), UCodeSetFlag.TYPE_ADJUST, src1, src2, uflag_op), instr)
        self.emit(UCodeSetFlag(self.pf(), UCodeSetFlag.TYPE_PARITY, src1, src2, uflag_op), instr)

    def emit_ret(self, instr):
        args = []
        if not isinstance(self.function.returns.type, VoidType):
            args = [
                self.sema.get_uregister(self.function.ufunction, self.sema.retval_location(self.function.returns.type))]
        self.emit(UCodeRet(args), instr)

    def emit_call(self, instr):
        target = self.ucode_for_operand_load(instr, instr.csinstr.operands[0])
        dest = self.get_native_register_or_subregister_by_name(instr, self.arch.bytes(), self.sema.retval_location(self.function.binary.types.get("long")))
        self.emit(UCodeCall(target, dest, []), instr)

    def process_instruction(self, instr):
        self.ucode = []
        assert isinstance(instr, AssemblyInstruction)

        if instr.csinstr.id in [X86_INS_MOV, X86_INS_MOVSX, X86_INS_MOVSXD, X86_INS_MOVZX] or \
                    instr.csinstr.id in [X86_INS_MOVAPS, X86_INS_MOVAPD] or \
                    instr.csinstr.id in [X86_INS_MOVUPS, X86_INS_MOVUPD] or \
                    instr.csinstr.id in [X86_INS_MOVSD, X86_INS_MOVSS] or \
                    instr.csinstr.id in [X86_INS_MOVABS] or \
                    instr.csinstr.id in [X86_INS_CVTDQ2PD, X86_INS_CVTDQ2PS, X86_INS_CVTPD2DQ, X86_INS_CVTPD2PS, X86_INS_CVTPS2DQ, X86_INS_CVTPS2PD, X86_INS_CVTSD2SI, X86_INS_CVTSD2SS, X86_INS_CVTSI2SD, X86_INS_CVTSI2SS, X86_INS_CVTSS2SD, X86_INS_CVTSS2SI, X86_INS_CVTTPD2DQ, X86_INS_CVTTPS2DQ, X86_INS_CVTTSD2SI, X86_INS_CVTTSS2SI] or \
                    instr.csinstr.id in [X86_INS_CVTPD2PI, X86_INS_CVTPI2PD, X86_INS_CVTPI2PS, X86_INS_CVTPS2PI, X86_INS_CVTTPD2PI, X86_INS_CVTTPS2PI] \
                    :
            src = self.ucode_for_operand_load(instr, instr.csinstr.operands[1])
            self.ucode_for_operand_store(instr, instr.csinstr.operands[0], src)
            return
        if instr.csinstr.id == X86_INS_LEA:
            dst = self.ucode_for_operand(instr, instr.csinstr.operands[0])
            src = self.ucode_for_operand(instr, instr.csinstr.operands[1])
            assert src.type == OperandValue.TYPE_POINTER
            self.emit(UCodeMov(self.byte_size, src.value, dst.value), instr)
            return
        if instr.csinstr.id == X86_INS_CALL:
            self.emit_call(instr)
            return

        if instr.csinstr.id in [X86_INS_XOR, X86_INS_XORPS] and len(instr.csinstr.operands) == 2 and \
                    instr.csinstr.operands[0].type == X86_OP_REG and instr.csinstr.operands[1].type == X86_OP_REG and \
                    instr.csinstr.operands[0].reg == instr.csinstr.operands[1].reg:  # Special case "XOR eax, eax"
            size = instr.csinstr.operands[0].size
            implicit_value = UCodeConstant(size, 0)
            self.ucode_for_operand_store(instr, instr.csinstr.operands[0], implicit_value)
            return

        if instr.csinstr.id in [X86_INS_SHL, X86_INS_SHR, X86_INS_SAL, X86_INS_SAR] and len(instr.csinstr.operands) and \
                    instr.csinstr.operands[1].type == X86_OP_REG and instr.csinstr.operands[1].reg == X86_REG_CL:
            size = instr.csinstr.operands[0].size
            reg_name = "rcx" if size == 8 else "ecx"
            reg = self.get_native_register_or_subregister_by_name(instr, size, reg_name)
            op = UCodeShiftLeft if instr.csinstr.id in [X86_INS_SHL, X86_INS_SAL] else UCodeShiftRight
            src = self.ucode_for_operand_load(instr, instr.csinstr.operands[0], size)
            self.emit(op(size, src, reg, src), instr)
            return

        if instr.csinstr.id in list(self.TWO_OP_INSTRUCTION_MAP.keys()) and len(instr.csinstr.operands) == 2:
            (ucode_op, uflag_op) = self.TWO_OP_INSTRUCTION_MAP[instr.csinstr.id]
            return self.emit_arithmetic_op(instr, ucode_op, uflag_op, 2, None)

        if instr.csinstr.id in list(self.TWO_OP_XMM_INSTRUCTION_MAP.keys()) and len(instr.csinstr.operands) == 2:
            return self.emit_arithmetic_op(instr, self.TWO_OP_XMM_INSTRUCTION_MAP[instr.csinstr.id], None, 2, None)

        if instr.csinstr.id in [X86_INS_INC, X86_INS_DEC]:
            ucode_op = UCodeAdd if instr.csinstr.id == X86_INS_INC else UCodeSub
            uflag_op = UCodeSetFlag.OPERATION_ADD if instr.csinstr.id == X86_INS_INC else UCodeSetFlag.OPERATION_SUB
            size = instr.csinstr.operands[0].size
            implicit_value = UCodeConstant(size, 1)
            return self.emit_arithmetic_op(instr, ucode_op, uflag_op, 1, implicit_value)

        if instr.csinstr.id in [X86_INS_IMUL] and len(instr.csinstr.operands) == 1:
            size = instr.csinstr.operands[0].size
            assert size == self.arch.bytes()
            reg_name = "rax" if size == 8 else "eax"
            reg = self.get_native_register_or_subregister_by_name(instr, size, reg_name)
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0], size)
            self.emit(UCodeMul(size, reg, src2, reg), instr)
            return

        if instr.csinstr.id in [X86_INS_IMUL] and len(instr.csinstr.operands) == 3:
            return self.emit_arithmetic_op(instr, UCodeMul, None, 3, None)  # TODO: flags

        if instr.csinstr.id in [X86_INS_MULSD] and len(instr.csinstr.operands) == 2:
            return self.emit_arithmetic_op(instr, UCodeMul, None, 2, None)

        if instr.csinstr.id in [X86_INS_NEG] and len(instr.csinstr.operands) == 1:
            size = instr.csinstr.operands[0].size
            implicit_value = UCodeConstant(size, 0)
            return self.emit_arithmetic_op(instr, UCodeNeg, None, 1, implicit_value)

        if instr.csinstr.id in [X86_INS_IDIV] and len(instr.csinstr.operands) == 1:
            size = instr.csinstr.operands[0].size
            assert size == self.arch.bytes()
            reg_rax = self.get_native_register_or_subregister_by_name(instr, size, "rax" if size == 8 else "eax")
            reg_rdx = self.get_native_register_or_subregister_by_name(instr, size, "rdx" if size == 8 else "edx")
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0], size)
            self.emit(UCodeMod(size, reg_rax, src2, reg_rdx), instr)
            self.emit(UCodeDiv(size, reg_rax, src2, reg_rax), instr)
            return

        if instr.csinstr.id in [X86_INS_CQO] and len(instr.csinstr.operands) == 0:
            size = 8
            reg_rdx = self.get_native_register_or_subregister_by_name(instr, size, "rdx")
            self.emit(UCodeMov(size, UCodeConstant(size, 0), reg_rdx), instr)
            return

        if instr.csinstr.id in [X86_INS_CDQ] and len(instr.csinstr.operands) == 0:
            size = 4
            reg_rdx = self.get_native_register_or_subregister_by_name(instr, size, "rdx" if size == 8 else "edx")
            self.emit(UCodeMov(size, UCodeConstant(size, 0), reg_rdx), instr)
            return

        if instr.csinstr.id == X86_INS_CMP:
            src1 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0])
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[1])
            return self.emit_flags(instr, src1, src2, UCodeSetFlag.OPERATION_SUB)

        if instr.csinstr.id == X86_INS_TEST:
            src1 = self.ucode_for_operand_load(instr, instr.csinstr.operands[0])
            src2 = self.ucode_for_operand_load(instr, instr.csinstr.operands[1])
            return self.emit_flags(instr, src1, src2, UCodeSetFlag.OPERATION_AND)


        if instr.csinstr.id in [X86_INS_SETAE, X86_INS_SETA, X86_INS_SETBE, X86_INS_SETB, X86_INS_SETE, X86_INS_SETGE,
                                X86_INS_SETG, X86_INS_SETLE, X86_INS_SETL, X86_INS_SETNE, X86_INS_SETNO, X86_INS_SETNP,
                                X86_INS_SETNS, X86_INS_SETO, X86_INS_SETP, X86_INS_SETS]:
            self.ucode_for_conditional_set(instr)
            return

        if instr.csinstr.id == X86_INS_NOP:
            self.emit(UCodeNop(), instr)
            return

        if self.sema.is_conditional_jump(instr) or self.sema.is_unconditional_jump(instr):
            if instr.csinstr.operands[0].type == X86_OP_MEM:
                assert instr.csinstr.operands[0].mem.base == X86_REG_RIP
                assert instr.csinstr.operands[0].mem.index == X86_REG_INVALID
                imm = self.sema.pc_value_for_addr(instr, instr.addr) + instr.csinstr.operands[0].mem.disp
            elif instr.csinstr.operands[0].type == X86_OP_IMM:
                imm = instr.csinstr.operands[0].imm
            elif instr.csinstr.operands[0].type == X86_OP_REG:
                if instr.jump_table is not None:
                    # SWITCH.
                    value = self.get_native_register_or_subregister_by_name(instr, self.arch.bytes(), instr.jump_table_index_register)
                    self.emit(UCodeSwitch(instr.jump_table, value), instr)
                    return
                else:
                    # Treat "JMP eax" as "CALL eax; RET"
                    self.emit_call(instr)
                    self.emit_ret(instr)
                    return
            else:
                assert False
            cond = self.ucode_for_condition(instr)
            self.emit(UCodeBranch(UCodeConstant(self.arch.bytes(), imm), cond), instr)
            return

        if self.sema.is_return(instr):
            self.emit_ret(instr)
            return

        self.emit(UCodeAsm(instr), instr)

    def ucode_for_condition(self, instr):
        if instr.csinstr.id == X86_INS_JMP:
            self.emit(UCodeMov(1, UCodeConstant(1, 1), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JA, X86_INS_SETA]:
            t1 = self.function.ufunction.create_temp_register(1)
            t2 = self.function.ufunction.create_temp_register(1)
            self.emit(UCodeNeg(1, self.cf(), UCodeConstant(1, 0), t1), instr)
            self.emit(UCodeNeg(1, self.zf(), UCodeConstant(1, 0), t2), instr)
            self.emit(UCodeAnd(1, t1, t2, self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JAE, X86_INS_SETAE]:
            self.emit(UCodeNeg(1, self.cf(), UCodeConstant(1, 0), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JE, X86_INS_SETE]:
            self.emit(UCodeMov(1, self.zf(), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JNE, X86_INS_SETNE]:
            self.emit(UCodeNeg(1, self.zf(), UCodeConstant(1, 0), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JG, X86_INS_SETG]:
            t1 = self.function.ufunction.create_temp_register(1)
            self.emit(UCodeNeg(1, self.zf(), UCodeConstant(1, 0), t1), instr)
            t2 = self.function.ufunction.create_temp_register(1)
            self.emit(UCodeEquals(1, self.sf(), self.of(), t2), instr)
            self.emit(UCodeAnd(1, t1, t2, self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JGE, X86_INS_SETGE]:
            self.emit(UCodeEquals(1, self.sf(), self.of(), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JL, X86_INS_SETL]:
            t = self.function.ufunction.create_temp_register(1)
            self.emit(UCodeEquals(1, self.sf(), self.of(), t), instr)
            self.emit(UCodeNeg(1, t, UCodeConstant(1, 0), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JLE, X86_INS_SETLE]:
            t1 = self.zf()
            t2 = self.function.ufunction.create_temp_register(1)
            self.emit(UCodeEquals(1, self.sf(), self.of(), t2), instr)
            self.emit(UCodeNeg(1, t2, UCodeConstant(1, 0), t2), instr)
            self.emit(UCodeOr(1, t1, t2, self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JB, X86_INS_SETB]:
            self.emit(UCodeMov(1, self.cf(), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JBE, X86_INS_SETBE]:
            self.emit(UCodeOr(1, self.cf(), self.zf(), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JS, X86_INS_SETS]:
            self.emit(UCodeMov(1, self.sf(), self.bc()), instr)
            return self.bc()
        elif instr.csinstr.id in [X86_INS_JNS, X86_INS_SETNS]:
            self.emit(UCodeNeg(1, self.sf(), UCodeConstant(1, 0), self.bc()), instr)
            return self.bc()

        assert False, "TODO: implement all x86 condition codes"

    def flag_register(self, name):
        return self.function.ufunction.get_flag_register(name)

    def zf(self): return self.flag_register("zf")
    def of(self): return self.flag_register("of")
    def sf(self): return self.flag_register("sf")
    def af(self): return self.flag_register("af")
    def pf(self): return self.flag_register("pf")
    def cf(self): return self.flag_register("cf")

    def bc(self): return self.function.ufunction.get_custom_register("branch_condition", 1)

    def get_ucode(self):
        return self.ucode

    def ucode_for_conditional_set(self, instr):
        src = self.ucode_for_condition(instr)

        self.ucode_for_operand_store(instr, instr.csinstr.operands[0], src)
