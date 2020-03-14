from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any


class MsgSendRewriter(object):
    def __init__(self, ast):
        self.ast = ast

    def callback(self, node):
        if not len(node.args) >= 2: return node
        if not isinstance(node.args[1], ast2.ObjCSelector): return node
        selector = node.args[1].value
        if node.func.id == "_objc_msgSend":
            receiver = node.args[0]
        elif node.func.id in ["_objc_msgSendSuper", "_objc_msgSendSuper2"]:
            receiver = ast2.Name("super")
        else:
            return node
        return ast2.ObjCMessageSend(receiver, selector, node.args[2:])

    def rewrite(self):
        # TODO other msgSends
        cond = ast2.Call(ast2.Name("_objc_msgSend"), Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)

        cond = ast2.Call(ast2.Name("_objc_msgSendSuper"), Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)

        cond = ast2.Call(ast2.Name("_objc_msgSendSuper2"), Any())
        AstMatcher().replace(self.ast.root, cond, self.callback)

        cond = ast2.Name(Any())
        AstMatcher().replace(self.ast.root, cond, self.callback_class_rewriting)

    def callback_class_rewriting(self, node):
        if not isinstance(node, ast2.Name): return node
        if not node.id.startswith("_OBJC_CLASS_$_"): return node
        clsname = node.id.replace("_OBJC_CLASS_$_", "")
        node.id = clsname

        return node
