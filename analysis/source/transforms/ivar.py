from analysis.source import ast2
from analysis.source.ast_matcher import *


class IvarLoadRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def callback(self, node):
        assert(isinstance(node, Sublist))
        assert(len(node.list) == 2)
        ivar_pointer = node.list[0].targets[0]
        if not isinstance(ivar_pointer, ast2.Name): return
        if not isinstance(node.list[1].value.pointer, ast2.Name): return
        if not node.list[1].value.pointer.id == ivar_pointer.id: return

        obj_name = node.list[0].value.left
        ivar_name = node.list[0].value.right

        if not isinstance(ivar_name, ast2.Name): return
        if not ivar_name.id.startswith("_OBJC_IVAR_$_"): return
        n = ivar_name.id.replace("_OBJC_IVAR_$_", "")
        class_name, ivar_name = n.split(".")

        node.list[1].value = ast2.FieldAccess(object=obj_name, field=ivar_name)

    def rewrite(self):
        # Match a sequence like:
        #    temp = object_pointer + _OBJC_IVAR_$_MyClass.myLong;   // offset to ivar
        #    result = *(temp)
        cond = Sublist([
            ast2.Assign(targets=[Any()], value=ast2.BinOp(left=Any(), op=ast2.Add(), right=Any()), decltype=None),
            ast2.Assign(targets=[Any()], value=ast2.Dereference(pointer=Any()), decltype=None)
        ])

        ast_matcher = AstMatcher()
        ast_matcher.match(self.ast.root, cond, self.callback)


class IvarStoreRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def callback(self, node):
        assert(isinstance(node, Sublist))
        assert(len(node.list) == 2)
        ivar_pointer = node.list[0].targets[0]
        if not isinstance(ivar_pointer, ast2.Name): return
        if not isinstance(node.list[1].targets[0], ast2.Dereference): return
        if not isinstance(node.list[1].targets[0].pointer, ast2.Name): return
        if not node.list[1].targets[0].pointer.id == ivar_pointer.id: return

        obj_name = node.list[0].value.left
        ivar_name = node.list[0].value.right

        if not isinstance(ivar_name, ast2.Name): return
        if not ivar_name.id.startswith("_OBJC_IVAR_$_"): return
        n = ivar_name.id.replace("_OBJC_IVAR_$_", "")
        class_name, ivar_name = n.split(".")

        node.list[1].targets = [ast2.FieldAccess(object=obj_name, field=ivar_name)]

    def rewrite(self):
        # Match a sequence like:
        #    temp = object_pointer + _OBJC_IVAR_$_MyClass.myLong;   // offset to ivar
        #    *(temp) = value
        cond = Sublist([
            ast2.Assign(targets=[Any()], value=ast2.BinOp(left=Any(), op=ast2.Add(), right=Any()), decltype=None),
            ast2.Assign(targets=[ast2.Dereference(pointer=Any())], value=Any(), decltype=None)
        ])

        ast_matcher = AstMatcher()
        ast_matcher.match(self.ast.root, cond, self.callback)
