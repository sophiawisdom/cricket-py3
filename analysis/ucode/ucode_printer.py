class UCodePrinter:
    def __init__(self, function):
        self.function = function
        self.text = ""
        self.line_number = 0
        self.line_to_object_map = {}

    def line(self, s, o=None):
        self.text += s + "\n"
        if o is not None:
            self.line_to_object_map[self.line_number] = o
        self.line_number += 1

    def print_to_text(self, show_ucode_details=False, main_function=None):
        self.text = ""
        self.line_number = 0
        self.line_to_object_map = {}

        addr_to_asm_instr_map = {}
        if show_ucode_details:
            for bb in main_function.bbs:
                for instr in bb.instructions:
                    addr_to_asm_instr_map[instr.addr] = instr

        l = self.line

        l(";")
        l("; uCode for function " + self.function.name)
        l("; Starting at 0x%x" % self.function.addr)
        l(";")
        l("; Input parameters:")
        for p in self.function.input_parameters:
            l(";   %s" % (p))
        l(";")
        l("; Returns:")
        # l(";   %s %s (%d bytes) at %s" % (func.return_type.type, func.return_type.name, func.return_type.size, func.return_type.location))
        l(";")
        l("; Stack variables:")
        #for p in func.stack_variables:
        #    l(";   %s %s (%d bytes) at %s" % (p.type, p.name, p.size, p.location))
        l(";")
        l("")
        l("")

        if self.function.bbs is None: return (self.text, self.line_to_object_map)

        last_addr = -1
        for bb in self.function.bbs:
            l("")
            l("0x%x:        ; %s" % (bb.addr, str(bb)))

            if len(bb.instructions) == 0:
                l("        ; empty basic block")
                continue

            for instr in bb.instructions:
                if show_ucode_details and instr.addr != last_addr:
                    l("")
                    l("    ; uCode for instruction: %s" % addr_to_asm_instr_map[instr.addr])
                l("        " + str(instr), instr)
                last_addr = instr.addr

        return (self.text, self.line_to_object_map)
