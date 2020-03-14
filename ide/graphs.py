import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import subprocess
import math
from numpy import linspace, meshgrid
import numpy
from scipy.interpolate import splprep, splev
from bspline import Uniform_B_Spline, Uniform_Cubic_B_Spline

scale = 50.0


class GraphPlotter:
    def __init__(self, app, func, detailed, callback_object=None):
        self.app = app
        self.func = func
        self.detailed = detailed
        self.callback_object = callback_object
        self.num_to_bb = {}
        self.rects = []
        self.rect_to_node = {}

    @staticmethod
    def generate_dot_file(bbs, bb_sizes):
        s = "digraph {\n"
        s += "node [shape=rectangle, fixedsize=true, width=3, height=1];\n"
        s += "edge [arrowhead=none, arrowtail=none];\n"

        for bb in bbs:
            (w, h) = bb_sizes[bb]

            name = "BB_%d" % bb.number
            s += "%s [width=%.2f, height=%.2f ];\n" % (name, w, h)

            for succ in bb.succs:
                name2 = "BB_%d" % succ.number
                s += "%s -> %s;\n" % (name, name2)

        s += "}\n"
        return s

    def text_for_bb(self, bb):
        s = ""
        max_line_len = 0
        count = len(bb.instructions)
        ellipsis_emitted = False
        n = 0
        for (idx, instr) in enumerate(bb.instructions):
            if not self.detailed:
                if idx not in [0, count - 1]:
                    if not ellipsis_emitted:
                        s += "...\n"
                        n += 1
                        ellipsis_emitted = True
                    continue
            s += instr.canonicalsyntax + "\n"
            n += 1
            max_line_len = max(max_line_len, len(instr.canonicalsyntax))
        return (s, n, max_line_len)

    def text_for_bb_ucode(self, bb):
        s = bb.to_str(self.detailed).strip()
        max_line_len = 0
        n = 0
        for line in s.split("\n"):
            n += 1
            max_line_len = max(max_line_len, len(line))
        return (s, n, max_line_len)

    def generate_scene_basic_blocks(self):
        return self.generate_scene(self.func.bbs, self.text_for_bb)

    def generate_scene_cfg(self):
        return self.generate_scene(self.func.ufunction.cfg.unassigned_bbs_with_cfg_roots, self.text_for_bb_ucode)

    def generate_scene(self, bbs, text_func):
        for bb in bbs:
            self.num_to_bb[bb.number] = bb

        bb_texts = {}
        bb_sizes = {}
        for bb in bbs:
            s, lines, max_line_len = text_func(bb)
            bb_texts[bb] = s
            w = max_line_len * 7.0
            h = (lines * 12.0 + 10.0)
            w = max(w, 200)
            #h = max(h, 30)
            bb_sizes[bb] = (w / scale, h / scale)

        scene = MyGraphicsScene(self)

        font = QFont()
        font.setFamily('Menlo')
        font.setFixedPitch(True)
        font.setPointSize(10)

        dot_contents = GraphPlotter.generate_dot_file(bbs, bb_sizes)

        filename = self.app.appdata_dir() + "/" + "dotfile.dot"
        #filename_png = os.path.dirname(os.path.abspath(__file__)) + "/" + "dotfile.png"
        #filename_plain = os.path.dirname(os.path.abspath(__file__)) + "/" + "dotfile.plain"
        with open(filename, "w") as text_file:
            text_file.write(dot_contents)
        #subprocess.check_output(["dot", "-Tpng", filename, "-o", filename_png])
        #subprocess.check_output(["dot", "-Tplain", filename, "-o", filename_plain])
        dot_plain = subprocess.check_output(["dot", "-Tplain", filename]).strip().split("\n")

        node_positions = {}
        graph_w = None
        graph_h = None
        for line in dot_plain:
            line = line.split(" ")

            if line[0] == "graph":
                graph_w = float(line[2]) * scale
                graph_h = float(line[2]) * scale
            if line[0] == "node":
                bb_number = int(line[1][3:])
                bb = self.num_to_bb[bb_number]
                x = float(line[2]) * scale
                y = graph_h - float(line[3]) * scale
                w = float(line[4]) * scale
                h = float(line[5]) * scale

                node_positions[bb_number] = (x, y, w, h)

                x -= w / 2
                y -= h / 2
                rect_item = MyRoundRectItem(QRectF(0, 0, w, h), self)
                rect_item.setPos(QPointF(x, y))
                rect_item.setFlag(QGraphicsItem.ItemClipsChildrenToShape, True)
                t = bb_texts[bb]
                text_item = QGraphicsTextItem(t, rect_item)
                text_item.setPos(QPointF(0, 0))
                text_item.setFont(font)

                scene.addItem(rect_item)
                self.rects.append(rect_item)
                self.rect_to_node[rect_item] = bb

            if line[0] == "edge":
                bb1_number = int(line[1][3:])
                bb2_number = int(line[2][3:])
                n = int(line[3])
                points = []
                for i in range(0, n):
                    x = float(line[4 + 2 * i]) * scale
                    y = graph_h - float(line[4 + 2 * i + 1]) * scale
                    points.append((x, y))

                points = self.evaluate_b_spline(points)

                p = QPainterPath()
                a,b = points[0]
                p.moveTo(a, b)
                for i in range(1, len(points)):
                    c,d = points[i]
                    p.lineTo(c, d)

                if bb1_number == bb2_number - 1:
                    # Fallthrough
                    color = QColor("#009C35")
                elif bb2_number > bb1_number:
                    # Forward jump
                    color = QColor("#0000C5")
                else:
                    color = QColor("#7F009C")
                path_item = MyArrowPathItem(p, color)
                scene.addItem(path_item)

        self.scene = scene

        return scene

    def set_selected_rect(self, rect):
        for r in self.rects:
            r.bg_color = QColor("#fff")
            r.update()

        if rect is not None:
            rect.bg_color = QColor("#ddd")
            rect.update()
            if self.callback_object is not None: self.callback_object.set_selected_graph_node(self.rect_to_node[rect])
        else:
            if self.callback_object is not None: self.callback_object.set_selected_graph_node(None)

    def evaluate_b_spline(self, control_points):
        #x = [i[0] for i in control_points]
        #y = [i[1] for i in control_points]
        new_points = []

        new_points.append(control_points[0])

        P = numpy.array(control_points)
        degree = 3
        bspline = Uniform_Cubic_B_Spline(P)
        evaluation_count = 40
        for val in linspace(0, 1, evaluation_count):
            x, y = bspline(val)
            new_points.append((x,y))

        new_points.append(control_points[-1])

        return new_points


