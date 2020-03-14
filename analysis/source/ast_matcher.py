import _ast


class Any(object):
    pass


class Sublist(object):
    def __init__(self, list):
        self.list = list


class AstMatcher(object):
    def __init__(self):
        pass

    def compare1(self, node, cond):
        if cond.__class__ == Any:
            return True
        if cond.__class__ == Sublist:
            if node.__class__ == list:
                return True
        if node.__class__ == cond.__class__:
            return True
        if node.__class__ in [str, str] and cond.__class__ in [str, str]:
            return True

        return False

    def deep_compare_sublist(self, node, cond):
        # Sublist comparison.
        if len(cond.list) == 0: return True, Sublist([])

        for idx, item in enumerate(node):
            result, matched_node = self.deep_compare(item, cond.list[0])
            if result:
                rest_result, rest_sublist = self.deep_compare_sublist(node[idx + 1:], Sublist(cond.list[1:]))
                if rest_result:
                    return True, Sublist([item] + rest_sublist.list)
        return False, []

    def deep_compare(self, node, cond):
        if cond.__class__ == Any:
            return True, node

        if not self.compare1(node, cond):
            return False, None

        if isinstance(node, list):
            if cond.__class__ == Sublist:
                compare_result, compare_sublist = self.deep_compare_sublist(node, cond)
                return compare_result, compare_sublist
            else:
                # Compare all indices.
                for i in node:
                    if not self.deep_compare(i, cond):
                        return False, None
        elif isinstance(node, _ast.AST):
            if node.__class__ != cond.__class__:
                return False

            for field in node.__class__._fields:
                compare_result, compare_sublist = self.deep_compare(getattr(node, field), getattr(cond, field))
                if not compare_result:
                    return False, None

        return True, node

    def match(self, node, cond, callback):
        compare_result, matched_node = self.deep_compare(node, cond)
        if compare_result:
            callback(matched_node)
        else:
            if isinstance(node, list):
                for field in node:
                    self.match(field, cond, callback)
            elif isinstance(node, _ast.AST):
                for field in node.__class__._fields:
                    self.match(getattr(node, field), cond, callback)

    def replace(self, node, cond, callback):
        compare_result, match_node = self.deep_compare(node, cond)
        if compare_result:
            return True

        if isinstance(node, list):
            for idx, field in enumerate(node):
                if self.replace(field, cond, callback):
                    node[idx] = callback(node[idx])
        elif isinstance(node, _ast.AST):
            for field in node.__class__._fields:
                if self.replace(getattr(node, field), cond, callback):
                    oldval = getattr(node, field)
                    newval = callback(oldval)
                    setattr(node, field, newval)
