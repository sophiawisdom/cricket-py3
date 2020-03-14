import _ast

from analysis.source import ast2
from analysis.source.ast2 import ObjCMessageSend
from analysis.source.ast_matcher import AstMatcher, Any
from analysis.source.transforms.addressof import AddressOfRewriter


class TypeRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.decls = {}

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)
        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

            if isinstance(node, ast2.Assign):
                if isinstance(node.targets[0], ast2.Name) and node.decltype is not None:
                    self.decls[node.targets[0].id] = node.decltype


    def rewrite(self):
        self.walk(self.ast.root, None)

        cond = ast2.Assign(value=Any(), targets=Any(), decltype=Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)


    def callback(self, node):
        if isinstance(node, ast2.Assign):
            target = node.targets[0]
            if not isinstance(target, ast2.Name): return node
            if node.decltype is None: return node

            if isinstance(node.value, ast2.ObjCMessageSend):
                node.decltype = "id"
            elif isinstance(node.value, ast2.Name):
                othername = node.value.id
                if othername in self.decls:
                    node.decltype = self.decls[othername]

            return node

        return node
