import abc

from analysis.ucode.ucode_printer import UCodePrinter


class UCodeFunction:
    def __init__(self, byte_size, name, addr):
        self.name = name
        self.addr = addr
        self.bbs = None
        self.cfg = None
        self.byte_size = byte_size
        self.uregisters = {}
        self.temp_counter = 0
        self.stack_frame_size = 0
        self.stack_frame_base_register = None
        self.stack_pointer_register = None
        self.stack_frame_layout = []
        self.pc_register = None
        self.input_parameters = []

    def get_stack_variable_at_offset(self, base_offset, sp_offset):
        if base_offset is not None:
            for i in self.stack_frame_layout:
                # We have a direct match, yay!
                if i.base_offset == base_offset: return (i, 0)
                # Partial access
                if i.base_offset is not None and i.base_offset < base_offset < i.base_offset + i.size:
                    return (i, base_offset - i.base_offset)
        else:
            for i in self.stack_frame_layout:
                if i.sp_offset == sp_offset: return (i, 0)
        assert False

    def get_sp_relative_register(self, offset, size):
        return self.get_custom_register("var_sp_%x" % offset, size)

    def get_native_register(self, name):
        if name not in list(self.uregisters.keys()):
            self.uregisters[name] = UCodeRegister(self.byte_size, name, UCodeRegister.TYPE_NATIVE)
        reg = self.uregisters[name]
        assert reg.size == self.byte_size
        return reg

    def get_native_extra_register(self, name, size):
        if name not in list(self.uregisters.keys()):
            self.uregisters[name] = UCodeRegister(size, name, UCodeRegister.TYPE_NATIVE_EXTRA)
        reg = self.uregisters[name]
        assert reg.size == size
        return reg

    def get_native_subregister(self, name, size):
        if name not in list(self.uregisters.keys()):
            self.uregisters[name] = UCodeRegister(size, name, UCodeRegister.TYPE_NATIVE_SUBREGISTER)
        reg = self.uregisters[name]
        assert reg.size == size
        return reg

    def get_flag_register(self, name):
        if name not in list(self.uregisters.keys()):
            self.uregisters[name] = UCodeRegister(1, name, UCodeRegister.TYPE_FLAG)
        return self.uregisters[name]

    # TODO: remove this
    def get_custom_register(self, name, size):
        if name not in list(self.uregisters.keys()):
            self.uregisters[name] = UCodeRegister(size, name, UCodeRegister.TYPE_CUSTOM)
        reg = self.uregisters[name]
        assert reg.size == size
        return reg

    def create_temp_register(self, size):
        name = "temp_%d" % self.temp_counter
        self.temp_counter += 1
        assert name not in list(self.uregisters.keys())
        self.uregisters[name] = UCodeRegister(size, name, UCodeRegister.TYPE_TEMP)
        return self.uregisters[name]

    def compute_def_use_chains_single_bb(self, bb):
        defs = dict(bb._ins)  # Copy.
        changed = False
        for uinstr in bb.instructions:
            assert isinstance(uinstr, UCodeInstruction)

            # Go through all input operands.
            for operand in uinstr.input_operands():
                if operand in list(defs.keys()):
                    for defining_uinstr in defs[operand]:
                        if defining_uinstr not in uinstr._definitions:
                            uinstr._definitions.append(defining_uinstr)
                            assert uinstr not in defining_uinstr._uses
                            defining_uinstr._uses.append(uinstr)
                            changed = True

            if uinstr.has_destination:
                # We found a new definition.
                destination = uinstr.destination()
                defs[destination] = [uinstr]  # Discard previous definitions.

        bb._outs = defs
        return changed

    def merge_ins(self, result, to_merge_in):
        changed = False
        for key in list(to_merge_in.keys()):
            if key not in list(result.keys()):
                result[key] = list(to_merge_in[key])
                changed = True
            else:
                defs_for_key = result[key]
                for val in to_merge_in[key]:
                    if val not in defs_for_key:
                        defs_for_key.append(val)
                        changed = True
        return changed

    def compute_def_use_chains(self):
        for bb in self.bbs:
            bb._outs = {}
            bb._ins = {}
            for instr in bb.instructions:
                instr._definitions = []
                instr._uses = []

        changing = True
        while changing:
            changing = False
            for bb in self.bbs:
                changed = self.compute_def_use_chains_single_bb(bb)
                if changed: changing = True
                for succ_bb in bb.succs:
                    changed = self.merge_ins(succ_bb._ins, bb._outs)
                    if changed: changing = True

    def is_aliased(self, register):
        for bb in self.bbs:
            for instr in bb.instructions:
                if isinstance(instr, UCodeAddressOfLocal):
                    if instr.source() == register:
                        return True

        return False

    def print_to_text(self, show_ucode_details=False, main_function=None):
        return UCodePrinter(self).print_to_text(show_ucode_details, main_function)


