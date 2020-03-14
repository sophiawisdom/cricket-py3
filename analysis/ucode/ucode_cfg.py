from copy import copy
from analysis.ucode.ucode import UCodeSwitch


class CFGGraph:
    def __init__(self, function):
        self.function = function
        self.next_number = 0

        self.bb_to_node = {}
        # self.unassigned_bbs = []
        self.unassigned_bbs_with_cfg_roots = []

        for bb in self.function.bbs:
            node = CFGNode(self, self.next_number)
            self.next_number += 1

            node.bb = bb
            self.bb_to_node[bb] = node
            # self.unassigned_bbs.append(node)
            self.unassigned_bbs_with_cfg_roots.append(node)

        for bb in self.function.bbs:
            for succ_bb in bb.succs: self.bb_to_node[bb].succs.add(self.bb_to_node[succ_bb])
            for pred_bb in bb.preds: self.bb_to_node[bb].preds.add(self.bb_to_node[pred_bb])

        self.sanity_check()

    def n(self):
        res = self.next_number
        self.next_number += 1
        return res

    def dump(self):
        s = "; CFG Dump\n"
        s += "; Root nodes: %d.\n" % len(self.unassigned_bbs_with_cfg_roots)
        s += ";\n\n"
        for cfg_node in self.unassigned_bbs_with_cfg_roots:
            s += "Root Node (%s):\n" % cfg_node.__class__.__name__
            s += cfg_node.to_str(True)
        return s

    def sanity_check_succs_preds(self):
        for bb in self.unassigned_bbs_with_cfg_roots:
            for pred_bb in bb.preds:
                assert bb in pred_bb.succs
            for succ_bb in bb.succs:
                assert bb in succ_bb.preds

    def sanity_check_no_dups(self, nodes, found_nodes):
        if nodes is None: return
        for node in nodes:
            if node in found_nodes:
                assert False, "Node already present in tree!"
            found_nodes |= set([node])
            self.sanity_check_no_dups(node.children, found_nodes)

    def sanity_check(self):
        self.sanity_check_succs_preds()
        self.sanity_check_no_dups(self.unassigned_bbs_with_cfg_roots, set())

    def replace_nodes_with_new_node(self, entry_node, nodes, exit_node, new_node):
        for pred_node in entry_node.preds:
            pred_node.succs.remove(entry_node)
            pred_node.succs.add(new_node)

        if exit_node is not None:
            exit_node.preds = (exit_node.preds - nodes - set([entry_node])) | set([new_node])
            new_node.preds = entry_node.preds - nodes - set([entry_node])
            new_node.succs = set([exit_node])
        else:
            new_node.preds = entry_node.preds - nodes - set([entry_node])
            new_node.succs = set([])

        for n in nodes:
            n.succs = None
            n.preds = None
            # self.unassigned_bbs.remove(n)
            self.unassigned_bbs_with_cfg_roots.remove(n)

        entry_node.succs = None
        entry_node.preds = None
        self.unassigned_bbs_with_cfg_roots.remove(entry_node)

        self.unassigned_bbs_with_cfg_roots.append(new_node)

    # (any)* => test_node
    # test_node => detour_node => exit_node
    # test_node => exit_node
    # (any)* => exit_node => (any)*
    def convert_if(self, test_node, check_only=False):
        if not len(test_node.succs) == 2: return False
        (detour_node, exit_node) = list(test_node.succs)
        if len(detour_node.succs) != 1 or not list(detour_node.succs)[0] == exit_node:
            (detour_node, exit_node) = (exit_node, detour_node)

        if not detour_node.succs == set([exit_node]): return False
        if not detour_node.preds == set([test_node]): return False
        if not test_node in exit_node.preds: return False
        if not detour_node in exit_node.preds: return False

        if check_only: return True

        new_node = CFGIfElse(self, self.n())
        new_node.test_node = test_node
        new_node.true_body_node = detour_node
        new_node.false_body_node = None
        new_node.parent = None
        new_node.children = [test_node, detour_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(test_node, set([detour_node]), exit_node, new_node)
        self.sanity_check()

        return True

    # (any)* => test_node
    # test_node => left_node => exit_node
    # test_node => right_node => exit_node
    # exit_node => (any)*
    def convert_if_else(self, test_node, check_only=False):
        if not len(test_node.succs) == 2: return False
        (left_node, right_node) = list(test_node.succs)
        if not left_node.preds == set([test_node]): return False
        if not right_node.preds == set([test_node]): return False
        if not left_node.succs == right_node.succs: return False
        if not len(left_node.succs) == 1: return False
        exit_node = list(left_node.succs)[0]

        if not exit_node.preds.issuperset(set([left_node, right_node])): return False

        if check_only: return True

        new_node = CFGIfElse(self, self.n())
        new_node.test_node = test_node
        new_node.true_body_node = left_node
        new_node.false_body_node = right_node
        new_node.parent = None
        new_node.children = [test_node, left_node, right_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(test_node, set([left_node, right_node]), exit_node, new_node)
        self.sanity_check()

        return True

    # (any)* => test_node
    # test_node <=> loop_node
    # test_node => exit_node
    # exit_node => (any)*
    def convert_while(self, test_node, check_only=False):
        if not len(test_node.succs) == 2: return False
        (loop_node, exit_node) = list(test_node.succs)
        if len(loop_node.succs) != 1 or not list(loop_node.succs)[0] == test_node:
            (loop_node, exit_node) = (exit_node, loop_node)

        if not len(loop_node.succs) == 1: return False
        if not list(loop_node.succs)[0] == test_node: return False
        if not len(loop_node.preds) == 1: return False
        if not list(loop_node.preds)[0] == test_node: return False
        if not len(exit_node.preds) == 1: return False
        if not list(exit_node.preds)[0] == test_node: return False

        if check_only: return True

        new_node = CFGWhile(self, self.n())
        new_node.test_node = test_node
        new_node.loop_body_node = loop_node
        new_node.parent = None
        new_node.children = [test_node, loop_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(test_node, set([loop_node]), exit_node, new_node)
        self.sanity_check()

        return True

    def convert_infinite_loop(self, loop_node, check_only=False):
        if not len(loop_node.succs) == 1: return False
        test_node = list(loop_node.succs)[0]
        if not len(test_node.succs) == 1: return False

        if not test_node.succs == set([loop_node]): return False
        if not test_node.preds == set([loop_node]): return False
        if not loop_node.succs == set([test_node]): return False

        if check_only: return True

        new_node = CFGDoWhile(self, self.n())
        new_node.loop_body_node = loop_node
        new_node.test_node = test_node
        new_node.parent = None
        new_node.children = [test_node, loop_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(loop_node, set([test_node]), None, new_node)
        self.sanity_check()

        return True


    # (any)* => loop_node => exit_node
    # loop_node <=> loop_node
    def convert_single_bb_while(self, loop_node, check_only=False):
        if not len(loop_node.succs) == 2: return False
        if not loop_node in loop_node.succs: return False
        if not loop_node in loop_node.preds: return False

        l = list(loop_node.succs)
        (_, exit_node) = l
        if exit_node == loop_node: (exit_node, _) = l

        if not exit_node != loop_node: return False

        if check_only: return True

        new_node = CFGDoWhile(self, self.n())
        new_node.test_node = loop_node
        new_node.loop_body_node = None
        new_node.parent = None
        new_node.children = [loop_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(loop_node, set([]), exit_node, new_node)
        self.sanity_check()

        return True

    # (any)* => loop_node
    # loop_node <=> test_node
    # test_node => exit_node
    def convert_do_while(self, loop_node, check_only=False):
        if not len(loop_node.succs) == 1: return False
        test_node = list(loop_node.succs)[0]
        if not len(test_node.succs) == 2: return False

        l = list(test_node.succs)
        (_, exit_node) = l
        if exit_node == loop_node: (exit_node, _) = l

        if not exit_node != loop_node: return False
        if not exit_node != test_node: return False

        if not test_node.succs == set([loop_node, exit_node]): return False
        if not test_node.preds == set([loop_node]): return False

        if check_only: return True

        new_node = CFGDoWhile(self, self.n())
        new_node.test_node = test_node
        new_node.loop_body_node = loop_node
        new_node.parent = None
        new_node.children = [loop_node, test_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(loop_node, set([test_node]), exit_node, new_node)
        self.sanity_check()

        return True

    # (any)* => first_node => ... => last_node (=> exit_node)
    def convert_sequence(self, first_node, check_only=False):
        if not len(first_node.succs) == 1: return False
        next_node = list(first_node.succs)[0]
        if not len(next_node.preds) == 1: return False
        if not list(next_node.preds)[0] == first_node: return False
        nodes = [first_node, next_node]

        if len(next_node.succs) == 1:
            exit_node = list(next_node.succs)[0]
        elif len(next_node.succs) == 0:
            exit_node = None  # RET block
        else:
            if not False: return False

        if exit_node in nodes: return False

        while True:
            last_node = nodes[-1]
            if len(last_node.succs) != 1: break
            next_node = list(last_node.succs)[0]
            if len(next_node.preds) != 1: break
            if list(next_node.preds)[0] != last_node: break
            if len(next_node.succs) > 1: break
            if next_node.succs.intersection(set(nodes)) != set(): break

            # Add node into list.
            nodes.append(next_node)
            if len(next_node.succs) == 1:
                exit_node = list(next_node.succs)[0]
            elif len(next_node.succs) == 0:
                exit_node = None  # RET block
            else:
                assert False

        last_node = nodes[-1]

        if check_only: return True

        new_node = CFGSequence(self, self.n())
        new_node.nodes = list(nodes)
        new_node.parent = None
        new_node.children = list(nodes)
        new_node.bb = None
        new_node.assigned = True

        for node in nodes[1:-1]:
            node.succs = None
            node.preds = None
            # self.unassigned_bbs.remove(node)
            self.unassigned_bbs_with_cfg_roots.remove(node)

        self.replace_nodes_with_new_node(first_node, set([last_node]), exit_node, new_node)
        self.sanity_check()

        return True

    # (any)* => test_node => exit_node
    # test_node => return_node
    # return_node => (empty)
    # exit_node => (any)*
    def convert_early_return(self, test_node, check_only=False):
        if not len(test_node.succs) == 2: return False
        (return_node, exit_node) = list(test_node.succs)
        if len(return_node.succs) != 0:
            (return_node, exit_node) = (exit_node, return_node)

        if not len(return_node.succs) == 0: return False
        if not return_node.preds == set([test_node]): return False

        if check_only: return True

        new_node = CFGIfElse(self, self.n())
        new_node.test_node = test_node
        new_node.true_body_node = return_node
        new_node.false_body_node = None
        new_node.parent = None
        new_node.children = [test_node, return_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(test_node, set([return_node]), exit_node, new_node)
        self.sanity_check()

        return True

    # test_node => fail_node
    # test_node => next_test_node => fail_node
    # test_node => next_test_node => ... => fail_node
    # ... => next_test_node => success_node
    # fail_node => exit_node
    # success_node => exit_node
    def convert_multi_if(self, test_node, check_only=False):
        all_test_nodes = [test_node]
        success_node = None
        if not len(test_node.succs) == 2: return False
        (next_test_node, fail_node) = list(test_node.succs)
        if len(fail_node.succs) != 1:
            (fail_node, next_test_node) = (next_test_node, fail_node)

        if len(fail_node.succs) != 1: return False
        exit_node = list(fail_node.succs)[0]
        # if exit_node in next_test_node.succs: return False  # This is a regular if-else.

        while True:
            if exit_node in next_test_node.succs:
                # Found an end.
                if len(next_test_node.succs) == 1:
                    success_node = next_test_node
                else:
                    assert len(next_test_node.succs) == 2
                    if fail_node in next_test_node.succs:
                        all_test_nodes.append(next_test_node)
                        success_node = None
                    else:
                        (success_node, assumed_exit_node) = list(next_test_node.succs)
                        if assumed_exit_node != exit_node:
                            (success_node, assumed_exit_node) = (assumed_exit_node, success_node)
                break

            if not fail_node in next_test_node.succs: return False
            if not len(next_test_node.succs) == 2: return False
            all_test_nodes.append(next_test_node)

            (next_next_test_node, assumed_fail_node) = list(next_test_node.succs)
            if assumed_fail_node != fail_node:
                (next_next_test_node, assumed_fail_node) = (assumed_fail_node, next_next_test_node)

            if not assumed_fail_node == fail_node: return False
            next_test_node = next_next_test_node

        if success_node is not None:
            if not success_node.succs == set([exit_node]): return False

        if not fail_node.succs == set([exit_node]): return False
        if not fail_node.preds == set(all_test_nodes): return False

        if not len(all_test_nodes) > 1: return False

        for (idx, n) in enumerate(all_test_nodes):
            if idx == 0: continue
            assert n.preds == set([all_test_nodes[idx-1]])

        if check_only: return True

        condition_node = CFGAndSequence(self, self.n())
        condition_node.nodes = list(all_test_nodes)
        condition_node.parent = None
        condition_node.children = list(all_test_nodes)
        condition_node.bb = None
        condition_node.assigned = True

        new_node = CFGIfElse(self, self.n())
        new_node.test_node = condition_node
        new_node.true_body_node = success_node
        new_node.false_body_node = fail_node
        new_node.parent = None
        new_node.children = [condition_node, success_node, fail_node] if success_node is not None else [condition_node, fail_node]
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(test_node, set(all_test_nodes + [fail_node] + ([success_node] if success_node is not None else [])) - set([test_node]), exit_node, new_node)
        self.sanity_check()

        return True

    def convert_duplicate_exit_node(self, exit_node, check_only=False):
        if not len(exit_node.succs) == 0: return False
        n = len(exit_node.preds)
        if not n > 1: return False

        if check_only: return True

        for pred_bb in exit_node.preds:
            new_node = exit_node.duplicate(self.n())
            new_node.preds = set([pred_bb])
            pred_bb.succs -= set([exit_node])
            pred_bb.succs |= set([new_node])
            self.unassigned_bbs_with_cfg_roots.append(new_node)

        self.unassigned_bbs_with_cfg_roots.remove(exit_node)
        self.sanity_check()

        return True

    def convert_switch(self, switch_node, check_only=False):
        if not len(switch_node.succs) > 2: return False
        assert isinstance(switch_node.bb.instructions[-1], UCodeSwitch)

        exit_node = list((list(switch_node.succs)[0]).succs)[0]
        case_nodes = list(switch_node.succs)

        for succ_bb in case_nodes:
            assert succ_bb.preds == set([switch_node])
            assert succ_bb.succs == set([exit_node])

        if check_only: return True

        new_node = CFGSwitch(self, self.n())
        new_node.test_node = switch_node
        new_node.case_nodes = list(case_nodes)
        new_node.parent = None
        new_node.children = [switch_node] + case_nodes
        new_node.bb = None
        new_node.assigned = True

        self.replace_nodes_with_new_node(switch_node, set(case_nodes), exit_node, new_node)
        self.sanity_check()

        return True


class CFGNode:
    def __init__(self, cfg, number):
        self.cfg = cfg
        self.number = number
        self.parent = None
        self.children = None
        self.bb = None
        self.assigned = False
        self.succs = set()
        self.preds = set()

    def __str__(self):
        return "CFGNode #%d (%s)" % (self.number, self.__class__.__name__)

    def __repr__(self):
        return self.__str__()

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        return new_node

    def _to_str_bb(self, bb, detailed=False, indent=0):
        s = ""
        ellipsis_emitted = False
        count = len(bb.instructions)
        for (idx, instr) in enumerate(bb.instructions):
            if not detailed:
                if idx not in [0, count - 1]:
                    if not ellipsis_emitted:
                        s += (" " * indent) + "...\n"
                        ellipsis_emitted = True
                    continue
            istring = str(instr)
            s += (" " * indent) + istring + "\n"
        return s

    def _to_str_node(self, node, detailed=False, indent=0):
        if node.bb is not None:
            return node._to_str_bb(node.bb, detailed, indent)
        elif isinstance(node, CFGIfElse):
            s = (" " * indent) + "CFGIFElse:" + "\n"
            s += (" " * indent) + "Test Node:" + "\n"
            s += node._to_str_node(node.test_node, detailed, indent + 4)
            if node.true_body_node is not None:
                s += (" " * indent) + "True Body Node:" + "\n"
                s += node._to_str_node(node.true_body_node, detailed, indent + 4)
            if node.false_body_node is not None:
                s += (" " * indent) + "False Body Node:" + "\n"
                s += node._to_str_node(node.false_body_node, detailed, indent + 4)
            return s
        elif isinstance(node, CFGWhile):
            s = (" " * indent) + "CFGWhile:" + "\n"
            s += (" " * indent) + "Test Node:" + "\n"
            s += node._to_str_node(node.test_node, detailed, indent + 4)
            s += (" " * indent) + "Loop Node:" + "\n"
            s += node._to_str_node(node.loop_body_node, detailed, indent + 4)
            return s
        elif isinstance(node, CFGDoWhile):
            s = (" " * indent) + "CFGDoWhile:" + "\n"
            if node.loop_body_node is not None:
                s += (" " * indent) + "Loop Node:" + "\n"
                s += node._to_str_node(node.loop_body_node, detailed, indent + 4)
            s += (" " * indent) + "Test Node:" + "\n"
            s += node._to_str_node(node.test_node, detailed, indent + 4)
            return s
        elif isinstance(node, CFGSequence):
            s = (" " * indent) + "CFGSequence:" + "\n"
            for n in node.nodes:
                s += (" " * indent) + "Sequence Node:" + "\n"
                s += node._to_str_node(n, detailed, indent + 4)
            return s
        elif isinstance(node, CFGAndSequence):
            s = (" " * indent) + "CFGAndSequence:" + "\n"
            for n in node.nodes:
                s += (" " * indent) + "Sequence Node:" + "\n"
                s += node._to_str_node(n, detailed, indent + 4)
            return s
        elif isinstance(node, CFGSwitch):
            s = (" " * indent) + "CFGSwitch:" + "\n"
            s += (" " * indent) + "Test Node:" + "\n"
            s += node._to_str_node(node.test_node, detailed, indent + 4)
            for n in node.case_nodes:
                s += (" " * indent) + "Case Node:" + "\n"
                s += node._to_str_node(n, detailed, indent + 4)
            return s
        assert False

    def to_str(self, detailed=False):
        return self._to_str_node(self, detailed, 0)


class CFGIfElse(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.test_node = None
        self.true_body_node = None
        self.false_body_node = None

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        new_node.test_node = self.test_node.duplicate(self.cfg.n())
        if self.true_body_node is not None:
            new_node.true_body_node = self.true_body_node.duplicate(self.cfg.n())
        if self.false_body_node is not None:
            new_node.false_body_node = self.false_body_node.duplicate(self.cfg.n())
        new_node.children = [new_node.test_node] + \
                ([new_node.true_body_node] if new_node.true_body_node is not None else []) + \
                ([new_node.false_body_node] if new_node.false_body_node is not None else [])
        return new_node


class CFGSwitch(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.test_node = None
        self.case_nodes = None

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        new_node.test_node = self.test_node.duplicate(self.cfg.n())
        new_node.case_nodes = [n.duplicate(self.cfg.n()) for n in self.case_nodes]
        new_node.children = [new_node.test_node] + list(new_node.nodes)
        return new_node


class CFGWhile(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.test_node = None
        self.loop_body_node = None


class CFGDoWhile(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.test_node = None
        self.loop_body_node = None

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        new_node.test_node = self.test_node.duplicate(self.cfg.n())
        new_node.loop_body_node = self.loop_body_node.duplicate(self.cfg.n())
        new_node.children = [new_node.test_node, new_node.loop_body_nody]
        return new_node


class CFGSequence(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.nodes = None

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        new_node.nodes = [n.duplicate(self.cfg.n()) for n in self.nodes]
        new_node.children = list(new_node.nodes)
        return new_node


class CFGAndSequence(CFGNode):
    def __init__(self, cfg, number):
        CFGNode.__init__(self, cfg, number)
        self.nodes = None

    def duplicate(self, number):
        new_node = copy(self)
        new_node.number = number
        new_node.nodes = [n.duplicate(self.cfg.n()) for n in self.nodes]
        new_node.children = list(new_node.nodes)
        return new_node
