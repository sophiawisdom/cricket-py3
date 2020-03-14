from analysis.source import ast2
from analysis.source.ast_matcher import *


class AddressOfRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def callback(self, node):
        assert(isinstance(node, Sublist))
        assert(len(node.list) == 2)
        temp_var = node.list[0].targets[0]
        if not isinstance(temp_var, ast2.Name): return
        if not isinstance(node.list[1].value.pointer, ast2.Name): return
        if not node.list[1].value.pointer.id == temp_var.id: return

        orig_var = node.list[0].value.variable

        node.list[1].value = orig_var

    def rewrite(self):
        # Match a sequence like:
        #    temp = &(self)
        #    temp2 = *(temp)
        cond = Sublist([
            ast2.Assign(targets=[Any()], value=ast2.AddressOf(variable=Any()), decltype=None),
            ast2.Assign(targets=[Any()], value=ast2.Dereference(pointer=Any()), decltype=None)
        ])

        ast_matcher = AstMatcher()
        ast_matcher.match(self.ast.root, cond, self.callback)
