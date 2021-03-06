import abc
from analysis.ucode.ucode import *


FAKE_FUNCTION_ADDR = 0xdeadbabe


class UCodeInstructionTransform:
    def __init__(self, function, instruction, binary=None):
        self.function = function
        self.instruction = instruction
        self.binary = binary

    def can_be_performed(self):
        idx = self.instruction.bb.instructions.index(self.instruction)
        return self.can_be_performed_on_instruction(self.instruction, self.instruction.bb, idx)

    def perform(self):
        if not self.can_be_performed(): return

        idx = self.instruction.bb.instructions.index(self.instruction)
        self.perform_on_instruction(self.instruction, self.instruction.bb, idx)

    @abc.abstractmethod
    def can_be_performed_on_instruction(self, instruction, bb, idx):
        assert False

    @abc.abstractmethod
    def perform_on_instruction(self, instruction, bb, idx):
        assert False


class UCodeCopyPropagateInstruction(UCodeInstructionTransform):
    name = "Copy Propagate Instruction"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeMov): return False
        destination = instruction.destination()
        if not isinstance(destination, UCodeRegister): return False
        return True

    def is_clobbered(self, register, from_instruction, to_instruction):
        assert from_instruction.bb == to_instruction.bb
        idx1 = from_instruction.bb.instructions.index(from_instruction)
        idx2 = from_instruction.bb.instructions.index(to_instruction)

        for i in from_instruction.bb.instructions[idx1+1:idx2]:
            if i.has_destination and i.destination() == register:
                return True

            if isinstance(i, UCodeStore) or isinstance(i, UCodeCall):
                if self.function.is_aliased(register):
                    return True

        return False

    def perform_on_instruction(self, instruction, bb, idx):
        defined_register = instruction.destination()
        defined_value = instruction.source()
        operands = instruction.operands

        # Copy via def-use chains.
        for use in instruction.uses():
            if len(use.definitions()) == 1:
                if isinstance(defined_value, UCodeConstant):
                    if not self.function.is_aliased(defined_register):
                        use.replace_uses_of_register(defined_register, defined_value)
                else:
                    if use.bb == instruction.bb:  # For non-constants, only propagate within BB.
                        if not self.is_clobbered(defined_value, instruction, use) and not self.function.is_aliased(defined_register):
                            use.replace_uses_of_register(defined_register, defined_value)

        for uinstr in bb.instructions[idx+1:]:
            if defined_register in uinstr.operands:
                # We found a use
                if not self.function.is_aliased(defined_register):
                    uinstr.replace_uses_of_register(defined_register, defined_value)

            if uinstr.has_destination and uinstr.destination() in operands:
                # We found a new definition of one of the operands used to calculate defined_register
                break

            if uinstr.has_destination and uinstr.destination() == defined_register:
                # We found a new definition of defined_register
                break


class UCodeConstantFoldInstruction(UCodeInstructionTransform):
    name = "Fold Constants on Instruction"

    def try_fold(self, instruction, for_real=False):
        replacer = instruction.replace_with if for_real else lambda x: None

        if isinstance(instruction, UCodeAdd):
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeConstant):
                value = UCodeConstant(instruction.size, instruction.source1().value + instruction.source2().value)
                replacer(UCodeMov(instruction.size, value, instruction.destination()))
                return True
            if isinstance(instruction.source1(), UCodeRegister) and isinstance(instruction.source2(), UCodeConstant):
                if instruction.source2().value == 0:
                    replacer(UCodeMov(instruction.size, instruction.source1(), instruction.destination()))
                    return True
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeRegister):
                if instruction.source1().value == 0:
                    replacer(UCodeMov(instruction.size, instruction.source2(), instruction.destination()))
                    return True
        if isinstance(instruction, UCodeMul):
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeConstant):
                value = UCodeConstant(instruction.size, instruction.source1().value * instruction.source2().value)
                replacer(UCodeMov(instruction.size, value, instruction.destination()))
                return True
            if isinstance(instruction.source1(), UCodeRegister) and isinstance(instruction.source2(), UCodeConstant):
                if instruction.source2().value == 1:
                    replacer(UCodeMov(instruction.size, instruction.source1(), instruction.destination()))
                    return True
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeRegister):
                if instruction.source1().value == 1:
                    replacer(UCodeMov(instruction.size, instruction.source2(), instruction.destination()))
                    return True
        if isinstance(instruction, UCodeOr):
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeConstant):
                value = UCodeConstant(instruction.size, instruction.source1().value | instruction.source2().value)
                replacer(UCodeMov(instruction.size, value, instruction.destination()))
                return True
        if isinstance(instruction, UCodeAnd):
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeConstant):
                value = UCodeConstant(instruction.size, instruction.source1().value & instruction.source2().value)
                replacer(UCodeMov(instruction.size, value, instruction.destination()))
                return True
        if isinstance(instruction, UCodeXor):
            if isinstance(instruction.source1(), UCodeConstant) and isinstance(instruction.source2(), UCodeConstant):
                value = UCodeConstant(instruction.size, instruction.source1().value ^ instruction.source2().value)
                replacer(UCodeMov(instruction.size, value, instruction.destination()))
                return True
        if isinstance(instruction, UCodeXor):
            if isinstance(instruction.source1(), UCodeRegister) and isinstance(instruction.source2(), UCodeRegister):
                if instruction.source1() == instruction.source2():
                    value = UCodeConstant(instruction.size, 0)
                    replacer(UCodeMov(instruction.size, value, instruction.destination()))
                    return True
        if isinstance(instruction, UCodeExtend) or isinstance(instruction, UCodeTruncate):
            if isinstance(instruction.source(), UCodeConstant):
                constant = UCodeConstant(instruction.size, instruction.source().value)
                constant.display_as_symbol(instruction.source().name)
                replacer(UCodeMov(instruction.size, constant, instruction.destination()))
                return True
        return False

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        return self.try_fold(instruction)

    def perform_on_instruction(self, instruction, bb, idx):
        return self.try_fold(instruction, True)


