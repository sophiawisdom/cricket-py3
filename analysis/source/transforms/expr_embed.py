import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import *


class ExpressionEmbedRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)

                if idx < len(node) - 1:
                    i1 = node[idx]
                    i2 = node[idx + 1]
                    if isinstance(i1, ast2.Assign) and isinstance(i1.value, ast2.ObjCMessageSend):
                        if isinstance(i2, ast2.Assign) and isinstance(i2.value, ast2.ObjCMessageSend):
                            self.callback(Sublist([i1, i2]))

        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

    def callback(self, node):
        assert(isinstance(node, Sublist))
        assert(len(node.list) == 2)
        assign1 = node.list[0]
        assign2 = node.list[1]
        if not isinstance(assign1, ast2.Assign): return
        if not isinstance(assign2, ast2.Assign): return
        if not isinstance(assign1.targets[0], ast2.Name): return
        temp_name = assign1.targets[0].id
        call1 = assign1.value
        call2 = assign2.value
        if not isinstance(call1, ast2.ObjCMessageSend): return
        if not isinstance(call2, ast2.ObjCMessageSend): return
        sel1 = call1.selector
        sel2 = call2.selector

        if not sel1 == "alloc": return
        if not sel2.startswith("init"): return

        call2.receiver = call1
        assign1.targets = []

    def rewrite(self):
        # Match a sequence like:
        #    temp = [object alloc]
        #    result = [temp init...]
        self.walk(self.ast.root.body)

        cond = ast2.Assign(targets=Any(), value=Any(), decltype=None)
        AstMatcher().replace(self.ast.root, cond, self.callback_remove)


    def callback_remove(self, node):
        if not isinstance(node, ast2.Assign): return node
        if node.targets == []: return ast2.Statement(ast2.Num(1))

        return node
