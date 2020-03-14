from analysis.source import ast2
from analysis.source.ast_matcher import AstMatcher, Any


class EmbedBlocksRewriter(object):
    def __init__(self, ast):
        self.ast = ast
        self.captures = {}

    def callback_capture_usage(self, node):
        if not isinstance(node, ast2.BinOp): return node
        if not isinstance(node.left, ast2.Name): return node
        if not node.left.id == "block_literal": return node
        if not isinstance(node.right, ast2.Num): return node
        offset = node.right.n
        if not offset in self.captures: return node

        return ast2.AddressOf(variable=ast2.Name(id=self.captures[offset]))

    def callback_capture_usage2(self, node):
        if not isinstance(node, ast2.FieldAccess): return node
        if not isinstance(node.object, ast2.Name): return node
        if not node.object.id == "block_literal": return node

        field_name = node.field
        offset = int(field_name[4:], 16)
        if not offset in self.captures: return node

        return ast2.Name(id=self.captures[offset])

    def process_inner_block_root(self, root):
        cond = ast2.BinOp(left=ast2.Name("block_literal"), op=ast2.Add(), right=ast2.Num(n=Any()))
        result = AstMatcher().replace(root, cond, self.callback_capture_usage)

        cond = ast2.FieldAccess(object=ast2.Name("block_literal"), field=Any())
        result = AstMatcher().replace(root, cond, self.callback_capture_usage2)
        pass

    def callback_process_block_to_be_embedded(self, node):
        if not isinstance(node, ast2.Assign): return node
        target = node.targets[0]
        binop = node.value
        if not isinstance(binop, ast2.BinOp): return node
        if not isinstance(binop.left, ast2.Name): return node
        if not binop.left.id == "block_literal": return node
        if not isinstance(binop.right, ast2.Num): return node
        offset = binop.right.n

        node.value = ast2.AddressOf(variable=ast2.FieldAccess(object=ast2.Name("block_literal"), field="off_%x"%offset))

        return node

    def process_block_to_be_embedded(self, root):
        cond = ast2.Assign(targets=Any(), value=ast2.BinOp(left=ast2.Name("block_literal"), op=ast2.Add(), right=ast2.Num(n=Any())), decltype=None)
        result = AstMatcher().replace(root, cond, self.callback_process_block_to_be_embedded)
        pass

    def callback(self, node):
        if not isinstance(node, ast2.AddressOf): return node

        bd = self.ast.func.binary.find_block_descriptor_for_function(self.ast.func)
        if bd is None: return node
        bl = bd.uses[0]
        block_func = bl.invoke_func
        block_ast = block_func.ast
        if block_ast is None: return node

        root = block_ast.root
        if not isinstance(root, ast2.CFunctionDef): return node

        self.process_inner_block_root(root)

        self.did_replace = True
        return ast2.BlockDefinition(body=root.body)

    def callback2(self, node):
        if not isinstance(node, ast2.Assign): return node
        if not isinstance(node.targets[0], ast2.FieldAccess): return node
        if not isinstance(node.targets[0].object, ast2.Name): return node
        if not node.targets[0].object.id == "block_literal": return node

        return ast2.Statement(ast2.Num(1))

    def callback_find_captures(self, node):
        if not isinstance(node, ast2.Assign): return node
        if not isinstance(node.targets[0], ast2.FieldAccess): return node
        if not isinstance(node.targets[0].object, ast2.Name): return node
        if not node.targets[0].object.id == "block_literal": return node

        field_name = node.targets[0].field
        offset = int(field_name[4:], 16)

        if not isinstance(node.value, ast2.Name): return node

        self.captures[offset] = node.value.id

        return node

    def callback_remove_decl(self, node):
        if not isinstance(node, ast2.Declaration): return node
        if not node.name == "block_literal": return node

        return ast2.Statement(ast2.Num(1))

    def rewrite(self):
        self.process_block_to_be_embedded(self.ast.root)

        # Find captures
        cond = ast2.Assign(targets=[ast2.FieldAccess(object=ast2.Name("block_literal"), field=Any())], value=Any(), decltype=None)
        result = AstMatcher().replace(self.ast.root, cond, self.callback_find_captures)

        # Replace block literal with ^{ ... }
        self.did_replace = False
        cond = ast2.AddressOf(variable=ast2.Name("block_literal"))
        result = AstMatcher().replace(self.ast.root, cond, self.callback)

        # bind captures
        if self.did_replace:
            cond = ast2.Assign(targets=[ast2.FieldAccess(object=ast2.Name("block_literal"), field=Any())], value=Any(), decltype=None)
            result = AstMatcher().replace(self.ast.root, cond, self.callback2)

        # remove block_literal
        cond = ast2.Declaration(typename=Any(), name="block_literal")
        result = AstMatcher().replace(self.ast.root, cond, self.callback_remove_decl)
