

import distorm3
import capstone


class AssemblyInstruction:
    def __init__(self, arch, addr, rawbytes, mnem, params):
        self.arch = arch
        self.addr = addr
        self.bytes = rawbytes
        self.mnem = mnem
        self.params = params
        self.canonicalsyntax = None
        self.csinstr = None
        self.bb = None
        #self.pattern = None
        self.pointer_hints = None
        self.jump_table = None
        self.jump_table_index_register = None

    def __str__(self):
        if self.canonicalsyntax:
            return "0x%08x: %s" % (self.addr, self.canonicalsyntax)
        else:
            return "0x%08x: %s %s     (non-canonical)" % (self.addr, self.mnem, self.params if self.params else "")

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo):
        # Don't copy csinstr.
        import copy
        result = self.__class__(None, None, None, None, None)
        memo[id(self)] = result
        for key, value in list(vars(self).items()):
            if key == "csinstr":
                result.csinstr = self.csinstr
            else:
                setattr(result, key, copy.deepcopy(value, memo))
        return result

    def canonicalize_distorm(self):
        decoded = distorm3.Decode(self.addr, self.bytes, self.arch.distorm_bits)
        assert len(decoded) == 1
        decoded = decoded[0]

        assert decoded[0] == self.addr
        assert decoded[1] == len(self.bytes)
        self.canonicalsyntax = decoded[2]

    def canonicalize_capstone(self):
        decoded = self.arch.capstone.disasm(self.bytes, self.addr)
        decoded = list(decoded)
        if len(decoded) == 1:
            decoded = decoded[0]
            self.csinstr = decoded

            assert decoded.address == self.addr
            #assert decoded.size == len(self.bytes) TODO
            self.canonicalsyntax = "%s %s" % (decoded.mnemonic, decoded.op_str)
        elif len(decoded) == 0:
            self.canonicalsyntax = None


class AssemblyDataInstruction(AssemblyInstruction):
    pass
