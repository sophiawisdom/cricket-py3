import copy


class UndoManager:
    def __init__(self, window):
        self.window = window
        self.stack = []
        self.undo_index = 0
        self.pre_post_counter = 0
        self.disabled = False

    def disable(self):
        self.disabled = True

    def setup_actions(self):
        self.window.actionUndo.triggered.connect(self.undo)
        self.window.actionRedo.triggered.connect(self.redo)

        self.window.actionUndo.setEnabled(False)
        self.window.actionRedo.setEnabled(False)

    def undo(self):
        if self.disabled: return

        item = self.stack[self.undo_index - 1]
        func_before = item["func_before"]
        func_addr = item["func_addr"]

        f = self.window.binary.function_from_addr(func_addr)
        f.replace_with_function(func_before)

        self.window.reload_func()

        self.undo_index -= 1
        self.update_buttons()

    def redo(self):
        if self.disabled: return

        item = self.stack[self.undo_index]
        func_after = item["func_after"]
        func_addr = item["func_addr"]

        f = self.window.binary.function_from_addr(func_addr)
        f.replace_with_function(func_after)

        self.window.reload_func()

        self.undo_index += 1
        self.update_buttons()

    def pre_action(self, func, name):
        self.pre_post_counter += 1
        if self.pre_post_counter > 1: return
        assert self.pre_post_counter == 1
        if self.disabled: return

        if len(self.stack) > 0:
            self.stack = self.stack[0:self.undo_index]

        func_copy = copy.deepcopy(func)
        self.stack.append({"func_addr": func.addr, "func_before": func_copy, "func": func, "name": name})

        self.undo_index = len(self.stack)

    def post_action(self):
        self.pre_post_counter -= 1
        if self.pre_post_counter > 0: return
        assert self.pre_post_counter == 0
        if self.disabled: return

        func = self.stack[len(self.stack) - 1]["func"]
        func_copy = copy.deepcopy(func)
        item = self.stack[len(self.stack) - 1]
        item["func_after"] = func_copy
        self.update_buttons()

    def update_buttons(self):
        self.window.actionUndo.setEnabled(len(self.stack) > 0 and self.undo_index > 0)
        self.window.actionRedo.setEnabled(len(self.stack) > 0 and self.undo_index != len(self.stack))