class UCodeStackFrameItem:
    def __init__(self):
        self.register = None
        self.size = 0
        self.base_offset = 0
        self.sp_offset = 0


class UCodeRegisterInput(UCodeStackFrameItem):
    def __init__(self):
        self.register = None
        self.size = 0
        self.name = None

    def __str__(self):
        return "%s: %d bytes in register %s" % (self.name, self.size, self.register)

    def variable_name(self):
        return "%s" % self.register.name


class UCodeStackInput(UCodeStackFrameItem):
    def __init__(self):
        self.register = None
        self.size = 0
        self.name = None
        self.base_offset = 0

    def __str__(self):
        return "%s: %d bytes on stack at offset 0x%x" % (self.name, self.size, self.base_offset)

    def variable_name(self):
        return "sp_0x%x" % self.base_offset


class UCodeBasicBlock:
    def __init__(self):
        self.addr = None
        self.instructions = None
        self.succs = set()
        self.preds = set()
        self.is_entry = None
        self.is_exit = None
        self.number = None
        self._ins = None
        self._outs = None


class UCodeValue:
    def __init__(self, size):
        self.size = size
        pass


class UCodeRegister(UCodeValue):
    TYPE_NATIVE = 1
    TYPE_NATIVE_SUBREGISTER = 2
    TYPE_NATIVE_EXTRA = 2
    TYPE_FLAG = 3
    TYPE_TEMP = 4
    TYPE_CUSTOM = 5

    def __init__(self, size, name, type):
        UCodeValue.__init__(self, size)
        self.name = name
        self.type = type

    def __str__(self):
        return "%s.%d" % (self.name, self.size)

    def is_native(self):
        return self.type == UCodeRegister.TYPE_NATIVE


class UCodeBasicBlockAddress(UCodeValue):
    def __init__(self, bb):
        UCodeValue.__init__(self, 0)
        self.bb = bb

    def __str__(self):
        return "BB#%d" % self.bb.number


class UCodeConstant(UCodeValue):
    def __init__(self, size, value):
        UCodeValue.__init__(self, size)
        self.value = value
        self.name = None

    def display_as_symbol(self, name):
        self.name = name

    def __str__(self):
        if self.name is not None:
            return self.name
        return "0x%x" % self.value if self.value >= 0 else "-0x%x" % -self.value


class UCodeInstruction(metaclass=abc.ABCMeta):
    def __init__(self):
        self.addr = None
        self.pc_value = None
        self.bb = None
        self.operands = []
        self.size = None
        self.has_destination = False
        self.has_side_effects = False
        self.has_unknown_operands = False
        self._uses = None
        self._definitions = None

    def __deepcopy__(self, memo):
        import copy
        class AnyObject(object):
            pass
        result = AnyObject()
        result.__metaclass__ = self.__metaclass__
        result.__class__ = self.__class__
        memo[id(self)] = result
        for key, value in list(vars(self).items()):
            if key not in ["_uses", "_definitions"]:
                setattr(result, key, copy.deepcopy(value, memo))
        return result

    def __str__(self):
        m = "%s.%d" % (self.mnem(), self.size) if self.size != 0 else self.mnem()
        return "%-12s %s" % (m, self.operands_str())

    def __repr__(self):
        return str(self)

    def replace_with(self, i2):
        assert self.bb is not None
        idx = self.bb.instructions.index(self)
        if idx >= 0:
            i2.addr = self.addr
            i2.bb = self.bb
            self.bb.instructions[idx] = i2
            return i2
        assert False

    def insert_after(self, i2):
        assert self.bb is not None
        idx = self.bb.instructions.index(self)
        if idx >= 0:
            i2.addr = self.addr
            i2.bb = self.bb
            self.bb.instructions.insert(idx + 1, i2)
            return i2
        assert False

    def replace_uses_of_register(self, r1, r2):
        if not self.has_destination:
            self.operands = [(r2 if r == r1 else r) for r in self.operands]
        else:
            self.operands = [self.operands[0]] + [(r2 if r == r1 else r) for r in self.operands[1:]]

    def uses(self, needs_all_uses=False):
        if needs_all_uses:
            return None if self.has_unknown_operands else self._uses
        else:
            return self._uses

    def definitions(self, only_reg=None):
        return self._definitions if only_reg is None else [d for d in self._definitions if d.destination() == only_reg]

    @abc.abstractmethod
    def mnem(self):
        assert False

    @abc.abstractmethod
    def operands_str(self):
        assert False

    def destination(self):
        assert self.has_destination == False  # Subclasses will override to return destination.

    def input_operands(self):
        if self.has_destination:
            return (self.operands[1:] if len(self.operands) > 0 else [])
        else:
            return self.operands


