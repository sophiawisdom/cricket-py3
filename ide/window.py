from functools import partial
import os

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from analysis.arch.architecture import I386Architecture, X86_64Architecture, ArmV7Architecture, AArch64Architecture
from analysis.ucode.ucode import UCodeInstruction
from ide.actions import ActionManager
from ide.bb.textbox import BBTextBox, BBArrow
from ide.editor.editor import Editor
from ide.graphs import GraphPlotter
from ide.navigation import NavigationManager
from ide.undo import UndoManager


class MainWindow(QMainWindow):
    TAB_CLASSDUMP = 0
    TAB_DISASSEMBLY = 1
    TAB_BASIC_BLOCKS = 2
    TAB_UCODE = 3
    TAB_CFG = 4
    TAB_SOURCE = 5

    def connect_list_switches(self):
        self.listSwitchClasses.clicked.connect(self.switch_list_type(self.listSwitchClasses, 0))
        self.listSwitchFunctions.clicked.connect(self.switch_list_type(self.listSwitchFunctions, 1))
        self.listSwitchBlocks.clicked.connect(self.switch_list_type(self.listSwitchBlocks, 2))

        self.stackedWidget.setCurrentIndex(0)

    def setup_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionClose.triggered.connect(self.close)

        self.actionOpen_Demo_Binary_x86.triggered.connect(partial(self.open_demo, "../../binaries/objc_sim", I386Architecture))
        self.actionOpen_Demo_Binary_x86_64.triggered.connect(partial(self.open_demo, "../../binaries/objc_sim", X86_64Architecture))
        self.actionOpen_Demo_Binary_armv7.triggered.connect(partial(self.open_demo, "../../binaries/objc_dev", ArmV7Architecture))
        self.actionOpen_Demo_Binary_arm64.triggered.connect(partial(self.open_demo, "../../binaries/objc_dev", AArch64Architecture))

    def open(self):
        file = QFileDialog.getOpenFileName(self, "Open file")[0]
        if file:
            self.app.open_binary(file)

    def open_demo(self, path, arch):
        self.app.open_binary(path, arch)

    def save(self):
        pass

    def setup_tabs(self):
        self.tabWidget.currentChanged.connect(self.tab_changed)
        #self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setCurrentIndex(0)

    def tab_changed(self):
        self.action_manager.tab_changed(self.tabWidget.currentIndex())

    def load_tree_items(self):
        self.classesTreeWidget.clear()
        for c in self.binary.classes:
            class_item = QTreeWidgetItem([c.name])
            class_item.func = None
            class_item.cls = c
            class_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/c.png"))
            self.classesTreeWidget.addTopLevelItem(class_item)

            for m in c.methods:
                method_item = QTreeWidgetItem([m.name])
                method_item.func = m.function
                method_item.cls = None
                method_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/m.png"))

                if self.classListFlatViewCheckbox.isChecked():
                    method_item.setText(0, m.function.name)
                    self.classesTreeWidget.addTopLevelItem(method_item)
                else:
                    class_item.addChild(method_item)

        if self.showExternalClassesCheckbox.isChecked():
            for c in list(self.binary.class_refs.values()):
                class_item = QTreeWidgetItem(["(external) %s (in %s)" % (c.class_name, c.external_dylib)])
                class_item.func = None
                class_item.cls = None
                class_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/c.png"))
                self.classesTreeWidget.addTopLevelItem(class_item)

        self.classesTreeWidget.itemSelectionChanged.connect(self.selection_changed(self.classesTreeWidget))

        self.classesTreeWidget.setFocus(Qt.ActiveWindowFocusReason)
        if self.classesTreeWidget.topLevelItemCount() > 0:
            self.classesTreeWidget.topLevelItem(0).setSelected(True)

        self.functionsTreeWidget.clear()
        for f in self.binary.functions:
            func_item = QTreeWidgetItem([f.name])
            func_item.func = f
            func_item.cls = None
            func_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/f.png"))
            self.functionsTreeWidget.addTopLevelItem(func_item)
        self.functionsTreeWidget.itemSelectionChanged.connect(self.selection_changed(self.functionsTreeWidget))

        self.blocksTreeWidget.clear()
        for b in self.binary.block_descriptors:
            block_item = QTreeWidgetItem([b.name])
            block_item.func = None
            block_item.cls = None
            block_item.block = b
            block_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/b.png"))
            self.blocksTreeWidget.addTopLevelItem(block_item)

            for u in b.uses:
                subblock_item = QTreeWidgetItem([u.name])
                subblock_item.func = u.function if hasattr(u, "function") else None
                subblock_item.cls = None
                subblock_item.block = None
                subblock_item.setIcon(0, QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/m.png"))
                block_item.addChild(subblock_item)

                if hasattr(u, "invoke_func") and u.invoke_func is not None:
                    invoke_item = QTreeWidgetItem(["Invoke: " + u.invoke_func.name])
                    invoke_item.func = u.invoke_func
                    invoke_item.cls = None
                    invoke_item.block = None
                    invoke_item.setIcon(0, QIcon(
                        os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/f.png"))
                    block_item.addChild(invoke_item)


                if hasattr(u, "uses"):
                    for u2 in u.uses:
                        subblock2_item = QTreeWidgetItem([u2.name])
                        subblock2_item.func = None
                        subblock2_item.cls = None
                        subblock2_item.block = None
                        subblock2_item.setIcon(0, QIcon(
                            os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/m.png"))
                        subblock_item.addChild(subblock2_item)

                    invoke_item = QTreeWidgetItem(["Invoke: " + u.invoke_func.name])
                    invoke_item.func = u.invoke_func
                    invoke_item.cls = None
                    invoke_item.block = None
                    invoke_item.setIcon(0, QIcon(
                        os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/letters/f.png"))
                    subblock_item.addChild(invoke_item)

        self.blocksTreeWidget.itemSelectionChanged.connect(self.selection_changed(self.blocksTreeWidget))

    def setup_editor(self):
        self.class_dump_editor = Editor()
        self.class_dump_editor.initialize_editor(self.classDumpTextEdit, Editor.MODE_CLASS_DUMP)

        self.disassembly_editor = Editor()
        self.disassembly_editor.initialize_editor(self.disassemblyTextEdit, Editor.MODE_DISASSEMBLY)

        self.ucode_editor = Editor()
        self.ucode_editor.initialize_editor(self.uCodeTextEdit, Editor.MODE_DISASSEMBLY)

        self.source_editor = Editor()
        self.source_editor.initialize_editor(self.sourceTextEdit, Editor.MODE_SOURCE)

    def current_tab(self):
        return self.tabWidget.currentIndex()

    def goto_tab(self, tab_index):
        self.tabWidget.setCurrentIndex(tab_index)

    def selection_changed(self, widget):
        def f():
            selected_item = widget.selectedItems()[0] if len(widget.selectedItems()) > 0 else None
            if selected_item is None: return

            if selected_item.func:
                self.func_clicked(selected_item.func)
                return

            if selected_item.cls:
                self.class_clicked(selected_item.cls)
                return

        return f

    def class_clicked(self, cls):
        class_dump = ""
        class_dump += "//" + "\n"
        class_dump += "// Class dump for " + cls.name + "\n"
        class_dump += "//" + "\n"
        class_dump += "" + "\n"
        class_dump += cls.class_dump()

        self.classDumpTextEdit.setPlainText(class_dump)

        self.tabWidget.setTabEnabled(self.TAB_DISASSEMBLY, False)
        self.tabWidget.setTabEnabled(self.TAB_BASIC_BLOCKS, False)
        self.tabWidget.setTabEnabled(self.TAB_UCODE, False)
        self.tabWidget.setTabEnabled(self.TAB_CFG, False)
        self.tabWidget.setTabEnabled(self.TAB_SOURCE, False)

        self.goto_tab(self.TAB_CLASSDUMP)

    def func_clicked(self, func):
        self.selected_func = func
        func.load()
        self.reload_func()
        self.goto_tab(self.TAB_DISASSEMBLY)

    def reload_assembly_instructions(self, func):
        ucode, line_map = func.print_asm_intructions()
        self.disassembly_editor.set_text(ucode, line_map)

    def reload_func(self):
        func = self.selected_func

        self.tabWidget.setTabEnabled(self.TAB_DISASSEMBLY, True)
        self.tabWidget.setTabEnabled(self.TAB_BASIC_BLOCKS, func.bbs is not None)
        self.tabWidget.setTabEnabled(self.TAB_UCODE, func.ufunction is not None)
        self.tabWidget.setTabEnabled(self.TAB_CFG, func.ufunction is not None and func.ufunction.cfg is not None)
        self.tabWidget.setTabEnabled(self.TAB_SOURCE, func.ast is not None)

        self.reload_assembly_instructions(func)

        self.reload_basic_blocks(func)

        self.reload_ucode()

        self.reload_ucode_cfg(func)

        self.reload_source()

    def reload_ucode(self):
        func = self.selected_func
        ufunc = func.ufunction
        if ufunc is None: return

        ufunc.compute_def_use_chains()
        ucode, line_map = ufunc.print_to_text(self.show_ucode_details, func)
        self.ucode_editor.show_def_use = self.show_ucode_def_use
        self.ucode_editor.set_text(ucode, line_map)

    def reload_source(self):
        func = self.selected_func
        if func.ast is None: return

        ast, line_map = func.print_ast()
        self.source_editor.set_text(ast, line_map)

    def show_detailed_basic_blocks_view(self):
        self.show_detailed_basic_blocks = not self.show_detailed_basic_blocks
        self.reload_func()

    def show_detailed_cfg_view(self):
        self.show_detailed_cfg = not self.show_detailed_cfg
        self.reload_func()

    def switch_basic_blocks_view(self):
        p = self.basicBlocksScrollArea.parent()
        if p:
            self.basicBlocksScrollArea.setParent(None)
            self.basicBlocksGraphicsView.setRenderHint(QPainter.Antialiasing)
            p.layout().addWidget(self.basicBlocksGraphicsView)
            self.basicBlocksSwitchButton.setText("switch to linear")
            self.basicBlocksDetailedButton.setVisible(True)
        else:
            p = self.basicBlocksGraphicsView.parent()
            self.basicBlocksGraphicsView.setParent(None)
            p.layout().addWidget(self.basicBlocksScrollArea)
            self.basicBlocksSwitchButton.setText("switch to graph")
            self.basicBlocksDetailedButton.setVisible(False)

        self.basicBlocksSwitchButton.raise_()
        self.basicBlocksDetailedButton.raise_()

    def cfg_blocks_view(self):
        p = self.cfgScrollArea.parent()
        if p:
            self.cfgScrollArea.setParent(None)
            self.cfgGraphicsView.setRenderHint(QPainter.Antialiasing)
            p.layout().addWidget(self.cfgGraphicsView)
            self.cfgSwitchButton.setText("switch to linear")
            self.cfgDetailedButton.setVisible(True)
        else:
            p = self.cfgGraphicsView.parent()
            self.cfgGraphicsView.setParent(None)
            p.layout().addWidget(self.cfgScrollArea)
            self.cfgSwitchButton.setText("switch to graph")
            self.cfgDetailedButton.setVisible(False)

        self.cfgSwitchButton.raise_()
        self.cfgDetailedButton.raise_()

    def basic_blocks_generate_graph(self, func):
        scene = GraphPlotter(self.app, func, self.show_detailed_basic_blocks).generate_scene_basic_blocks()
        self.basicBlocksGraphicsView.setScene(scene)
        scene_rect = scene.itemsBoundingRect()
        scene_rect.setTop(scene_rect.top() - 20)
        scene_rect.setBottom(scene_rect.bottom() + 20)
        scene_rect.setLeft(scene_rect.left() - 20)
        scene_rect.setRight(scene_rect.right() + 20)
        self.basicBlocksGraphicsView.setSceneRect(scene_rect)

    def cfg_generate_graph(self, func):
        scene = GraphPlotter(self.app, func, self.show_detailed_cfg, self).generate_scene_cfg()
        self.cfgGraphicsView.setScene(scene)
        scene_rect = scene.itemsBoundingRect()
        scene_rect.setTop(scene_rect.top() - 20)
        scene_rect.setBottom(scene_rect.bottom() + 20)
        scene_rect.setLeft(scene_rect.left() - 20)
        scene_rect.setRight(scene_rect.right() + 20)
        self.cfgGraphicsView.setSceneRect(scene_rect)
        self.set_selected_graph_node(None)

    def set_selected_graph_node(self, node):
        self.selected_cfg_node = node
        self.action_manager.cfg_node_changed(node)

    def basic_blocks_generate_linear(self, func):
        # Remove BBs.
        for c in self.basicBlocksContent.children():
            if isinstance(c, QWidget):
                c.setParent(None)

        # Remove stretch.
        for i in range(0, self.basicBlocksContent.layout().count()):
            item = self.basicBlocksContent.layout().itemAt(i)
            if isinstance(item, QSpacerItem):
                self.basicBlocksContent.layout().takeAt(i)
        self.basicBlocksContent.layout().addWidget(BBArrow(func, None, func.bbs[0]))
        for i in range(0, len(func.bbs)):
            bb = func.bbs[i]
            nextbb = func.bbs[i + 1] if i + 1 < len(func.bbs) else None

            t = BBTextBox(func, bb)
            self.basicBlocksContent.layout().addWidget(t)
            self.basicBlocksContent.layout().addWidget(BBArrow(func, bb, nextbb))
        self.basicBlocksContent.layout().addStretch(0)

    def cfg_generate_linear(self, func):
        # Remove BBs.
        for c in self.cfgContent.children():
            if isinstance(c, QWidget):
                c.setParent(None)

        # Remove stretch.
        for i in range(0, self.cfgContent.layout().count()):
            item = self.cfgContent.layout().itemAt(i)
            if isinstance(item, QSpacerItem):
                self.cfgContent.layout().takeAt(i)
        self.cfgContent.layout().addWidget(BBArrow(func, None, func.ufunction.bbs[0]))
        for i in range(0, len(func.ufunction.bbs)):
            bb = func.ufunction.bbs[i]
            nextbb = func.ufunction.bbs[i + 1] if i + 1 < len(func.ufunction.bbs) else None

            t = BBTextBox(func, bb)
            self.cfgContent.layout().addWidget(t)
            self.cfgContent.layout().addWidget(BBArrow(func, bb, nextbb))
        self.cfgContent.layout().addStretch(0)

    def reload_basic_blocks(self, func):
        if func.bbs is None: return

        self.basic_blocks_generate_graph(func)
        self.basic_blocks_generate_linear(func)

    def reload_ucode_cfg(self, func):
        if func.ufunction is None: return
        if func.ufunction.cfg is None: return

        self.cfg_generate_graph(func)
        self.cfg_generate_linear(func)

    def switch_list_type(self, button, page_index):
        def f(clicked):
            self.listSwitchClasses.setChecked(False)
            self.listSwitchBlocks.setChecked(False)
            self.listSwitchFunctions.setChecked(False)
            button.setChecked(True)
            self.stackedWidget.setCurrentIndex(page_index)

        return f

    def set_object_under_caret(self, o):
        if o is not None:
            s = "<%s at %s> %s" % (o.__class__.__name__, hex(id(o)), str(o))
        else:
            s = ""

        self.statusBar().showMessage(s)

        if isinstance(o, UCodeInstruction):
            self.selected_uinstruction = o
        else:
            self.selected_uinstruction = None

    def __init__(self, app, binary):
        QMainWindow.__init__(self)

        self.app = app
        self.binary = binary; """:type : Binary"""

        self.selected_class = None
        self.selected_func = None
        self.selected_uinstruction = None
        self.selected_cfg_node = None

        self.show_ucode_details = False
        self.show_ucode_def_use = False
        self.show_detailed_basic_blocks = False
        self.show_detailed_cfg = False

        self.ui_path = os.path.dirname(os.path.abspath(__file__)) + "/" + 'window.ui'
        uic.loadUi(self.ui_path, self)

        # Define type hints for widgets.
        self.classesTreeWidget = self.classesTreeWidget; """:type : QTreeWidget"""
        self.functionsTreeWidget = self.functionsTreeWidget; """:type : QTreeWidget"""
        self.stackedWidget = self.stackedWidget; """:type : QStackedWidget"""
        self.splitter = self.splitter; """:type : QSplitter"""
        self.disassemblyTextEdit = self.disassemblyTextEdit; """:type : QTextEdit"""
        self.tabWidget = self.tabWidget; """:type : QTabWidget"""
        self.actionClose = self.actionClose; """:type : QAction"""
        self.listSwitchClasses = self.listSwitchClasses; """:type : QToolButton"""
        self.listSwitchBlocks = self.listSwitchBlocks; """:type : QToolButton"""
        self.listSwitchFunctions = self.listSwitchFunctions; """:type : QToolButton"""
        self.classDumpTextEdit = self.classDumpTextEdit; """:type : QTextEdit"""
        self.mainToolBar = self.mainToolBar; """:type : QToolBar"""
        self.sideToolBar = self.sideToolBar; """:type : QToolBar"""

        self.basicBlocksScrollArea = self.basicBlocksScrollArea; """:type : QScrollArea"""
        self.basicBlocksContent = self.basicBlocksContent; """:type : QWidget"""
        self.basicBlocksGraphicsView = QGraphicsView()
        self.cfgScrollArea = self.cfgScrollArea; """:type : QScrollArea"""
        self.cfgContent = self.cfgContent; """:type : QWidget"""
        self.cfgGraphicsView = QGraphicsView()

        self.basicBlocksSwitchButton = QPushButton("switch to graph", self.basicBlocksTab)
        self.basicBlocksSwitchButton.move(5, 5)
        self.basicBlocksSwitchButton.resize(120, 28)
        self.basicBlocksSwitchButton.clicked.connect(self.switch_basic_blocks_view)
        self.basicBlocksDetailedButton = QPushButton("show all instructions", self.basicBlocksTab)
        self.basicBlocksDetailedButton.move(5, 35)
        self.basicBlocksDetailedButton.resize(160, 28)
        self.basicBlocksDetailedButton.clicked.connect(self.show_detailed_basic_blocks_view)
        self.basicBlocksDetailedButton.setVisible(False)

        self.cfgSwitchButton = QPushButton("switch to graph", self.cfgTab)
        self.cfgSwitchButton.move(5, 5)
        self.cfgSwitchButton.resize(120, 28)
        self.cfgSwitchButton.clicked.connect(self.cfg_blocks_view)
        self.cfgDetailedButton = QPushButton("show all instructions", self.cfgTab)
        self.cfgDetailedButton.move(5, 35)
        self.cfgDetailedButton.resize(160, 28)
        self.cfgDetailedButton.clicked.connect(self.show_detailed_cfg_view)
        self.cfgDetailedButton.setVisible(False)

        self.cfgSwitchButton.click()

        self.showExternalClassesCheckbox.clicked.connect(self.load_tree_items)
        self.classListFlatViewCheckbox.clicked.connect(self.load_tree_items)

        self.setWindowTitle("Cricket - %s" % self.binary.full_path)

        self.action_manager = ActionManager(self)
        self.action_manager.setup_actions()

        self.undo_manager = UndoManager(self)
        self.undo_manager.setup_actions()

        self.navigation_manager = NavigationManager(self)
        self.navigation_manager.setup_actions()

        self.connect_list_switches()
        app.setup_icons(self)
        self.setup_actions()
        self.setup_tabs()

        self.load_tree_items()

        self.setup_editor()

    def closeEvent(self, event):
        self.app.window_closed(self)
        QMainWindow.closeEvent(self, event)
