import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any
from analysis.source.transforms.addressof import AddressOfRewriter


class UnusedVarsRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.var_to_decl = {}
        self.var_to_use = {}

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)
        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

            if isinstance(node, ast2.Declaration):
                self.found_decl(node)

            if isinstance(node, ast2.Name):
                self.found_use(node)

    def found_decl(self, node):
        assert(isinstance(node, ast2.Declaration))
        name = node.name
        self.var_to_decl[name] = node

    def found_use(self, node):
        assert (isinstance(node, ast2.Name))
        name = node.id
        self.var_to_use[name] = node

    def rewrite(self):
        self.walk(self.ast.root.body)

        cond = ast2.Declaration(name=Any(), typename=Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)

    def callback(self, node):
        if not isinstance(node, ast2.Declaration): return node
        name = node.name

        if not name in self.var_to_decl: return node
        if not name in self.var_to_use:
            return ast2.Statement(ast2.Num(1))

        return node