class UCodeNop(UCodeInstruction):
    def __init__(self):
        UCodeInstruction.__init__(self)
        self.size = 0

    def mnem(self):
        return "uNOP"

    def operands_str(self):
        return ""


class UCodeAsm(UCodeInstruction):
    def __init__(self, asm_instruction):
        UCodeInstruction.__init__(self)
        self.asm_instruction = asm_instruction
        self.size = 0

    def mnem(self):
        return "uASM"

    def operands_str(self):
        return "__asm { %s }" % str(self.asm_instruction)


class UCodeMov(UCodeInstruction):
    def __init__(self, size, source, destination):
        UCodeInstruction.__init__(self)
        assert isinstance(source, UCodeValue)
        assert isinstance(destination, UCodeRegister)

        self.size = size
        self.operands = [destination, source]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def source(self):
        return self.operands[1]

    def mnem(self):
        return "uMOV"

    def operands_str(self):
        return "%s := %s" % (self.destination(), self.source())


class UCodeAddressOfLocal(UCodeInstruction):
    def __init__(self, size, source, offset, destination):
        UCodeInstruction.__init__(self)
        assert isinstance(source, UCodeRegister)
        assert isinstance(destination, UCodeRegister)
        assert isinstance(offset, int)

        self.size = size
        self.operands = [destination, source, offset]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def source(self):
        return self.operands[1]

    def offset(self):
        return self.operands[2]

    def mnem(self):
        return "uADDRESSOF"

    def operands_str(self):
        off_str = "" if self.offset() == 0 else " + 0x%x" % self.offset()
        return "%s := &(%s%s)" % (self.destination(), self.source(), off_str)


class UCodeSetMember(UCodeInstruction):
    def __init__(self, size, var, offset, value):
        UCodeInstruction.__init__(self)
        assert isinstance(var, UCodeRegister)
        assert isinstance(value, UCodeValue)
        assert isinstance(offset, int)

        self.size = size
        self.operands = [var, offset, value, var]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def offset(self):
        return self.operands[1]

    def value(self):
        return self.operands[2]

    def mnem(self):
        return "uSETMEMBER"

    def operands_str(self):
        return "%s[0x%x] := %s" % (self.destination(), self.offset(), self.value())

class UCodeGetMember(UCodeInstruction):
    def __init__(self, size, destination, value, offset):
        UCodeInstruction.__init__(self)
        assert isinstance(destination, UCodeRegister)
        assert isinstance(value, UCodeValue)
        assert isinstance(offset, int)

        self.size = size
        self.operands = [destination, offset, value]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def offset(self):
        return self.operands[1]

    def value(self):
        return self.operands[2]

    def mnem(self):
        return "uGETMEMBER"

    def operands_str(self):
        return "%s := %s[0x%x]" % (self.destination(), self.value(), self.offset())


class UCodeTruncate(UCodeInstruction):
    def __init__(self, size, source, destination):
        super(UCodeTruncate, self).__init__()
        assert isinstance(source, UCodeRegister) or isinstance(source, UCodeConstant)
        assert isinstance(destination, UCodeRegister)
        assert destination.size < source.size

        self.size = size
        self.operands = [destination, source]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def source(self):
        return self.operands[1]

    def mnem(self):
        return "uTRUNC"

    def operands_str(self):
        return "%s := %s" % (self.destination(), self.source())


class UCodeExtend(UCodeInstruction):
    def __init__(self, size, source, destination):
        super(UCodeExtend, self).__init__()
        assert isinstance(source, UCodeRegister) or isinstance(source, UCodeConstant)
        assert isinstance(destination, UCodeRegister)
        assert destination.size > source.size

        self.size = size
        self.operands = [destination, source]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def source(self):
        return self.operands[1]

    def mnem(self):
        return "uEXTEND"

    def operands_str(self):
        return "%s := %s" % (self.destination(), self.source())


