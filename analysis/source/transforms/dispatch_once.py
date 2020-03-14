import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import *


class DispatchOnceRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)

                if isinstance(listitem, ast2.Statement) and isinstance(parent, ast2.If):
                    myif = parent
                    call = listitem.expr
                    if isinstance(call, ast2.Call):
                        if isinstance(call.func, ast2.Name):
                            if call.func.id == "_dispatch_once":
                                decl = ast2.Declaration(typename="static dispatch_once_t", name="onceToken")
                                args = [
                                    ast2.AddressOf(variable=ast2.Name(id="onceToken")),
                                    call.args[1],
                                ]
                                call = ast2.Statement(expr=ast2.Call(func=ast2.Name(id="dispatch_once"), args=args))
                                node[:] = [decl, call]
                                parent.test = ast2.Num(n=1)
                                break

        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

    def rewrite(self):
        self.walk(self.ast.root.body)
