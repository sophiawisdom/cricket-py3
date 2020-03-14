class AssemblyPrinter:
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

    def print_to_text(self):
        self.text = ""
        self.line_number = 0
        self.line_to_object_map = {}

        func = self.function
        l = self.line

        l(";")
        l("; Disassembly for function " + func.name)
        l("; Starting at 0x%x" % func.addr)
        l("; Stack frame size: %d bytes" % func.stack_frame_size)
        l(";")
        l("; Input parameters:")
        for p in func.parameters:
            l(";   %s %s (%d bytes) at %s" % (p.type, p.name, p.size, p.location))
        l(";")
        l("; Returns:")
        l(";   %s %s (%d bytes) at %s" % (func.returns.type, func.returns.name, func.returns.size, func.returns.location))
        l(";")
        l("; Stack variables:")
        for p in func.stack_variables:
            l(";   %s %s (%d bytes) at %s" % (p.type, p.name, p.size, p.location))
        l(";")
        l("")

        for instr in func.instructions:
            if func.bb_beginnings is not None:
                if instr.addr in func.bb_beginnings:
                    l("; ----------------------------------------------------------------------")
            if func.func_end is not None:
                if instr.addr == func.func_end:
                    l("; endp")

            s = instr.canonicalsyntax
            comment = ""
            if instr.pointer_hints is not None:
                pointer_hints_str = ", ".join([("Ref: 0x%x" % h) for h in instr.pointer_hints])
                comment += pointer_hints_str
            if comment != "":
                s = "%-60s ; %s" % (s, comment)

            l("0x%x        %s" % (instr.addr, s), instr)

        return (self.text, self.line_to_object_map)