class UCodeSetFlag(UCodeInstruction):
    OPERATION_NONE = 0
    OPERATION_ADD = 1
    OPERATION_SUB = 2
    OPERATION_AND = 3
    OPERATION_XOR = 4
    OPERATION_OR = 5

    TYPE_CARRY = 1
    TYPE_PARITY = 2
    TYPE_ADJUST = 3
    TYPE_ZERO = 4
    TYPE_SIGN = 5
    TYPE_OVERFLOW = 6

    def __init__(self, flag, type, source1, source2, operation):
        super(UCodeSetFlag, self).__init__()
        assert isinstance(flag, UCodeRegister)
        assert isinstance(source1, UCodeRegister)
        assert source2 is None or isinstance(source2, UCodeRegister) or isinstance(source2, UCodeConstant)
        assert operation in [self.OPERATION_NONE, self.OPERATION_ADD, self.OPERATION_SUB, self.OPERATION_AND, self.OPERATION_XOR, self.OPERATION_OR]
        assert type in [self.TYPE_CARRY, self.TYPE_PARITY, self.TYPE_ADJUST, self.TYPE_ZERO, self.TYPE_SIGN, self.TYPE_OVERFLOW]
        if operation == self.OPERATION_NONE: assert source2 is None
        else: assert source2 is not None

        self.size = 1
        self.operands = [flag, source1, source2]
        self.operation = operation
        self.type = type
        self.has_destination = True

    def source1(self):
        return self.operands[1]

    def source2(self):
        return self.operands[2]

    def flag(self):
        return self.operands[0]

    def destination(self):
        return self.flag()

    def operands_str(self):
        if self.operation == self.OPERATION_NONE: s = str(self.source1())
        elif self.operation == self.OPERATION_ADD: s = "%s + %s" % (self.source1(), self.source2())
        elif self.operation == self.OPERATION_SUB: s = "%s - %s" % (self.source1(), self.source2())
        elif self.operation == self.OPERATION_AND: s = "%s & %s" % (self.source1(), self.source2())
        elif self.operation == self.OPERATION_OR: s = "%s | %s" % (self.source1(), self.source2())
        elif self.operation == self.OPERATION_XOR: s = "%s ^ %s" % (self.source1(), self.source2())
        else: assert False

        if self.type == self.TYPE_CARRY: s = "CARRY(%s)" % s
        elif self.type == self.TYPE_PARITY: s = "PARITY(%s)" % s
        elif self.type == self.TYPE_ADJUST: s = "ADJUST(%s)" % s
        elif self.type == self.TYPE_ZERO: s = "ZERO(%s)" % s
        elif self.type == self.TYPE_SIGN: s = "SIGN(%s)" % s
        elif self.type == self.TYPE_OVERFLOW: s = "OVERFLOW(%s)" % s

        return "%s := %s" % (self.flag(), s)

    def mnem(self):
        return "uFLAG"


class UCodeArithmeticOperation(UCodeInstruction):
    def __init__(self, size, source1, source2, destination):
        UCodeInstruction.__init__(self)
        assert isinstance(source1, UCodeValue)
        assert isinstance(source2, UCodeValue)
        assert isinstance(destination, UCodeRegister)
        assert destination.size == source1.size and source1.size == source2.size

        self.size = size
        self.operands = [destination, source1, source2]
        self.has_destination = True

    def destination(self):
        return self.operands[0]

    def source1(self):
        return self.operands[1]

    def source2(self):
        return self.operands[2]

    @abc.abstractmethod
    def operation_str(self):
        assert False

    @abc.abstractmethod
    def mnem(self):
        assert False

    def operands_str(self):
        return "%s := %s %s %s" % (self.destination(), self.source1(), self.operation_str(), self.source2())


class UCodeAdd(UCodeArithmeticOperation):
    def mnem(self): return "uADD"
    def operation_str(self): return "+"
class UCodeSub(UCodeArithmeticOperation):
    def mnem(self): return "uSUB"
    def operation_str(self): return "-"
class UCodeMul(UCodeArithmeticOperation):
    def mnem(self): return "uMUL"
    def operation_str(self): return "*"
class UCodeDiv(UCodeArithmeticOperation):
    def mnem(self): return "uDIV"
    def operation_str(self): return "/"
class UCodeMod(UCodeArithmeticOperation):
    def mnem(self): return "uMOD"
    def operation_str(self): return "%"


class UCodeAnd(UCodeArithmeticOperation):
    def mnem(self): return "uAND"
    def operation_str(self): return "&"
class UCodeOr(UCodeArithmeticOperation):
    def mnem(self): return "uOR"
    def operation_str(self): return "|"
