import ast

from analysis.source import ast2
from analysis.ucode.ucode import *


class UCodeConverter(object):
    def __init__(self, func):
        self.func = func
        self.locals = {}
        self.globals = {}

        self.parameter_names = {}
        for p in self.func.ufunction.input_parameters:
            self.parameter_names[p.register.name] = p.name

    def convert(self, instructions):
        res = []
        for idx, instr in enumerate(instructions):
            assert(isinstance(instr, UCodeInstruction))
            res.append(self.convert1(instr))
        return res

    def type_for_register(self, register_name):
        if register_name in ["zf", "of", "sf", "af", "pf", "cf", "branch_condition"]: return "BOOL";
        return "long"

    def get_variable(self, register):
        n = register.name
        if n in self.parameter_names:
            n = self.parameter_names[n]

        if n not in self.locals:
            self.locals[n] = ast2.Declaration(self.type_for_register(n), n)
        return ast2.Name(n)

    def declare_argument(self, register, t):
        n = register.name
        if n in self.parameter_names:
            n = self.parameter_names[n]

        if n not in self.locals:
            self.locals[n] = None  # Implicit declaration (function argument)
        return ast2.Name(n)

    def convert1(self, o):
        c = self.convert1
        if isinstance(o, UCodeAdd):
            return ast2.Assign(targets=[c(o.destination())], value=ast2.BinOp(c(o.source1()), ast2.Add(), c(o.source2())), decltype=None)
        elif isinstance(o, UCodeRet):
            if len(o.operands) == 0:
                return ast2.Return(None)
            else:
                assert(len(o.operands) == 1)
                return ast2.Return(c(o.operands[0]))
        elif isinstance(o, UCodeCall):
            call = ast2.Call(c(o.callee()), [c(p) for p in o.params()])
            if o.has_destination:
                return ast2.Assign(targets=[c(o.destination())], value=call, decltype=None)
            else:
                return ast2.Statement(expr=call)
        elif isinstance(o, UCodeMov):
            return ast2.Assign(targets=[c(o.destination())], value=c(o.source()), decltype=None)
        elif isinstance(o, UCodeRegister):
            return self.get_variable(o)
        elif isinstance(o, UCodeStore):
            deref = ast2.Dereference(c(o.pointer()))
            return ast2.Assign(targets=[deref], value=c(o.source()), decltype=None)
        elif isinstance(o, UCodeLoad):
            deref = ast2.Dereference(c(o.pointer()))
            return ast2.Assign(targets=[c(o.destination())], value=deref, decltype=None)
        elif isinstance(o, UCodeAddressOfLocal):
            return ast2.Assign(targets=[c(o.destination())], value=ast2.AddressOf(variable=c(o.source())), decltype=None)
        elif isinstance(o, UCodeSetMember):
            field = "off_%x" % o.offset()
            target = ast2.FieldAccess(object=c(o.destination()), field=field)
            return ast2.Assign(targets=[target], value=c(o.value()), decltype=None)
        elif isinstance(o, UCodeGetMember):
            field = "off_%x" % o.offset()
            value = ast2.FieldAccess(object=c(o.value()), field=field)
            return ast2.Assign(targets=[c(o.destination())], value=value, decltype=None)
        elif isinstance(o, UCodeBranch):
            return ast2.Statement(c(o.condition()))
        elif isinstance(o, UCodeSetFlag):
            if o.type == UCodeSetFlag.TYPE_ZERO and o.operation == UCodeSetFlag.OPERATION_SUB:
                comparison = ast2.Equals(left=c(o.source1()), right=c(o.source2()))
            elif o.type == UCodeSetFlag.TYPE_ZERO and o.operation == UCodeSetFlag.OPERATION_AND:
                comparison = ast2.BinOp(left=c(o.source1()), op=ast2.And(), right=c(o.source2()))
            elif o.type == UCodeSetFlag.TYPE_CARRY and o.operation == UCodeSetFlag.OPERATION_SUB:
                comparison = ast2.BinOp(left=c(o.source1()), op=ast2.Gt(), right=c(o.source2()))
            else:
                comparison = ast2.Todo(str(o))
            target = c(o.destination())
            return ast2.Assign(targets=[target], value=comparison, decltype=None)
        elif isinstance(o, UCodeNeg):
            target = c(o.destination())
            value = ast2.Negation(value=c(o.source1()))
            return ast2.Assign(targets=[target], value=value, decltype=None)
        elif isinstance(o, UCodeTruncate) or isinstance(o, UCodeExtend):
            target = c(o.destination())
            value = c(o.source())
            return ast2.Assign(targets=[target], value=value, decltype=None)
        elif isinstance(o, UCodeArithmeticOperation):
            target = c(o.destination())
            mnem_to_op = {"uADD": ast2.Add, "uSUB": ast2.Sub, "uMUL": ast2.Mult, "uDIV": ast2.Div, "uMOD": ast2.Mod,
                          "uAND": ast2.And, "uOR": ast2.Or, "uXOR": ast2.Xor, "uSHL": ast2.Shl, "uSHR": ast2.Shr}
            op = mnem_to_op[o.mnem()]()
            value = ast2.BinOp(left=c(o.source1()), op=op, right=c(o.source2()))
            return ast2.Assign(targets=[target], value=value, decltype=None)
        elif isinstance(o, UCodeInstruction):
            return ast2.Statement(ast2.Todo(str(o)))  # TODO
        elif isinstance(o, UCodeConstant):
            if not o.name:
                return ast2.Num(n=o.value)
            if o.name.startswith("_OBJC_CFSTRING_$_"):
                if o.value in self.func.binary.cfstrings:
                    return ast2.ObjCString(value=self.func.binary.cfstrings[o.value].string)
            if o.name.startswith("_OBJC_SELECTOR_$_"):
                return ast2.ObjCSelector(value=o.name.replace("_OBJC_SELECTOR_$_", ""))
            if o.name not in self.globals:
                self.globals[o.name] = ast2.Declaration("long", o.name)
            return ast2.Name(o.name)
        else:
            return ast2.Todo(str(o))  # TODO


