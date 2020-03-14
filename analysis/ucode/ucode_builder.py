from analysis.ucode.ucode import *


class UCodeBuilder:
    def __init__(self, function):
        self.function = function

    def build_ucode(self):

        # Sanity check.
        for bb in self.function.bbs:
            for instr in bb.instructions:
                assert instr.bb == bb


        self.function.ufunction = UCodeFunction(self.function.arch.bits / 8, self.function.name, self.function.addr)
        ufunction = self.function.ufunction
        ufunction.bbs = []
        ufunction.stack_frame_base_register = self.function.ufunction.get_native_register(self.function.arch.sema.base_register())
        ufunction.stack_pointer_register = self.function.ufunction.get_native_register(self.function.arch.sema.sp_register())
        ufunction.pc_register = self.function.ufunction.get_native_register(self.function.arch.sema.pc_register())

        ufunction.input_parameters = []
        for i in self.function.parameters:
            item = UCodeStackFrameItem()
            item.size = i.size
            item.base_offset = i.offset
            item.register = ufunction.get_custom_register(i.name, i.size)
            ufunction.stack_frame_layout.append(item)
            if i.is_register:
                inp = UCodeRegisterInput()
                inp.name = i.name
                inp.size = i.size
                inp.register = self.function.arch.sema.get_uregister(ufunction, i.register)
                ufunction.input_parameters.append(inp)
            else:
                inp = UCodeStackInput()
                inp.name = i.name
                inp.base_offset = i.offset
                inp.size = i.size
                inp.register = None
                ufunction.input_parameters.append(inp)

        for i in self.function.stack_variables:
            item = UCodeStackFrameItem()
            item.size = i.size
            item.base_offset = i.offset
            item.sp_offset = i.sp_offset
            item.register = ufunction.get_custom_register(i.name, i.size)
            ufunction.stack_frame_layout.append(item)

        bb_to_ubb = {}
        for bb in self.function.bbs:
            ucode_bb = UCodeBasicBlock()
            ucode_bb.number = bb.number
            ucode_bb.addr = bb.addr
            bb_to_ubb[bb] = ucode_bb
            self.function.ufunction.bbs.append(ucode_bb)

        for bb in self.function.bbs:
            ucode_bb = bb_to_ubb[bb]
            ucode_bb.succs = set([bb_to_ubb[bb2] for bb2 in bb.succs])
            ucode_bb.preds = set([bb_to_ubb[bb2] for bb2 in bb.preds])

        for bb in self.function.bbs:
            ucode_bb = bb_to_ubb[bb]
            ucode = []
            for instr in bb.instructions:
                if isinstance(instr, UCodeInstruction):
                    ucode.append(instr)
                else:
                    ucode_instrs = self.function.arch.sema.generate_ucode(self.function, instr)
                    for ucode_instr in ucode_instrs:
                        ucode_instr.addr = instr.addr
                        ucode_instr.bb = ucode_bb
                        ucode.append(ucode_instr)

            ucode_bb.instructions = ucode