class UCodeXor(UCodeArithmeticOperation):
    def mnem(self): return "uXOR"
    def operation_str(self): return "^"
class UCodeShiftLeft(UCodeArithmeticOperation):
    def mnem(self): return "uSHL"
    def operation_str(self): return "<<"
class UCodeShiftRight(UCodeArithmeticOperation):
    def mnem(self): return "uSHR"
    def operation_str(self): return ">>"


class UCodeNeg(UCodeArithmeticOperation):
    def mnem(self): return "uNEG"
    def operation_str(self): return "~"
    def operands_str(self):
        return "%s := ~%s" % (self.destination(), self.source1())


class UCodeEquals(UCodeArithmeticOperation):
    def mnem(self): return "uEQUALS"
    def operation_str(self): return "=="

class UCodeLoad(UCodeInstruction):
    def __init__(self, size, pointer, register):
        UCodeInstruction.__init__(self)
        assert isinstance(pointer, UCodeValue)
        assert isinstance(register, UCodeRegister)

        self.size = size
        self.operands = [register, pointer]
        self.has_destination = True

    def pointer(self):
        return self.operands[1]

    def register(self):
        return self.operands[0]

    def destination(self):
        return self.register()

    def mnem(self):
        return "uLOAD"

    def operands_str(self):
        return "%s := *(%s)" % (self.register(), self.pointer())


class UCodeStore(UCodeInstruction):
    def __init__(self, size, pointer, source):
        UCodeInstruction.__init__(self)
        assert isinstance(pointer, UCodeValue)
        assert isinstance(source, UCodeRegister) or isinstance(source, UCodeConstant)

        self.size = size
        self.operands = [pointer, source]
        self.has_side_effects = True

    def pointer(self):
        return self.operands[0]

    def source(self):
        return self.operands[1]

    def mnem(self):
        return "uSTORE"

    def operands_str(self):
        return "*(%s) := %s" % (self.pointer(), self.source())


class UCodeCallStackParameter(UCodeValue):
    def __init__(self, size, base_register, offset):
        UCodeValue.__init__(self, size)
        self.base_register = base_register
        self.offset = offset

    def __str__(self):
        return "[%s+0x%x]" % (self.base_register, self.offset)


class UCodeCall(UCodeInstruction):
    def __init__(self, callee, destination, params, full_operators=False, param_types=None, return_type=None):
        UCodeInstruction.__init__(self)
        self.size = 0
        self.operands = [destination, callee] + params
        self.has_destination = destination is not None
        self.has_side_effects = True
        self.has_unknown_operands = not full_operators
        self.param_types = param_types
        self.return_type = return_type

    def all_operands_despilled(self):
        for p in self.params():
            if isinstance(p, UCodeCallStackParameter): return False
        return True

    def callee(self):
        return self.operands[1]

    def destination(self):
        return self.operands[0]

    def params(self):
        return self.operands[2:]

    def params_str(self):
        ar = [str(p) for p in self.params()]
        if self.has_unknown_operands: ar.append("...")
        return ", ".join(ar)

    def mnem(self):
        return "uCALL"

    def operands_str(self):
        if self.has_destination:
            return "%s := %s(%s)" % (self.destination(), self.callee(), self.params_str())
        else:
            return "%s(%s)" % (self.callee(), self.params_str())


class UCodeBranch(UCodeInstruction):
    def __init__(self, target, condition):
        UCodeInstruction.__init__(self)
        assert isinstance(target, UCodeConstant)
        assert isinstance(condition, UCodeRegister)

        self.size = 0
        self.operands = [condition, target]

    def condition(self):
        return self.operands[0]

    def target(self):
        return self.operands[1]

    def mnem(self):
        return "uBRANCH"

    def operands_str(self):
        return "%s, %s" % (self.condition(), self.target())


class UCodeSwitch(UCodeInstruction):
    def __init__(self, targets, value):
        UCodeInstruction.__init__(self)
        assert isinstance(targets, list)
        assert isinstance(value, UCodeRegister)

        self.size = 0
        self.targets = targets
        self.operands = [value]

    def condition(self):
        return self.operands[0]

    def mnem(self):
        return "uSWITCH"

    def operands_str(self):
        return "%s in [%s]" % (self.condition(), ", ".join([("0x%x" % i) for i in self.targets]))


class UCodeRet(UCodeInstruction):
    def __init__(self, operands):
        UCodeInstruction.__init__(self)
        self.size = 0
        self.operands = operands

    def operands_str(self):
        return ", ".join([str(r) for r in self.operands])

    def mnem(self):
        return "uRET"
