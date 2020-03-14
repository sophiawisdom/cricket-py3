class NavigationManager:
    def __init__(self, window):
        self.window = window
        self.stack = []
        self.back_index = 0

    def setup_actions(self):
        self.window.actionGo_Back.triggered.connect(self.go_back)
        self.window.actionGo_Forward.triggered.connect(self.go_forward)

        self.window.actionGo_Back.setEnabled(False)
        self.window.actionGo_Forward.setEnabled(False)

    def go_back(self):
        pass

    def go_forward(self):
        pass

    def goto_function(self, func):
        pass

    def goto_class(self, cls):
        pass
