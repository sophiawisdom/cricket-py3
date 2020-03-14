import hashlib
import os
import re
import pickle

from pycparser import c_ast, parse_file

from analysis.types import VariadicArguments, VoidType
from analysis.ucode.ucode import *
from analysis.ucode.ucode_utils import UCodeUtils


class CallPrototypesResolver:
    def __init__(self, arch, binary):
        self.arch = arch
        self.binary = binary
        self.prototypes = {}

        cache_file = "/var/tmp/cricket-" + "callprototypes.cache"
        files_to_load = [
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_objc_runtime.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_objc_runtime2.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_foundation.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_c_stdlib.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_posix.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_uikit.h",
            os.path.dirname(os.path.abspath(__file__)) + "/" + "callprototypes_dispatch.h",
        ]
        code_file = __file__

        checksum = hashlib.md5()
        for f in files_to_load:
            checksum.update(open(f, 'rb').read())
        checksum.update(open(code_file, 'rb').read())
        digest = checksum.hexdigest()

        try:
            (checksum_from_cache, prototypes_from_cache) = self.load_from_cache(cache_file, digest)
            if checksum_from_cache == digest:
                self.prototypes = prototypes_from_cache
                return
        except:
            pass  # Ignore all cache failures, just rebuild the cache.

        self.load_from_files(files_to_load, cache_file, digest)

    def load_from_cache(self, cache_file, digest):
        return pickle.load(open(cache_file, "rb"))

    def load_from_files(self, files, cache_file, checksum):
        for f in files:
            self.parse_header(f)

        pickle.dump((checksum, self.prototypes), open(cache_file, "wb"), -1)

    def parse_header(self, f):
        ast = parse_file(f, use_cpp=False)
        v = FuncDeclVisitor(self)
        v.visit(ast)

    def convert_type(self, p):
        if isinstance(p, c_ast.EllipsisParam): return VariadicArguments(0, "...")
        if isinstance(p, c_ast.Typename) or isinstance(p, c_ast.Decl):
            if isinstance(p.type, c_ast.PtrDecl):
                type_name = "void *"
            else:
                type_name = p.type.type.names[0]
        elif isinstance(p, c_ast.TypeDecl):
            type_name = p.type.names[0]
        elif isinstance(p, c_ast.PtrDecl):
            type_name = "void *"
        else:
            assert False
        return self.binary.types.get(type_name)

    def resolve_call(self, function, call_instruction):
        if len(call_instruction.params()) != 0:
            # Already resolved.
            assert call_instruction.has_unknown_operands
            if call_instruction.callee().name in ["_objc_msgSend", "_objc_msgSendSuper", "_objc_msgSendSuper2"]:
                if len(call_instruction.params()) == 2:
                    self.resolve_objc_msgsend(function, call_instruction)
                elif len(call_instruction.params()) >= 3:
                    variadic_index = len(call_instruction.params())
                    self.guess_parameters(function, call_instruction, call_instruction.bb, call_instruction.bb.instructions.index(call_instruction), variadic_index)
                else:
                    assert False
            elif call_instruction.callee().name == "_NSLog":
                self.resolve_format_string(function, call_instruction)
            elif call_instruction.callee().name == "_printf":
                self.resolve_format_string(function, call_instruction)
            return

        assert call_instruction.callee().name is not None
        assert call_instruction.callee().name[0] == "_"
        name = call_instruction.callee().name[1:]

        if not name in list(self.prototypes.keys()): return
        decl = self.prototypes[name]

        if len(decl.type.args.params) == 1 and isinstance(decl.type.args.params[0].type.type, c_ast.IdentifierType) and \
                        decl.type.args.params[0].type.type.names[0] == "void":
            decl.type.args.params = []

        param_types = []
        for p in decl.type.args.params:
            param_types.append(self.convert_type(p))

        return_type = self.convert_type(decl.type.type)

        self.process_call_with_params(function, call_instruction, param_types, return_type)

    def process_call_with_params(self, function, call_instruction, param_types, return_type):
        params = []
        ellipsis = False

        param_locations = self.arch.sema.call_arg_locations(param_types)
        already_found_params = call_instruction.params()

        for i in range(0, len(param_types)):
            t = param_types[i]
            (reg, subreg, offset) = param_locations[i]

            if i < len(already_found_params):
                params.append(already_found_params[i])
                continue

            ellipsis = False
            if isinstance(t, VariadicArguments):
                ellipsis = True
                continue

            if reg is None and subreg is None and offset is None:
                continue

            if offset is None:
                param = self.arch.sema.get_uregister(function, reg)
            else:
                param = function.get_sp_relative_register(offset, self.arch.bytes())
                #base_reg = function.get_native_register(self.arch.sema.sp_register())
                #param = UCodeCallStackParameter(self.arch.bytes(), base_reg, offset)
            params.append(param)

        returns_something = not isinstance(return_type, VoidType)

        callee = call_instruction.callee()
        # destination = (call_instruction.destination() if returns_something else None)
        destination = (self.arch.sema.get_uregister(function, self.arch.sema.retval_location(return_type)) if returns_something else None)
        new_instr = call_instruction.replace_with(UCodeCall(callee, destination, params))
        if not ellipsis:
            new_instr.has_unknown_operands = False
        new_instr.param_types = param_types
        new_instr.return_type = return_type

    def resolve_objc_msgsend(self, function, call_instruction):
        selector = call_instruction.params()[1]
        if not isinstance(selector, UCodeConstant): return
        assert selector.name is not None
        assert selector.name.startswith("_OBJC_SELECTOR_$_")
        sel = selector.name.replace("_OBJC_SELECTOR_$_", "")
        num_args = len(re.findall(":", sel))

        param_types = call_instruction.param_types
        assert isinstance(param_types[-1], VariadicArguments)
        param_types = param_types[:-1]

        variadic = False
        variadic_index = -1
        if sel.endswith("WithFormat:"):
            # [NSString stringWithFormat:], [NSExpression expressionWithFormat:], ...
            param_types.append(self.binary.types.id())
            param_types.append(VariadicArguments(0, None))
        elif sel in ["arrayWithObjects:", "initWithObjects:", "dictionaryWithObjectsAndKeys:", "initWithObjectsAndKeys:"]:
            # [NSArray arrayWithObjects:a,b,c,nil]
            param_types.append(self.binary.types.id())
            param_types.append(VariadicArguments(0, None))
        else:
            for i in range(0, num_args):
                param_types.append(self.binary.types.id())

        self.process_call_with_params(function, call_instruction, param_types, call_instruction.return_type)

        # params = call_instruction.params()
        # index = len(params)
        # offset = self.arch.bytes() * len(params)
        # for i in range(0, num_args):
        #     (reg_name, stack_offset) = self.arch.sema.arg_location(index, offset, variadic_index)
        #     if stack_offset is None:
        #         param = function.get_native_register(reg_name)
        #     else:
        #         base_reg = function.get_native_register(self.arch.sema.sp_register())
        #         param = UCodeCallStackParameter(self.arch.bytes(), base_reg, stack_offset)
        #     params.append(param)
        #     index += 1
        #     offset += self.arch.bytes()
        #
        # callee = call_instruction.callee()
        # destination = call_instruction.destination()
        # new_instr = call_instruction.replace_with(UCodeCall(callee, destination, params))
        # new_instr.has_unknown_operands = variadic

    def types_from_format_string(self, s):
        types = []
        matches = re.findall("(%(-|\\+| |0|#)?([0-9+-]+)?(\\.[0-9+-]+)?(hh|h|l|ll|L|z|j|t)?([diufFeEgGxXoscpaAn%@]))", s)
        for m in matches:
            t = m[5]
            if t in ["d", "i", "u", "x", "X", "o"]: types.append(self.binary.types.get("long"))
            elif t in ["f", "F", "e", "E", "g", "G", "a", "A"]: types.append(self.binary.types.get("double"))
            elif t in ["c"]: types.append(self.binary.types.get("char"))
            elif t in ["p"]: types.append(self.binary.types.get("void *"))
            elif t in ["@"]: types.append(self.binary.types.get("void *"))
            elif t in ["%"]: continue
            else: assert False
        return types

    def resolve_format_string(self, function, call_instruction):
        format_string = call_instruction.params()[0]
        if not isinstance(format_string, UCodeConstant): return
        if format_string.name is None: return
        assert format_string.name.startswith("_OBJC_CFSTRING_$_")
        cfstring = self.binary.cfstrings[format_string.value].string

        param_types = call_instruction.param_types
        # assert isinstance(param_types[-1], VariadicArguments)
        # param_types = param_types[:-1]

        # num_args = len(re.findall("%", cfstring))
        types = self.types_from_format_string(cfstring)
        if len(types) == 0:
            # No params.
            assert isinstance(param_types[-1], VariadicArguments)
            param_types = param_types[:-1]

        param_types = param_types + types

        self.process_call_with_params(function, call_instruction, param_types, call_instruction.return_type)

        # params = call_instruction.params()
        # index = len(params)
        # offset = self.arch.bytes() * len(params)
        # for i in range(0, num_args):
        #     (reg_name, stack_offset) = self.arch.sema.arg_location(index, offset, variadic_index=1)
        #     if stack_offset is None:
        #         param = function.get_native_register(reg_name)
        #     else:
        #         base_reg = function.get_native_register(self.arch.sema.sp_register())
        #         param = UCodeCallStackParameter(self.arch.bytes(), base_reg, stack_offset)
        #     params.append(param)
        #     index += 1
        #     offset += self.arch.bytes()
        #
        # callee = call_instruction.callee()
        # destination = call_instruction.destination()
        # new_instr = call_instruction.replace_with(UCodeCall(callee, destination, params))
        # new_instr.has_unknown_operands = False

    def guess_parameters(self, function, call_instruction, bb, idx, variadic_index=-1):
        if call_instruction.callee().name in ["_objc_msgSend", "_objc_msgSendSuper", "_objc_msgSendSuper2"]:
            return

        idx -= 1
        native_register_writes = []
        stack_args_offsets = []
        while idx >= 0:
            i = bb.instructions[idx]
            idx -= 1

            assert isinstance(i, UCodeInstruction)
            if i.has_destination:
                destination = i.destination()
                assert isinstance(destination, UCodeRegister)
                if destination.is_native():
                    native_register_writes.append(destination.name)
            if isinstance(i, UCodeStore):
                # Detect "*(sp + 0xc) = ...".
                ptr = i.pointer()
                (reg, offset) = UCodeUtils.find_stack_ptr_value(self.arch, ptr, i)
                if offset is not None:
                    stack_args_offsets.append(offset)
                    continue
            if isinstance(i, UCodeCall):
                # Stop at previous call.
                break

        (param_types, return_type) = self.arch.sema.guess_call_prototype(call_instruction, native_register_writes, stack_args_offsets, None)

        param_types = [self.binary.types.get(t) for t in param_types]
        return_type = self.binary.types.get(return_type)

        self.process_call_with_params(function, call_instruction, param_types, return_type)
        return
        #print native_register_writes
        #print stack_args_offsets

        # TODO remove, replace

        # params = call_instruction.params()
        index = len(params)
        offset = len(params) * self.arch.bytes()
        for i in range(0, 32):
            (reg_name, stack_offset) = self.arch.sema.arg_location(index, offset, variadic_index)
            if stack_offset is None:
                if reg_name not in native_register_writes: break
                param = function.get_native_register(reg_name)
            else:
                if stack_offset not in stack_args_offsets: break
                base_reg = function.get_native_register(self.arch.sema.sp_register())
                param = UCodeCallStackParameter(self.arch.bytes(), base_reg, stack_offset)
            params.append(param)
            index += 1
            offset += self.arch.bytes()

        #print params
        callee = call_instruction.callee()
        destination = call_instruction.destination()
        new_instr = call_instruction.replace_with(UCodeCall(callee, destination, params))
        new_instr.has_unknown_operands = False


class FuncDeclVisitor(c_ast.NodeVisitor):
    def __init__(self, resolver):
        self.resolver = resolver

    def visit_Decl(self, node):
        # print node.name
        self.resolver.prototypes[node.name] = node
