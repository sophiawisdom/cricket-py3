from analysis.asm.assembly import AssemblyInstruction


class OtoolReader(object):
    def __init__(self, arch, lines):
        self.arch = arch
        self.lines = lines

    def parseDisassemblyForMethod(self, symbol_name):
        line_index = 0
        instructions = []
        while True:
            line = self.lines[line_index]
            if line.startswith(symbol_name + ":"):
                break

            line_index += 1

        line_index += 1

        while True:
            line = self.lines[line_index]
            splitted = line.split("\t")

            if line.startswith("_main:") or len(splitted) == 1:
                break

            addr = int(splitted[0].strip(), 16)
            bytes = splitted[1].strip().decode('hex')

            if self.arch.otool_swap > 1:
                bytes = bytearray(bytes)
                assert len(bytes) % self.arch.otool_swap == 0
                for i in range(0, len(bytes), self.arch.otool_swap):
                    if self.arch.otool_swap == 2:
                        bytes[i], bytes[i + 1] = bytes[i + 1], bytes[i]
                    elif self.arch.otool_swap == 4:
                        bytes[i + 0], bytes[i + 3] = bytes[i + 3], bytes[i + 0]
                        bytes[i + 1], bytes[i + 2] = bytes[i + 2], bytes[i + 1]
                    else:
                        assert False
                bytes = str(bytes)

            mnem = splitted[2].strip()
            params = splitted[3].strip() if len(splitted) >= 4 else None

            if len(instructions) > 0 and instructions[len(instructions) - 1].mnem == "rep":
                addr = instructions[len(instructions) - 1].addr
                bytes = instructions[len(instructions) - 1].bytes + bytes
                mnem = "rep " + mnem
                del instructions[len(instructions) - 1]

            instr = AssemblyInstruction(self.arch, addr, bytes, mnem, params)
            instructions.append(instr)

            line_index += 1

        return instructions
