from PyQt5 import QtGui, QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from analysis.asm.basicblock import BasicBlock
from analysis.ucode.ucode import UCodeBasicBlock
from ide.editor.editor import Editor


class BBTextBox(QWidget):
    def format_instr(self, instr):
        if hasattr(instr, "canonicalsyntax"):
            s = "        %s" % (instr.canonicalsyntax)
        else:
            s = "        %s" % str(instr)
        #
        # for p in instr.bb.function.patterns:
        #     if instr in p.matched_instructions:
        #         s += " " * max(1, 50 - len(s)) + "; " + str(p)
        #         break

        return s

    def __init__(self, function, bb):
        QWidget.__init__(self)

        self.bb = bb
        self.function = function

        self.text_edit = QTextEdit()

        self.text_edit.textChanged.connect(self.text_changed)
        f = int(self.text_edit.textInteractionFlags())
        f &= ~QtCore.Qt.TextEditable
        self.text_edit.setTextInteractionFlags(Qt.TextInteractionFlags(f))

        l = QVBoxLayout()
        self.setLayout(l)
        l.setContentsMargins(100,0,100,0)
        self.layout().addWidget(self.text_edit)

        self.editor = Editor()
        self.editor.initialize_editor(self.text_edit, Editor.MODE_BASIC_BLOCKS)

        s = "0x%x:" % bb.addr + "\n"

        line_to_object_map = {}
        line_no = 1

        for instr in bb.instructions:
            s += self.format_instr(instr) + "\n"
            line_to_object_map[line_no] = instr
            line_no += 1

        s = s.strip()
        self.editor.set_text(s, line_to_object_map)

        self.text_changed()

    def sizeHint(self):
        return self.size_hint

    def minimumSizeHint(self):
        return self.size_hint

    def text_changed(self):
        #self.text_edit.document().setTextWidth(self.text_edit.viewport().width())
        s = self.text_edit.document().size()
        self.size_hint = QtCore.QSize(self.size().width(), s.height() + 2)
        self.setMaximumHeight(self.size_hint.height())
        self.updateGeometry()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)

        in_bbs = []
        out_bbs = []
        pre_fallthrough_num = self.bb.number - 1
        if pre_fallthrough_num >= 0:
            if isinstance(self.bb, BasicBlock):
                pre_fallthrough_bb = self.bb.function.bbs[pre_fallthrough_num]
            elif isinstance(self.bb, UCodeBasicBlock):
                pre_fallthrough_bb = self.function.ufunction.bbs[pre_fallthrough_num]
            else:
                assert False

            for pred_bb in self.bb.preds:
                if pred_bb != pre_fallthrough_bb:
                    in_bbs.append(pred_bb)
        for succ_bb in self.bb.succs:
            if succ_bb.number != self.bb.number + 1:
                out_bbs.append(succ_bb)

        font = QtGui.QFont()
        font.setFamily('Helvetica Neue')
        font.setItalic(True)
        font.setPointSize(10)
        p.setFont(font)
        p.setPen(QtGui.QPen(Qt.gray))

        ARROW_SIZE = 5

        y = 15
        for bb in in_bbs:
            t = "#%d" % bb.number
            l = 30
            p.drawText(QtCore.QPoint(l, y), t)
            bounds = p.boundingRect(QtCore.QRect(0, 0, 100, 20), 0, t)
            l += bounds.width()

            y -= 4
            p.drawLine(l, y, 100 - ARROW_SIZE, y)
            p.drawLine(100 - ARROW_SIZE, y - ARROW_SIZE, 100 - ARROW_SIZE, y + ARROW_SIZE)
            p.drawLine(100 - ARROW_SIZE, y + ARROW_SIZE, 100, y)
            p.drawLine(100, y, 100 - ARROW_SIZE, y - ARROW_SIZE)

            y += 30

        y = self.height() - 30 * len(out_bbs) + 20
        for bb in out_bbs:
            t = "#%d" % bb.number
            l = self.width() - 100
            r = self.width() - 30
            bounds = p.boundingRect(QtCore.QRect(0, 0, 100, 20), 0, t)
            r -= bounds.width()
            p.drawText(QtCore.QPoint(r, y), t)
            r -= 2

            y -= 4
            p.drawLine(l, y, r - ARROW_SIZE, y)
            p.drawLine(r - ARROW_SIZE, y - ARROW_SIZE, r - ARROW_SIZE, y + ARROW_SIZE)
            p.drawLine(r - ARROW_SIZE, y + ARROW_SIZE, r, y)
            p.drawLine(r, y, r - ARROW_SIZE, y - ARROW_SIZE)

            y += 30


class BBArrow(QWidget):
    def __init__(self, function, prevbb, nextbb):
        QWidget.__init__(self)

        self.function = function
        self.prevbb = prevbb
        self.nextbb = nextbb

        self.title = ""
        self.big = False
        self.arrow_hidden = False

        if self.prevbb == None:
            self.title = "function entry"
            self.big = True
        elif self.prevbb.is_exit:
            self.title = "function exit"
            self.big = True
        else:
            self.title = "fallthrough"
            num = self.prevbb.number
            fallthrough_num = self.prevbb.number + 1
            fallthrough_bb = None
            if isinstance(self.prevbb, BasicBlock):
                if fallthrough_num < len(self.prevbb.function.bbs):
                    fallthrough_bb = self.prevbb.function.bbs[fallthrough_num]
            elif isinstance(self.prevbb, UCodeBasicBlock):
                if fallthrough_num < len(self.function.ufunction.bbs):
                    fallthrough_bb = self.function.ufunction.bbs[fallthrough_num]
            else:
                assert False
            if not fallthrough_bb or not fallthrough_bb in self.prevbb.succs:
                self.arrow_hidden = True

        self.setFixedHeight(25)
        if self.prevbb and self.prevbb.is_exit:
            self.setFixedHeight(35)

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setPen(QtGui.QPen(Qt.black))

        c = self.width() / 2

        LINE_SPACING = 3
        LINE_SIZE = 20
        ARROW_SIZE = 5

        font = QtGui.QFont()
        font.setFamily('Helvetica Neue')
        font.setItalic(True)
        font.setPointSize(10)
        p.setFont(font)

        if not self.arrow_hidden:
            p.setPen(QtGui.QPen(Qt.gray))
            if not self.big:
                p.drawLine(c, 0, c, LINE_SIZE)
                p.drawLine(c - ARROW_SIZE, LINE_SIZE, c + ARROW_SIZE, LINE_SIZE)
                p.drawLine(c + ARROW_SIZE, LINE_SIZE, c, LINE_SIZE + ARROW_SIZE)
                p.drawLine(c, LINE_SIZE + ARROW_SIZE, c - ARROW_SIZE, LINE_SIZE)
            else:
                p.drawLine(c - LINE_SPACING, 0, c - LINE_SPACING, LINE_SIZE)
                p.drawLine(c + LINE_SPACING, 0, c + LINE_SPACING, LINE_SIZE)

                p.drawLine(c - 10, LINE_SIZE, c + 10, LINE_SIZE)
                p.drawLine(c + 10, LINE_SIZE, c, LINE_SIZE + ARROW_SIZE)
                p.drawLine(c, LINE_SIZE + ARROW_SIZE, c - 10, LINE_SIZE)

            # Draw edge title.
            p.setPen(QtGui.QPen(Qt.gray))
            p.drawText(QtCore.QPoint(c + 15, 15), self.title)

        # Draw BB number.
        if self.nextbb is not None:
            p.setPen(QtGui.QPen(Qt.gray))
            p.drawText(QtCore.QPoint(100, 23), "#%d" % self.nextbb.number)
