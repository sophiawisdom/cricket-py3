import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any
from analysis.source.transforms.addressof import AddressOfRewriter


class DeclarationToDefinitionRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.var_decls = {}
        self.var_use = {}

    def walk(self, node, parent=None):
        if isinstance(node, list):
            var_decl_idx = {}
            var_assigns = {}
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)

                if isinstance(listitem, ast2.Declaration):
                    var_decl_idx[listitem.name] = idx

                if isinstance(listitem, ast2.Assign):
                    if isinstance(listitem.targets[0], ast2.Name):
                        if not listitem.targets[0].id in var_assigns:
                            var_assigns[listitem.targets[0].id] = listitem

            for name in var_assigns:
                if not name in var_decl_idx: continue
                var_assigns[name].decltype = node[var_decl_idx[name]].typename
                node[var_decl_idx[name]] = ast2.Statement(ast2.Num(1))
                del(var_decl_idx[name])

        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)



    def rewrite(self):
        self.walk(self.ast.root.body)
