import abc
from analysis.ucode.ucode import *


class UCodeBasicBlockTransform:
    def __init__(self, function, bb, binary=None):
        self.function = function
        self.bb = bb
        self.idx = function.bbs.index(bb)
        self.binary = binary

    def can_be_performed(self):
        return self.can_be_performed_on_bb(self.bb, self.function, self.idx)

    def perform(self):
        self.perform_on_bb(self.bb, self.function, self.idx)

    @abc.abstractmethod
    def can_be_performed_on_bb(self, bb, function, idx):
        assert False

    @abc.abstractmethod
    def perform_on_bb(self, bb, function, idx):
        assert False


class UCodeApplyInstructionTransformToAllFromBasicBlock(UCodeBasicBlockTransform):
    def __init__(self, function, bb, instruction_transform):
        UCodeBasicBlockTransform.__init__(self, function, bb)
        self.instruction_transform = instruction_transform

    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        for instr in bb.instructions:
            transform = self.instruction_transform(self.function, instr)
            transform.perform()


class UCodeRemoveNopsFromBasicBlock(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        bb.instructions = [instr for instr in bb.instructions if not isinstance(instr, UCodeNop)]


"""
Stack item to local variable promotion.
"""
class UCodeConvertStackVariablesToRegisters(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        for (idx, instruction) in enumerate(bb.instructions):
            reg = None
            offset = None

            if isinstance(instruction, UCodeAdd):
                if isinstance(instruction.source1(), UCodeRegister):
                    if instruction.source1() == function.stack_frame_base_register \
                            or instruction.source1() == function.stack_pointer_register:
                        if isinstance(instruction.source2(), UCodeConstant):
                            reg = instruction.source1()
                            offset = instruction.source2().value
            elif isinstance(instruction, UCodeStore):
                if instruction.pointer() == function.stack_pointer_register:
                    local_variable_register = function.get_sp_relative_register(0, instruction.size)
                    instruction.replace_with(UCodeMov(instruction.size, instruction.source(), local_variable_register))
                    continue
            elif isinstance(instruction, UCodeLoad):
                if instruction.pointer() == function.stack_pointer_register:
                    local_variable_register = function.get_sp_relative_register(0, instruction.size)
                    instruction.replace_with(UCodeMov(instruction.size, local_variable_register, instruction.destination()))
                    continue

            if reg is None: continue

            temp_register = instruction.destination()

            if reg == function.stack_frame_base_register:
                (stack_frame_item, local_variable_offset) = function.get_stack_variable_at_offset(offset, None)
                local_variable_register = stack_frame_item.register
            else:
                local_variable_offset = 0
                local_variable_register = function.get_sp_relative_register(offset, instruction.size)

            # Generate ADDRESSOF
            instruction.replace_with(UCodeAddressOfLocal(instruction.size, local_variable_register, local_variable_offset, instruction.destination()))

            # Poor-man's use detection. TODO: find all uses, transform all uses.
            if not len(bb.instructions) >= idx + 2: continue
            use = bb.instructions[idx + 1]
            if not (isinstance(use, UCodeLoad) or isinstance(use, UCodeStore)):
                if not len(bb.instructions) >= idx + 3: continue
                use = bb.instructions[idx + 2]
            if not (isinstance(use, UCodeLoad) or isinstance(use, UCodeStore)): continue
            if not use.pointer() == temp_register: continue

            if isinstance(use, UCodeLoad):
                # Replace the uLOAD with:
                #    1) direct local-variable assignment
                # or 2) uGETMEMBER
                if local_variable_offset == 0 and use.size == local_variable_register.size:
                    use.replace_with(UCodeMov(use.size, local_variable_register, use.destination()))
                else:
                    use.replace_with(UCodeGetMember(use.size, use.destination(), local_variable_register, local_variable_offset))
            elif isinstance(use, UCodeStore):
                # Replace the uSTORE with:
                #    1) direct local-variable assignment
                # or 2) uSETMEMBER
                if local_variable_offset == 0 and use.size == local_variable_register.size:
                    use.replace_with(UCodeMov(use.size, use.source(), local_variable_register))
                else:
                    use.replace_with(UCodeSetMember(use.size, local_variable_register, local_variable_offset, use.source()))



class UCodeDetectPattern1(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        constant = 0xffffffffffffff00 if function.byte_size == 8 else 0xffffff00
        for (idx, instruction) in enumerate(bb.instructions):
            if not isinstance(instruction, UCodeAnd): continue
            if not isinstance(instruction.source2(), UCodeConstant): continue
            if not instruction.source2().value == constant: continue
            if not len(instruction.uses()) == 1: continue
            or_instr = instruction.uses()[0]
            if not isinstance(or_instr, UCodeOr): continue
            if not len(or_instr.uses()) == 1: continue
            trunc_instr = or_instr.uses()[0]
            destination_reg = trunc_instr.destination()
            if not isinstance(trunc_instr, UCodeTruncate): continue
            extend_instr = or_instr.source2()
            if not len(or_instr.definitions(extend_instr)) == 1: continue
            extend_instr = or_instr.definitions(extend_instr)[0]
            if not isinstance(extend_instr, UCodeExtend): continue
            source_reg = extend_instr.source()

            if not trunc_instr in trunc_instr.bb.instructions: continue

            trunc_instr.replace_with(UCodeMov(source_reg.size, source_reg, destination_reg))


class UCodeDetectPattern2(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        for (idx, instruction) in enumerate(bb.instructions):
            if not isinstance(instruction, UCodeTruncate): continue
            trunc_instr = instruction
            if len(trunc_instr.definitions()) != 1: continue
            extend_instr = trunc_instr.definitions()[0]
            if not isinstance(extend_instr, UCodeExtend): continue
            if not (extend_instr.source().size == trunc_instr.destination().size): continue

            trunc_instr.replace_with(UCodeMov(trunc_instr.size, extend_instr.source(), trunc_instr.destination()))


class UCodeDetectPattern3(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        for (idx, instruction) in enumerate(bb.instructions):
            if not isinstance(instruction, UCodeAddressOfLocal): continue
            addressof_instr = instruction
            if len(addressof_instr.uses()) != 1: continue
            store_instr = addressof_instr.uses()[0]
            if not isinstance(store_instr, UCodeStore): continue
            if not (store_instr.size == addressof_instr.source().size): continue

            store_instr.replace_with(UCodeMov(store_instr.size, store_instr.source(), addressof_instr.source()))


class UCodeDetectPattern4(UCodeBasicBlockTransform):
    def can_be_performed_on_bb(self, bb, function, idx):
        return True

    def perform_on_bb(self, bb, function, idx):
        for (idx, instruction) in enumerate(bb.instructions):
            if not isinstance(instruction, UCodeMov): continue
            mov_instr = instruction
            if not isinstance(mov_instr.source(), UCodeRegister): continue
            if len(mov_instr.definitions()) != 1: continue
            def_instr = mov_instr.definitions()[0]
            if len(def_instr.uses()) != 1: continue
            if len(mov_instr.uses()) != 1: continue

            if isinstance(mov_instr.destination(), UCodeRegister): continue
            if mov_instr.destination().type != UCodeRegister.TYPE_TEMP: continue

            use_instr = mov_instr.uses()[0]
            use_instr.replace_uses_of_register(mov_instr.destination(), mov_instr.source())
