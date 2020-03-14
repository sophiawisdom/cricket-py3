import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import *


class ForeachRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.parents = {}
        self.mutation_call = None

    def walk(self, node, parent=None):
        if isinstance(node, list):
            for idx, listitem in enumerate(node):
                self.walk(listitem, parent)
        elif isinstance(node, _ast.AST):
            self.parents[node] = parent
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.walk(subnode, node)

            if isinstance(node, ast2.Call):
                if isinstance(node.func, ast2.Name) and node.func.id == "_objc_enumerationMutation":
                    self.mutation_call = node

    def rewrite(self):
        self.walk(self.ast.root.body, self.ast.root)
        if self.mutation_call is None: return

        if not self.mutation_call in self.parents: return
        statement = self.parents[self.mutation_call]
        if not statement in self.parents: return
        if1 = self.parents[statement]
        if not if1 in self.parents: return
        while1 = self.parents[if1]
        if not while1 in self.parents: return
        while2 = self.parents[while1]
        if not while2 in self.parents: return
        if2 = self.parents[while2]

        if not isinstance(statement, ast2.Statement): return
        if not isinstance(if1, ast2.If): return
        if not isinstance(if2, ast2.If): return
        if not isinstance(while1, ast2.DoWhile): return
        if not isinstance(while2, ast2.DoWhile): return

        # find var
        if_in_while_idx = while1.body.index(if1)
        deref_idx = 0
        var = ast2.Name('i')
        for (idx, s) in enumerate(while1.body[if_in_while_idx+1:]):
            if isinstance(s, ast2.Assign):
                if isinstance(s.value, ast2.Dereference) and isinstance(s.targets[0], ast2.Name):
                    var = s.targets[0]
                    deref_idx = idx + if_in_while_idx + 2
                    break
        while1.body = while1.body[deref_idx:]

        # find collection
        collection = ast2.Name("collection")
        for (idx, s) in enumerate(self.ast.root.body):
            if isinstance(s, ast2.Assign):
                if isinstance(s.value, ast2.ObjCMessageSend) and isinstance(s.targets[0], ast2.Name):
                    if s.value.selector == "countByEnumeratingWithState:objects:count:":
                        collection = s.targets[0]
                        self.ast.root.body[idx] = ast2.Statement(ast2.Num(n=1))
                        break

        if2.test = ast2.Num(n=1)
        if2.body = [ast2.ForEach(typename='id', variable=var, source=collection, body=while1.body)]

