# Superclass for all types.
class Type:
    def __init__(self, byte_size, name):
        self.byte_size = byte_size
        self.name = name

    def __str__(self):
        return self.name


class PrimitiveType(Type):
    pass


class VoidType(Type):
    def __init__(self):
        Type.__init__(self, 0, "void")


class IntegerType(PrimitiveType):
    pass


class FloatingPointType(PrimitiveType):
    pass


class PointerType(Type):
    def __init__(self, byte_size, pointee_type):
        name = "%s *" % pointee_type.name
        self.pointee_type = pointee_type
        Type.__init__(self, byte_size, name)


class StructType(Type):
    def __init__(self, byte_size, name):
        Type.__init__(self, byte_size, name)


class ObjectType(PointerType):
    def __init__(self, byte_size, class_name):
        PointerType.__init__(self, byte_size, class_name)
        if class_name.name == "void":
            self.name = "id"


class VariadicArguments(Type):
    pass


# Type manager, holding all known types.
class TypeManager:
    types = {}

    def __init__(self, arch):
        self.arch = arch

        self.types["void"] = VoidType()

        self.types["BOOL"] = IntegerType(1, "BOOL")
        self.types["char"] = IntegerType(1, "char")
        self.types["short"] = IntegerType(2, "short")
        self.types["int"] = IntegerType(4, "int")
        self.types["long"] = IntegerType(self.arch.bytes(), "long")
        self.types["ptrdiff_t"] = self.types["long"]
        self.types["unsigned"] = self.types["long"]
        self.types["size_t"] = self.types["long"]
        self.types["pid_t"] = self.types["long"]

        self.types["float"] = FloatingPointType(4, "float")
        self.types["double"] = FloatingPointType(8, "double")

        self.types["void *"] = PointerType(self.arch.bytes(), self.types["void"])
        self.types["char *"] = PointerType(self.arch.bytes(), self.types["char"])
        self.types["SEL"] = PointerType(self.arch.bytes(), self.types["char"])
        self.types["id"] = ObjectType(self.arch.bytes(), self.types["void"])

        self.types["dispatch_block_t"] = self.types["void *"]
        self.types["CFTypeRef"] = self.types["void *"]

    def get(self, name):
        return self.types[name]

    def integer_of_size(self, size):
        if size == 1: return self.types["char"]
        elif size == 2: return self.types["short"]
        elif size == 4: return self.types["int"]
        elif size == 8 and self.arch.bytes() == 8: return self.types["long"]
        assert False

    def float_of_size(self, size):
        if size == 4: return self.types["float"]
        elif size == 8: return self.types["double"]
        assert False

    def void_pointer(self):
        return self.types["void *"]

    def id(self):
        return self.types["id"]

    def char_pointer(self):
        return self.types["char *"]

    def SEL(self):
        return self.types["SEL"]

    def create_or_get_struct(self, s):
        name = s.name
        byte_size = s.sizeof(is64bit=(self.arch.bytes() == 8))
        if name in self.types:
            assert self.types[name].byte_size == byte_size
        else:
            self.types[name] = StructType(byte_size, name)
        return self.types[name]