class CFGWalker(object):
    def __init__(self, converter):
        self.converter = converter

    def visit(self, node):
        classname = node.__class__.__name__
        return self.__getattribute__("visit_" + classname)(node)

    def visit_CFGNode(self, node):
        return self.converter.convert(node.bb.instructions)

    def convert_to_bool_expression(self, stmt):
        return stmt.expr

    def visit_CFGIfElse(self, node):
        t = self.visit(node.test_node)
        b1 = self.visit(node.true_body_node) if node.true_body_node else []
        b2 = self.visit(node.false_body_node) if node.false_body_node else []
        if isinstance(t, list) and len(t) > 1:
            single_test_statement = t[-1]
            test_expression = self.convert_to_bool_expression(single_test_statement)
            return [t[0:-1], ast2.If(test_expression, b1, b2)]
        elif isinstance(t, list) and len(t) == 1:
            single_test_statement = t[0]
            test_expression = self.convert_to_bool_expression(single_test_statement)
            return ast2.If(test_expression, b1, b2)
        elif isinstance(t, ast2.BoolOp):
            return ast2.If(t, b1, b2)
        else:
            return ast2.If(t, b1, b2)


    def visit_CFGSequence(self, node):
        statements = []
        for n2 in node.nodes:
            statements.append(self.visit(n2))
        return statements

    def visit_CFGSwitch(self, node):
        return [ast2.Statement(ast2.Todo("switch"))]  # TODO

    def visit_CFGWhile(self, node):
        t = self.visit(node.test_node)
        l = self.visit(node.loop_body_node)
        return ast2.While(t, l, None)

    def visit_CFGDoWhile(self, node):
        t = self.visit(node.test_node) if node.test_node else []
        l = self.visit(node.loop_body_node) if node.loop_body_node else []

        if isinstance(t, list) and len(t) > 1:
            single_test_statement = t[-1]
            test_expression = self.convert_to_bool_expression(single_test_statement)
            return ast2.DoWhile(test_expression, [l] + t[0:-1], None)
        elif isinstance(t, list) and len(t) == 1:
            single_test_statement = t[0]
            test_expression = self.convert_to_bool_expression(single_test_statement)
            return ast2.DoWhile(test_expression, l, None)
        elif isinstance(t, ast2.BoolOp):
            return ast2.DoWhile(t, l, None)
        else:
            return ast2.DoWhile(t, l, None)

    def visit_CFGAndSequence(self, node):
        statements = []
        for n2 in node.nodes:
            statements.append(self.visit(n2))
        return ast.BoolOp(ast.And(), statements)


