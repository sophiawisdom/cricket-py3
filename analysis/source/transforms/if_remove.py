import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import *


class IfRemoveRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)

                if isinstance(listitem, ast2.If):
                    myif = listitem
                    if isinstance(myif.test, ast2.Num):
                        if myif.test.n != 0:
                            node[idx:idx+1] = myif.body
                            break

        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

    def rewrite(self):
        self.walk(self.ast.root.body)
