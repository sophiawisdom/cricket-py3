import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any
from analysis.source.transforms.addressof import AddressOfRewriter


class PropagateRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.var_to_def = {}
        self.var_to_use = {}

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)
        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

            if isinstance(node, ast2.Assign):
                self.found_assign(node)

            if isinstance(node, ast2.Name):
                if isinstance(parent, ast2.Assign) and node == parent.targets[0]:
                    pass
                else:
                    self.found_use(node)

    def found_assign(self, node):
        assert(isinstance(node, ast2.Assign))
        variable = node.targets[0]
        if not isinstance(variable, ast2.Name): return
        name = variable.id

        if name in self.var_to_def:
            # More than one definitions
            self.var_to_def[name] = None
            return

        self.var_to_def[name] = node

    def found_use(self, node):
        assert (isinstance(node, ast2.Name))
        name = node.id

        if name in self.var_to_use:
            # More than one use
            self.var_to_use[name] = None
            return

        self.var_to_use[name] = node

    def rewrite(self):
        self.walk(self.ast.root.body)

        # print self.var_to_def
        # print self.var_to_use

        cond = ast2.Name(id=Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)

        cond = ast2.Assign(value=Any(), targets=Any(), decltype=None)
        AstMatcher().replace(self.ast.root, cond, self.callback)

    def callback(self, node):
        if isinstance(node, ast2.Name):
            name = node.id

            if not name in self.var_to_use: return node
            if self.var_to_use[name] is None: return node
            if not name in self.var_to_def: return node
            if self.var_to_def[name] is None: return node

            if self.var_to_def[name].targets[0] == node: return node

            return self.var_to_def[name].value

        if isinstance(node, ast2.Assign):
            target = node.targets[0]
            if not isinstance(target, ast2.Name): return node
            name = target.id

            if not name in self.var_to_use: return node
            if self.var_to_use[name] is None: return node
            if not name in self.var_to_def: return node
            if self.var_to_def[name] is None: return node

            return ast2.Statement(ast2.Num(1))

        return node