class AstBuilder(object):
    def __init__(self, func):
        self.func = func

    def convert(self):
        cfg = self.func.ufunction.cfg
        assert(len(cfg.unassigned_bbs_with_cfg_roots) == 1)
        cfg_root = cfg.unassigned_bbs_with_cfg_roots[0]

        converter = UCodeConverter(self.func)

        # Add inputs as locals
        for (idx, p) in enumerate(self.func.ufunction.input_parameters):
            t = None
            if idx in self.func.parameters:
                t = self.func.parameters[idx].type
            converter.declare_argument(p.register, t)

        walker = CFGWalker(converter)
        ast_body = walker.visit(cfg_root)

        ast_body = [l for l in list(converter.locals.values()) if l is not None] + ast_body

        #f = FunctionDef('a', None, ast_body, [])
        #print ast.dump(f)

        from analysis.binary import ObjCMethod

        returntype = self.func.returns.type

        if self.func.method is not None:
            args = [ast2.Declaration(typename=self.func.parameters[idx + 2].type.name, name=p.name) for (idx, p) in
                    enumerate(self.func.ufunction.input_parameters[2:])]
            classname = self.func.method.cls.name
            selector = self.func.method.name
            static = self.func.method.method_type == ObjCMethod.METHOD_TYPE_CLASS
            f = ast2.ObjCFunctionDef(classname=classname, selector=selector, args=args, body=ast_body, static=static, returntype=returntype)
        else:
            args = [ast2.Declaration(typename="long", name=p.name) for (idx, p) in
                    enumerate(self.func.ufunction.input_parameters[0:])]
            f = ast2.CFunctionDef(name=self.func.name, args=args, body=ast_body, returntype=returntype)

        return f, converter.globals

        #
        # statements = []
        # label = None
        # for bb in self.func.ufunction.bbs:
        #     label = "l_%x" % bb.addr
        #     for instr in bb.instructions:
        #         if label:
        #             # Mark first statement with the label
        #             statements.append(ast2.Label(label, ast2.Asm(instr)))
        #             label = None
        #         else:
        #             statements.append(ast2.Asm(instr))
        #
        #     if bb.terminator:
        #         stmt = None
        #         if self.arch.sema.is_unconditional_jump(bb.terminator):
        #             destination = "l_%x" % self.arch.sema.jump_destination(bb.terminator)
        #             stmt = ast2.Goto(destination)
        #         elif self.arch.sema.is_conditional_jump(bb.terminator):
        #             destination = "l_%x" % self.arch.sema.jump_destination(bb.terminator)
        #             if_ = ast2.If(self.arch.sema.jump_condition(bb.terminator), ast2.Goto(destination), None)
        #             stmt = if_
        #         elif self.arch.sema.is_return(bb.terminator):
        #             stmt = ast2.Return()
        #         else:
        #             # Huh?
        #             assert False
        #
        #         assert stmt
        #         if label:
        #             # Mark first statement with the label
        #             statements.append(ast2.Label(label, stmt))
        #             label = None
        #         else:
        #             statements.append(stmt)
        #
        # return ast2.Compound(statements)
