import _ast

from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any
from analysis.source.transforms.addressof import AddressOfRewriter
from analysis.source.transforms.decl_def import DeclarationToDefinitionRewriter
from analysis.source.transforms.dispatch_once import DispatchOnceRewriter
from analysis.source.transforms.expr_embed import ExpressionEmbedRewriter
from analysis.source.transforms.foreach import ForeachRewriter
from analysis.source.transforms.if_remove import IfRemoveRewriter
from analysis.source.transforms.propagate import PropagateRewriter
from analysis.source.transforms.unused_vars import UnusedVarsRewriter


class SimplifySourceRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def flatten_lists(self, node, cb):
        if isinstance(node, list):
            newlist = []
            for idx, listitem in enumerate(node):
                self.flatten_lists(listitem, cb)
                if isinstance(listitem, list):
                    newlist += listitem
                else:
                    newlist.append(listitem)
            newlist = cb(newlist)
            node[:] = newlist
        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                subnode = getattr(node, field)
                self.flatten_lists(subnode, cb)

    def list_removal(self, l):
        idx_to_remove = []
        for idx in range(0, len(l)):
            node = l[idx]
            if isinstance(node, ast2.Statement):
                if isinstance(node.expr, ast2.Num):
                    idx_to_remove.append(idx)

        return [node for (idx, node) in enumerate(l) if idx not in idx_to_remove]

    def rewrite(self):
        self.flatten_lists(self.ast.root.body, self.list_removal)

        # remove final return
        if isinstance(self.ast.root.body, list):
            last_stmt = self.ast.root.body[-1]
            if isinstance(last_stmt, ast2.Return):
                if last_stmt.value is None:
                    del(self.ast.root.body[-1])

        cond = ast2.BinOp(left=ast2.Name(id=Any()), op=Any(), right=ast2.Name(id=Any()))
        AstMatcher().replace(self.ast.root, cond, self.callback1)

        ForeachRewriter(self.ast).rewrite()
        AddressOfRewriter(self.ast).rewrite()
        PropagateRewriter(self.ast).rewrite()
        UnusedVarsRewriter(self.ast).rewrite()
        ExpressionEmbedRewriter(self.ast).rewrite()
        DeclarationToDefinitionRewriter(self.ast).rewrite()
        DispatchOnceRewriter(self.ast).rewrite()
        IfRemoveRewriter(self.ast).rewrite()

    def callback1(self, node):
        if not isinstance(node, ast2.BinOp): return node
        if not isinstance(node.left, ast2.Name): return node
        if not isinstance(node.right, ast2.Name): return node
        if node.left.id != node.right.id: return node

        if isinstance(node.op, ast2.And) or isinstance(node.op, ast2.Or):
            return node.left

        return node
