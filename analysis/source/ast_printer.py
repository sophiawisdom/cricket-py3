import ast
from analysis.tools.objc import format_msgSend, format_objc_function_declaration, format_c_function_declaration


class CCodePrinter(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0
        self.text = None
        self.line_to_object_map = None

    def execute(self, func):
        self.line_to_object_map = {}

        self.text = ""
        self.text += "// Generated %s code for function '%s'\n" % ("Obj-C" if func.is_objc() else "C", func.name)
        self.text += "\n"
        if func.is_objc():
            self.text += "#import <Foundation/Foundation.h>\n\n"
            for i in func.ast.globals:
                self.text += "%s" % self.visit(func.ast.globals[i])
            if len(func.ast.globals) != 0:
                self.text += "\n"
            self.text += "@interface %s : NSObject\n@end\n\n" % func.method.cls.name
            self.text += "@implementation %s\n\n" % func.method.cls.name

        self.text += self.visit(func.ast.root)

        if func.is_objc():
            self.text += "\n@end\n"

    def i(self):
        return " " * (self.indent_level * 4)

    def i_up(self):
        self.indent_level += 1

    def i_down(self):
        self.indent_level -= 1

    def generic_visit(self, node):
        print(("No visitor for " + str(node)))
        assert False

    def visit_list(self, l):
        s = ""
        for i in l:
            s += self.visit(i)
        return s

    # def visit_Compound(self, node):
    #     assert isinstance(node.body, list)
    #     s = self.i() + "{\n"
    #     self.i_up()
    #     s += "".join([("%s" % self.visit(st)) for st in node.body])
    #     self.i_down()
    #     s += "}\n"
    #     return s

    def visit_Name(self, node):
        return node.id

    def visit_Label(self, node):
        return "%s:\n%s" % (node.name, self.visit(node.body))

    def visit_Assign(self, node):
        if node.decltype is None:
            return self.i() + "%s = %s;\n" % (self.visit(node.targets), self.visit(node.value))
        else:
            return self.i() + "%s %s = %s;\n" % (node.decltype, self.visit(node.targets), self.visit(node.value))

    def visit_Increment(self, node):
        return "%s++" % self.visit(node.target)

    def visit_Call(self, node):
        return "%s(" % self.visit(node.func) + ", ".join([self.visit(p) for p in node.args]) + ")"

    def visit_ObjCMessageSend(self, node):
        return "[%s %s]" % (self.visit(node.receiver), format_msgSend(node.selector, [self.visit(a) for a in node.args]))

    def visit_ObjCString(self, node):
        return "@\"%s\"" % node.value

    def visit_ObjCSelector(self, node):
        return "@selector(%s)" % node.value

    def visit_If(self, node):
        s = self.i() + "if (%s) {\n" % self.visit(node.test)
        self.i_up()
        s += self.visit(node.body)
        if node.orelse:
            self.i_down()
            s += self.i() + "} else {\n"
            self.i_up()
            s += self.visit(node.orelse)
        self.i_down()
        s += self.i() + "}\n"
        return s

    def visit_While(self, node):
        s = self.i() + "while (%s) {\n" % self.visit(node.test)
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "}\n"
        return s

    def visit_DoWhile(self, node):
        s = self.i() + "do {\n"
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "} while (%s);\n" % self.visit(node.test)
        return s

    def visit_ForEach(self, node):
        s = self.i() + "for (%s %s in %s) {\n" % (node.typename, self.visit(node.variable), self.visit(node.source))
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "}\n"
        return s

    def visit_Compare(self, node):
        return "%s %s %s" % (self.visit(node.left), self.visit(node.ops), self.visit(node.comparators))

    def visit_Str(self, node):
        return node.s

    def visit_Add(self, node): return "+"
    def visit_Sub(self, node): return "-"
    def visit_Mult(self, node): return "*"
    def visit_Div(self, node): return "/"
    def visit_Mod(self, node): return "%"

    def visit_And(self, node): return "&&"
    def visit_Or(self, node): return "||"
    def visit_Xor(self, node): return "^"
    def visit_Shl(self, node): return "<<"
    def visit_Shr(self, node): return ">>"

    def visit_Lt(self, node): return "<"
    def visit_LtE(self, node): return "<="
    def visit_Gt(self, node): return ">"
    def visit_GtE(self, node): return ">="

    def visit_Num(self, node):
        return str(node.n)

    def visit_BinOp(self, node):
        return self.visit(node.left) + " " + self.visit(node.op) + " " + self.visit(node.right)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Statement(self, node):
        return self.i() + self.visit(node.expr) + ";\n"

    def visit_Goto(self, node):
        return self.i() + "goto " + node.label + ";\n"

    def visit_Asm(self, node):
        return self.i() + "__asm { %s };\n" % node.instr.canonicalsyntax

    def visit_Return(self, node):
        if node.value:
            return self.i() + "return %s;\n" % self.visit(node.value)
        else:
            return self.i() + "return;\n"

    def visit_Todo(self, node):
        return "<<TODO %s>>" % node.text

    def visit_Declaration(self, node):
        return self.i() + "%s %s;\n" % (node.typename, node.name)

    def visit_BoolOp(self, node):
        return (" %s " % self.visit(node.op)).join([self.visit(n) for n in node.values])


    def visit_Dereference(self, node):
        return "*(%s)" % self.visit(node.pointer)

    def visit_AddressOf(self, node):
        return "&(%s)" % self.visit(node.variable)

    def visit_FieldAccess(self, node):
        return "%s->%s" % (self.visit(node.object), node.field)

    def visit_ObjCFunctionDef(self, node):
        arg_types = [a.typename for a in node.args]
        arg_names = [a.name for a in node.args]
        s = "%s {\n" % format_objc_function_declaration(node.static, node.returntype, node.selector, arg_types, arg_names)
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "}\n"
        return s

    def visit_CFunctionDef(self, node):
        arg_types = [a.typename for a in node.args]
        arg_names = [a.name for a in node.args]
        s = "%s {\n" % format_c_function_declaration(node.returntype, node.name, arg_types, arg_names)
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "}\n"
        return s

    def visit_BlockDefinition(self, node):
        s = "^() {\n"
        self.i_up()
        s += self.visit(node.body)
        self.i_down()
        s += self.i() + "}"
        return s

    def visit_Equals(self, node):
        return "%s == %s" % (self.visit(node.left), self.visit(node.right))

    def visit_Negation(self, node):
        return "!(%s)" % (self.visit(node.value))