class UCodeDeadCodeEliminateInstruction(UCodeInstructionTransform):
    name = "Dead Code Elimination on Instruction"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not instruction.has_destination: return False
        if instruction.has_side_effects: return False
        if len(instruction.uses()) > 0: return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        destination = instruction.destination()
        eliminate = True

        for uinstr in bb.instructions[idx+1:]:
            if destination in uinstr.input_operands():
                # We found a use.
                eliminate = False
                break

            if uinstr.has_unknown_operands:
                # We found a possible use ("uCALL" with unresolved operands), let's be conservative.
                if destination.type != UCodeRegister.TYPE_TEMP:
                    eliminate = False
                    break

            if uinstr.has_destination and uinstr.destination() == destination:
                # We found a new definition.
                break

        if eliminate:
            if self.function.is_aliased(destination):
                eliminate = False

        # If we found a new definition or we reached end of BB before a use, then eliminate.
        if eliminate:
            instruction.replace_with(UCodeNop())


class UCodeRemovePCReferences(UCodeInstructionTransform):
    name = "Remove PC References"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        pc_register = self.function.pc_register
        value = UCodeConstant(self.function.byte_size, self.instruction.pc_value)
        instruction.replace_uses_of_register(pc_register, value)


class UCodeResolveIVars(UCodeInstructionTransform):
    name = "Resolve ivars"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeLoad): return False
        pointer = instruction.pointer()
        if not isinstance(pointer, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.pointer().value
        binary = self.binary
        if value in list(binary.ivars.keys()):
            ivar = binary.ivars[value]
            destination_reg = instruction.destination()
            constant = UCodeConstant(destination_reg.size, ivar.offset)
            constant.display_as_symbol(ivar.name)
            instruction.replace_with(UCodeMov(destination_reg.size, constant, destination_reg))


class UCodeResolveOffsetCalls(UCodeInstructionTransform):
    name = "Resolve Offset Calls"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeLoad): return False
        pointer = instruction.pointer()
        if not isinstance(pointer, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.pointer().value
        binary = self.binary
        if value in list(binary.external_pointers.keys()):
            func_name = binary.external_pointers[value]
            destination_reg = instruction.destination()
            constant = UCodeConstant(destination_reg.size, FAKE_FUNCTION_ADDR)
            constant.display_as_symbol(func_name)
            instruction.replace_with(UCodeMov(destination_reg.size, constant, destination_reg))


class UCodeResolveCCalls(UCodeInstructionTransform):
    name = "Resolve C Calls"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        pointer = instruction.callee()
        if not isinstance(pointer, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.callee().value
        binary = self.binary
        mymap = dict([(f.addr, f.name) for f in self.binary.functions])
        if value in list(mymap.keys()):
            func_name = mymap[value]
            instruction.callee().display_as_symbol(func_name)

class UCodeResolveCalls(UCodeInstructionTransform):
    name = "Resolve Calls"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        callee = instruction.callee()
        if not instruction.has_unknown_operands: return False
        if not isinstance(callee, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.callee().value
        binary = self.binary
        if value in list(binary.stubs.keys()):
            func_name = binary.stubs[value]
            instruction.callee().display_as_symbol(func_name)
            binary.call_resolver.resolve_call(self.function, instruction)
        else:
            if instruction.callee().name is not None:
                binary.call_resolver.resolve_call(self.function, instruction)


class UCodeResolveUnknownCalls(UCodeInstructionTransform):
    name = "Heuristically Resolve Unknown Calls"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        callee = instruction.callee()
        if not instruction.has_unknown_operands: return False
        if not isinstance(callee, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.callee().value
        binary = self.binary
        if value not in list(binary.stubs.keys()) and value != FAKE_FUNCTION_ADDR:
            binary.call_resolver.guess_parameters(self.function, instruction, bb, idx)

        if value in list(binary.stubs.keys()):
            # The signature library is missing this imported symbol, let's resolve it anyway
            binary.call_resolver.guess_parameters(self.function, instruction, bb, idx)


class UCodeResolveSelectors(UCodeInstructionTransform):
    name = "Resolve Selectors"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeLoad): return False
        pointer = instruction.pointer()
        if not isinstance(pointer, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.pointer().value
        binary = self.binary
        if value in list(binary.selectors.keys()):
            selector = binary.selectors[value]
            destination_reg = instruction.destination()
            constant = UCodeConstant(destination_reg.size, selector.string_location)
            constant.display_as_symbol(selector.name)
            instruction.replace_with(UCodeMov(destination_reg.size, constant, destination_reg))


class UCodeResolveClassRefs(UCodeInstructionTransform):
    name = "Resolve Class References"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeLoad): return False
        pointer = instruction.pointer()
        if not isinstance(pointer, UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        value = instruction.pointer().value
        binary = self.binary
        if value in list(binary.class_refs.keys()):
            cls = binary.class_refs[value]
            destination_reg = instruction.destination()
            constant = UCodeConstant(destination_reg.size, cls.class_location)
            constant.display_as_symbol(cls.symbol_name)
            instruction.replace_with(UCodeMov(destination_reg.size, constant, destination_reg))


class UCodeResolveCFStrings(UCodeInstructionTransform):
    name = "Resolve CFString References"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        if isinstance(instruction, UCodeMov):
            if isinstance(instruction.source(), UCodeConstant):
                value = instruction.source().value
                if value in list(self.binary.cfstrings.keys()):
                    instruction.source().display_as_symbol(self.binary.cfstrings[value].name)
        elif isinstance(instruction, UCodeCall):
            for p in instruction.params():
                if isinstance(p, UCodeConstant):
                    value = p.value
                    if value in list(self.binary.cfstrings.keys()):
                        p.display_as_symbol(self.binary.cfstrings[value].name)


class UCodeRemoveUselessMoves(UCodeInstructionTransform):
    name = "Remove Useless Moves"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeMov): return False
        if instruction.source() != instruction.destination(): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        instruction.replace_with(UCodeNop())


class UCodeFoldArithmeticChains(UCodeInstructionTransform):
    name = "Fold Arithmetic Chains"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeAdd): return False
        if not isinstance(instruction.source2(), UCodeConstant): return False
        if not isinstance(instruction.source1(), UCodeRegister): return False
        defs = instruction.definitions(instruction.source1())
        if not len(defs) == 1: return False
        definition = defs[0]
        if not isinstance(definition, UCodeAdd): return False
        if not isinstance(definition.source2(), UCodeConstant): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        definition = instruction.definitions(instruction.source1())[0]
        value = definition.source2().value + instruction.source2().value
        instruction.replace_with(UCodeAdd(instruction.size, definition.source1(), UCodeConstant(instruction.size, value), instruction.destination()))


class UCodeNormalizeArithmetics(UCodeInstructionTransform):
    name = "Normalize Arithmetic Operations"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeAdd) and not isinstance(instruction, UCodeMul): return False
        if not isinstance(instruction.source1(), UCodeConstant): return False
        if not isinstance(instruction.source2(), UCodeRegister): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        assert isinstance(instruction, UCodeArithmeticOperation)
        assert isinstance(instruction.source1(), UCodeConstant)
        assert isinstance(instruction.source2(), UCodeRegister)

        if isinstance(instruction, UCodeAdd):
            instruction.replace_with(UCodeAdd(instruction.size, instruction.source2(), instruction.source1(), instruction.destination()))
        elif isinstance(instruction, UCodeMul):
            instruction.replace_with(UCodeMul(instruction.size, instruction.source2(), instruction.source1(), instruction.destination()))


class UCodeRemoveUnusedCallResults(UCodeInstructionTransform):
    name = "Remove Unused Call Results"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        if not instruction.has_destination: return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        assert isinstance(instruction, UCodeCall)
        output_reg = instruction.destination()
        assert isinstance(output_reg, UCodeRegister)
        uses = instruction.uses(needs_all_uses=True)
        if uses is None: return
        if len(uses) == 0:
            instruction.replace_with(UCodeCall(instruction.callee(), None, instruction.params(), not instruction.has_unknown_operands, instruction.param_types, instruction.return_type))


class UCodeStackArgumentsToRegisters(UCodeInstructionTransform):
    name = "Convert Stack Arguments to Registers"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        # if instruction.callee.name is None: return False  # Callee must be resolved.
        # if instruction.has_unknown_operands: return False  # Arguments must be resolved.
        found_stack_argument = False
        for p in instruction.params():
            if isinstance(p, UCodeCallStackParameter): found_stack_argument = True
        if not found_stack_argument: return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        callee = instruction.callee()
        call_destination = instruction.destination()
        params = instruction.params()
        has_unknown_operands = instruction.has_unknown_operands
        sp_reg = self.function.get_native_register(self.binary.arch.sema.sp_register())
        offset_to_param_index_map = {}
        for (param_index, p) in enumerate(instruction.params()):
            if isinstance(p, UCodeCallStackParameter):
                offset_to_param_index_map[p.offset] = param_index

        for i in range(idx - 1, -1, -1):
            store_instr = bb.instructions[i]
            if isinstance(store_instr, UCodeCall): break
            if not isinstance(store_instr, UCodeStore): continue

            if store_instr.pointer() == sp_reg:
                # *(esp) := ...
                if 0 not in list(offset_to_param_index_map.keys()): continue

                t = self.function.create_temp_register(store_instr.size)
                store_instr.replace_with(UCodeMov(store_instr.size, store_instr.source(), t))
                params[offset_to_param_index_map[0]] = t
                del offset_to_param_index_map[0]
                continue

            address_register = store_instr.pointer()
            assert isinstance(address_register, UCodeRegister)
            definitions = store_instr.definitions(address_register)
            assert len(definitions) == 1
            sp_offset_calc_instr = definitions[0]
            if not isinstance(sp_offset_calc_instr, UCodeAdd): continue
            if not sp_offset_calc_instr.source1() == sp_reg: continue
            assert isinstance(sp_offset_calc_instr.source2(), UCodeConstant)
            offset = sp_offset_calc_instr.source2().value
            if offset not in offset_to_param_index_map: continue

            # temp = esp + 0x10
            # *(temp) = ...

            t = self.function.create_temp_register(store_instr.size)
            store_instr.replace_with(UCodeMov(store_instr.size, store_instr.source(), t))
            params[offset_to_param_index_map[offset]] = t
            del offset_to_param_index_map[offset]

        instruction.replace_with(UCodeCall(callee, call_destination, params, not has_unknown_operands, instruction.param_types, instruction.return_type))


class UCodeRemoveRetainRelease(UCodeInstructionTransform):
    name = "Remove ARC Retain-Release"

    def can_be_performed_on_instruction(self, instruction, bb, idx):
        if not isinstance(instruction, UCodeCall): return False
        if not isinstance(instruction.callee(), UCodeConstant): return False
        if instruction.callee().name is None: return False
        if not instruction.all_operands_despilled(): return False
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        assert isinstance(instruction, UCodeCall)
        f = instruction.callee().name
        if f in ["_objc_retainAutoreleasedReturnValue", "_objc_retain", "_objc_retainAutorelease", "_objc_autoreleaseReturnValue", "_objc_retainAutoreleaseReturnValue"]:
            if instruction.has_destination:
                if not len(instruction.params()) > 0: return
                ptr_size = instruction.params()[0].size
                instruction.replace_with(UCodeMov(ptr_size, instruction.params()[0], instruction.destination()))
            else:
                instruction.replace_with(UCodeNop())
        elif f in ["_objc_loadWeakRetained"]:
            if not len(instruction.params()) > 0: return
            ptr_size = instruction.params()[0].size
            instruction.replace_with(UCodeLoad(ptr_size, instruction.params()[0], instruction.destination()))
        elif f in ["_objc_release", "_objc_destroyWeak"]:
            instruction.replace_with(UCodeNop())
        elif f in ["_objc_storeStrong", "_objc_storeWeak"]:
            if not len(instruction.params()) > 0: return
            ptr_size = instruction.params()[0].size
            i1 = instruction.replace_with(UCodeStore(ptr_size, instruction.params()[0], instruction.params()[1]))
            if instruction.has_destination:
                i1.insert_after(UCodeMov(ptr_size, instruction.params()[1], instruction.destination()))


class UCodeRemoveInstruction(UCodeInstructionTransform):
    name = "Remove Instruction"
    def can_be_performed_on_instruction(self, instruction, bb, idx):
        return True

    def perform_on_instruction(self, instruction, bb, idx):
        del bb.instructions[idx]
