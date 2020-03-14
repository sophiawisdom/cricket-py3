import abc


class UCodeFunctionTransform:
    def __init__(self, function, binary=None):
        self.function = function
        self.binary = binary

    def can_be_performed(self):
        return self.can_be_performed_on_function(self.function)

    def perform(self):
        self.perform_on_function(self.function)

    @abc.abstractmethod
    def can_be_performed_on_function(self, function):
        assert False

    @abc.abstractmethod
    def perform_on_function(self, function):
        assert False


class UCodeApplyBasicBlockTransformToAll(UCodeFunctionTransform):
    def __init__(self, function, basic_block_transform):
        UCodeFunctionTransform.__init__(self, function)
        self.basic_block_transform = basic_block_transform

    def can_be_performed_on_function(self, function):
        return True  # TODO

    def perform_on_function(self, function):
        for bb in function.bbs:
            transform = self.basic_block_transform(self.function, bb)
            transform.binary = self.binary
            transform.perform()


class UCodeApplyInstructionTransformToAll(UCodeFunctionTransform):
    def __init__(self, function, instruction_transform):
        UCodeFunctionTransform.__init__(self, function)
        self.instruction_transform = instruction_transform

    def can_be_performed_on_function(self, function):
        return True  # TODO

    def perform_on_function(self, function):
        for bb in function.bbs:
            for instr in bb.instructions:
                transform = self.instruction_transform(self.function, instr)
                transform.binary = self.binary
                transform.perform()
