import os

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from analysis.arch.architecture import *


class WelcomeDialog(QDialog):

    def __init__(self, app):
        QDialog.__init__(self)

        self.app = app
        self.ui_path = os.path.dirname(os.path.abspath(__file__)) + "/" + 'welcome.ui'
        uic.loadUi(self.ui_path, self)

        self.setWindowTitle("Cricket")

        self.recentlyOpenedListWidget = self.recentlyOpenedListWidget ; """:type : QListWidget"""
        self.demoBinariesListWidget = self.demoBinariesListWidget ; """:type : QListWidget"""
        self.browseButton = self.browseButton ; """:type : QPushButton"""

        self.recentlyOpenedListWidget.clear()
        self.demoBinariesListWidget.clear()
        self.recentlyOpenedListWidget.installEventFilter(self)
        self.demoBinariesListWidget.installEventFilter(self)
        self.recentlyOpenedListWidget.itemDoubleClicked.connect(self.recent_double_clicked)
        self.demoBinariesListWidget.itemDoubleClicked.connect(self.demo_double_clicked)
        self.browseButton.clicked.connect(self.browse_clicked)

        d = os.path.dirname(os.path.abspath(__file__)) + "/"

        self.qs = QSettings()

        self.recent_items = []
        if self.qs.contains("welcome_recent_items"):
            self.recent_items = self.qs.value("welcome_recent_items")

        self.demo_items = [
            ("AFNetworking-osx-x86_64-release", d + "../demos/AFNetworking-osx-x86_64-release", X86_64Architecture),
            ("AFNetworking-osx-x86_64-debug", d + "../demos/AFNetworking-osx-x86_64-debug", X86_64Architecture),
        ]

        for i in self.recent_items:
            self.recentlyOpenedListWidget.addItem(i[0])
        for i in self.demo_items:
            self.demoBinariesListWidget.addItem(i[0])

        if len(self.recent_items) > 0:
            self.recentlyOpenedListWidget.setCurrentRow(0)
            self.recentlyOpenedListWidget.setFocus()
        else:
            self.demoBinariesListWidget.setCurrentRow(0)
            self.demoBinariesListWidget.setFocus()

        app.setup_icons(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.recentlyOpenedListWidget:
                self.demoBinariesListWidget.clearSelection()
            elif obj == self.demoBinariesListWidget:
                self.recentlyOpenedListWidget.clearSelection()
        return QDialog.eventFilter(self, obj, event)

    def recent_double_clicked(self, item):
        self.accept()

    def demo_double_clicked(self, item):
        self.accept()

    def accept(self):
        idxs = self.demoBinariesListWidget.selectedIndexes()
        if len(idxs) > 0:
            demo_item = self.demo_items[idxs[0].row()]
            if self.app.open_binary(demo_item[1], demo_item[2]):
                QDialog.accept(self)

        idxs = self.recentlyOpenedListWidget.selectedIndexes()
        if len(idxs) > 0:
            recent_item = self.recent_items[idxs[0].row()]
            archvalue = Architecture.get_arch_from_archvalue(recent_item[2])
            if self.app.open_binary(recent_item[1], archvalue):
                QDialog.accept(self)

    def browse_clicked(self):
        file = QFileDialog.getOpenFileName(None, "Open file")[0]
        if file:
            ret = self.app.open_binary(file)
            if ret:
                QDialog.accept(self)
