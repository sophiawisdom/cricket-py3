


class InstructionPattern:
    def __init__(self):
        self.matched_instructions = []
        self.instructions_to_insert = []


class InstructionPatternSaveAndRestoreRegisters(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.save_instructions = []
        self.restore_instructions = []
        self.registers = set()


class InstructionPatternSetupAndTeardownStackFrame(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.setup_instructions = []
        self.teardown_instructions = []


class InstructionPatternSetupFramePointer(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.setup_instructions = []
        self.teardown_instructions = []

    def __str__(self):
        return "Stack frame pointer setup"

class InstructionPatternGetPICBase(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.setup_instructions = []
        self.teardown_instructions = []
        self.register = None
        self.pc_value = None

    def __str__(self):
        return "PIC base retrieval"


class InstructionPatternPushPop(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.setup_instructions = []
        self.teardown_instructions = []
        self.register = None

    def __str__(self):
        return "Saving non-scratch registers"

class InstructionPatternSubAddEsp(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.setup_instructions = []
        self.teardown_instructions = []
        self.register = None

    def __str__(self):
        return "Setup stack variables"


class InstructionPatternStackCheck(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.check_failed_bb = None
        self.branch_bb = None

    def __str__(self):
        return "Stack overflow check"


class InstructionPatternTailCall(InstructionPattern):
    def __init__(self, function):
        InstructionPattern.__init__(self)
        self.function = function
        self.jump_instruction = None
        self.jump_destination = None
        self.indirect = None

    def __str__(self):
        return "Tail call"