class MyGraphicsScene(QGraphicsScene):
    def __init__(self, plotter):
        QGraphicsScene.__init__(self)
        self.plotter = plotter

    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QTransform()) is None:
            self.plotter.set_selected_rect(None)
        else:
            super(MyGraphicsScene, self).mousePressEvent(event)


class MyRoundRectItem(QGraphicsRectItem):
    def __init__(self, rect, plotter):
        QGraphicsRectItem.__init__(self, rect)
        self.plotter = plotter
        self.bg_color = QColor("#fff")

    def paint(self, painter, option, widget=None):
        rect = self.rect()
        painter.setPen(QColor("#ccc"))
        painter.setBrush(self.bg_color)
        painter.drawRoundedRect(0, 0, rect.width(), rect.height(), 5, 5)

    def mousePressEvent(self, event):
        def f():
            self.plotter.set_selected_rect(self)

        QTimer.singleShot(10, f)


class MyArrowPathItem(QGraphicsPathItem):
    def __init__(self, path, color):
        QGraphicsPathItem.__init__(self, path)
        self.color = color

    def paint(self, painter, option, widget=None):
        painter.setPen(self.color)
        path = self.path()
        painter.drawPath(path)
        angle = path.angleAtPercent(1.0)
        endpoint = path.pointAtPercent(1.0)

        painter.translate(endpoint.x(), endpoint.y())
        painter.rotate(-angle - 90)

        endpoint = QPointF(0, 0)
        p1 = QPointF(-5, -5)
        p2 = QPointF(+5, -5)

        path = QPainterPath()
        path.addPolygon(QPolygonF([endpoint, p1, p2]))

        painter.fillPath(path, QBrush(self.color))
