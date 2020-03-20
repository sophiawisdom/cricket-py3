from analysis.ucode.ucode import *


class UCodeUtils:
    @staticmethod
    def find_stack_ptr_value(arch, ptr, mem_instruction):
        assert isinstance(ptr, UCodeRegister)
        if arch.sema.sp_register() == ptr.name:
            return (ptr, 0)
        to_add = 0
        while len(mem_instruction.definitions(ptr)) == 1:
            add_instruction = mem_instruction.definitions(ptr)[0]
            if not isinstance(add_instruction, UCodeAdd): return (None, None)
            # assert isinstance(add_instruction, UCodeAdd) # disabling this to just get it to work...
            assert isinstance(add_instruction.source1(), UCodeRegister)
            assert isinstance(add_instruction.source2(), UCodeConstant)
            to_add += add_instruction.source2().value
            if arch.sema.sp_register() == add_instruction.source1().name:
                return (add_instruction.source1(), to_add)
            ptr = add_instruction.source1()
            mem_instruction = add_instruction
        return (None, None)
