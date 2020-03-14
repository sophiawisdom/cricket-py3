from capstone import x86_const




class X86Meta2:
    def __init__(self, type, id, var_to_store, only_first):
        self.type = type
        self.only_first = only_first
        self.var_to_store = var_to_store
        self.id = id
        self.ops = []

    def __call__(self, *args, **kwargs):
        if self.only_first:
            setattr(self, self.var_to_store, args[0])
        else:
            setattr(self, self.var_to_store, args)
        return self


class X86Meta(type):
    def __getattr__(self, name):
        if hasattr(x86_const, "X86_INS_" + name):
            return X86Meta2("ins", getattr(x86_const, "X86_INS_" + name), "ops", False)
        elif hasattr(x86_const, "X86_REG_" + name):
            return X86Meta2("reg", None, "reg", True)(getattr(x86_const, "X86_REG_" + name))
        elif name == "IMM":
            return X86Meta2("imm", None, "imm", True)
        elif name == "ANY_IMM":
            return X86Meta2("imm", None, "imm", True)(None)
        elif name == "ANY_MEM":
            return X86Meta2("mem", None, "mem", True)(None)
        elif name == "ANY_REG":
            return X86Meta2("reg", None, "reg", True)(None)
        elif name == "REG":
            return X86Meta2("reg", None, "reg", True)
        else:
            assert False


class X86(object, metaclass=X86Meta):
    pass
