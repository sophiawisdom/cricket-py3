from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QTextCursor, QTextDocument, QBrush, QColor, QTextFormat
from PyQt5.QtWidgets import *
from ide.editor.highlighter import Highlighter
from ide.editor.linenumbers import LineTextWidget



class Editor:
    MODE_CLASS_DUMP = 1
    MODE_DISASSEMBLY = 2
    MODE_BASIC_BLOCKS = 3
    MODE_UCODE = 4
    MODE_SOURCE = 5

    def __init__(self):
        self.text_edit = None
        self.line_to_object_map = None
        self.object_to_line_map = None
        self.show_def_use = False

    def initialize_editor(self, text_edit, mode):
        self.text_edit = text_edit
        self.line_to_object_map = {}

        p = text_edit.parentWidget().layout()
        w = LineTextWidget(text_edit)
        p.addWidget(w)

        font = QtGui.QFont()
        font.setFamily('Menlo')
        font.setFixedPitch(True)
        font.setPointSize(10)

        text_edit.setFont(font)
        text_edit.setLineWrapMode(QTextEdit.NoWrap)

        text_edit.highlighter = Highlighter(text_edit.document())

        if mode == self.MODE_CLASS_DUMP:
            text_edit.highlighter.load_syntax_c()
        elif mode == self.MODE_DISASSEMBLY:
            text_edit.highlighter.load_syntax_asm()
        elif mode == self.MODE_BASIC_BLOCKS:
            text_edit.highlighter.load_syntax_asm()
        elif mode == self.MODE_SOURCE:
            text_edit.highlighter.load_syntax_c()
        else:
            assert False

        text_edit.cursorPositionChanged.connect(self.cursor_position_changed)

    def cursor_position_changed(self):
        cursor = self.text_edit.textCursor()
        line, column = cursor.blockNumber(), cursor.columnNumber()

        w = self.text_edit.window()
        if isinstance(w, QMainWindow):
            if line in list(self.line_to_object_map.keys()):
                o = self.line_to_object_map[line]
                w.set_object_under_caret(o)
            else:
                w.set_object_under_caret(None)

        extra_selections = []

        # Highlight current line.
        selection = QTextEdit.ExtraSelection()
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.format.setBackground(QBrush(QColor("#E6E6FC")))
        selection.cursor = self.text_edit.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)

        # Highlight all defs and uses.
        if self.show_def_use:
            if line in list(self.line_to_object_map.keys()):
                o = self.line_to_object_map[line]
                uses = []
                defs = []
                if hasattr(o, "uses") and o.uses() is not None:
                    uses = o.uses()
                if hasattr(o, "definitions") and o.definitions() is not None:
                    defs = o.definitions()
                for o2 in uses + defs:
                    use_line = self.object_to_line_map[o2]
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                    if o2 in uses and o2 in defs:
                        color = "#F0F0F0"
                    elif o2 in uses:
                        color = "#F0FFF0"
                    elif o2 in defs:
                        color = "#FFF0F0"
                    else:
                        assert False
                    selection.format.setBackground(QBrush(QColor(color)))
                    text_block = self.text_edit.document().findBlockByLineNumber(use_line)
                    cursor = self.text_edit.textCursor()
                    cursor.setPosition(text_block.position())
                    selection.cursor = cursor
                    selection.cursor.clearSelection()
                    extra_selections.append(selection)

        # Highlight all occurences of word under cursor.
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        text = cursor.selectedText()
        rtext = r"\b%s\b" % QRegExp.escape(text)
        if self.text_edit.textCursor().hasSelection():
            text = self.text_edit.textCursor().selectedText()
            rtext = QRegExp.escape(text)
        regexp = QRegExp(rtext, Qt.CaseSensitive)
        cursor.movePosition(QTextCursor.Start)
        flags = QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords
        cursor = self.text_edit.document().find(regexp, cursor, flags)
        first = cursor
        while cursor:
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QBrush(Qt.yellow))
            selection.cursor = cursor
            selection.format.setFontUnderline(True)
            extra_selections.append(selection)

            cursor = self.text_edit.document().find(regexp, cursor, flags)
            if cursor == first: break

        self.text_edit.setExtraSelections(extra_selections)

    def set_text(self, new_text, line_to_object_map):
        self.line_to_object_map = line_to_object_map
        self.object_to_line_map = {}
        for (key, value) in list(self.line_to_object_map.items()):
            self.object_to_line_map[value] = key

        cursor = self.text_edit.textCursor()
        line, column = cursor.blockNumber(), cursor.columnNumber()
        scroll_value = self.text_edit.verticalScrollBar().value()
        self.text_edit.setPlainText(new_text)
        text_block = self.text_edit.document().findBlockByLineNumber(line)
        column = min(column, len(text_block.text()))
        cursor = self.text_edit.textCursor()
        cursor.setPosition(text_block.position())
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, column)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.verticalScrollBar().setValue(scroll_value)
