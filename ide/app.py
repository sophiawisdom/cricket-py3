import cProfile
import os

import io
import pstats

import errno

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from analysis.binary import Binary
from ide.welcome import WelcomeDialog
from ide.window import MainWindow


class App:
    open_windows = []

    def __init__(self):
        self.qapp = None
        self.profiler = cProfile.Profile()
        self.profiling_enabled = False
        self.profiling_has_results = False
        self.welcome_dialog = None
        self.open_windows = []

    def start_profiling(self):
        if not self.profiling_enabled:
            self.profiler.enable()
            self.profiling_enabled = True
            self.profiling_has_results = True

    def stop_profiling(self):
        if self.profiling_enabled:
            self.profiler.disable()
            self.profiling_enabled = False

    def print_profiling_stats_and_clear(self):
        self.stop_profiling()
        if self.profiling_has_results:
            s = io.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(self.profiler, stream=s).sort_stats(sortby)
            ps.print_stats()
            print((s.getvalue()))

            self.profiler.clear()
            if not self.profiling_enabled:
                self.profiling_has_results = False

    def setup_icons(self, window):
        import xml.etree.ElementTree as ET
        xml = ET.parse(window.ui_path)

        def process_element(el):
            name = el.attrib["name"]
            prop = el.find("property[@name='icon']")
            if prop is None: return None
            icon = prop.find("iconset").find("normaloff").text
            icon = icon[1:]

            action = getattr(window, name)
            icon = QIcon(os.path.dirname(os.path.abspath(__file__)) + "/" + "icons/." + icon)
            action.setIcon(icon)
            return action

        for el in xml.getroot().iter("action"):
            process_element(el)

        for el in xml.getroot().findall(".//widget[@class='QToolButton']"):
            process_element(el)

    def progress(self, s, value=None):
        if value is not None:
            s += " %.2f%%" % (value * 100)
            self.progress_dialog.setValue(int(value * 100))
        else:
            # Some super fake progress
            v = self.progress_dialog.value()
            v = int((v + 99) / 2)
            self.progress_dialog.setValue(v)

        self.progress_dialog.setLabelText(s)
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def open_binary(self, filename, arch=None):
        if arch is None:
            archs = Binary.list_architectures_from_file(filename)
            assert len(archs) > 0
            if len(archs) == 1:
                arch = archs[0]
            else:
                arch_strs = [str(arch) for arch in archs]
                selected = QInputDialog.getItem(None, "Select architecture", "The binary contains several architectures, please select one:", arch_strs, 0, False)
                ok = selected[1]
                if not ok:
                    return False
                selected = selected[0]
                idx = arch_strs.index(selected)
                arch = archs[idx]

        if not arch.can_open:
            QMessageBox.critical(None, "Not implemented", "Opening ARMv7 binaries is not implemented. Try AArch64.")
            return False

        self.progress_dialog = QProgressDialog("Opening binary...", None, 0, 100)
        self.progress_dialog.forceShow()
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        binary = Binary(filename, arch)
        binary.load_progress_callback = self
        binary.load()
        window = MainWindow(self, binary)

        # Binary loaded...
        qs = QSettings()
        recent_items = []
        if qs.contains("welcome_recent_items"):
            recent_items = qs.value("welcome_recent_items")
        item = ("%s (%s)" % (os.path.abspath(filename), arch.name), os.path.abspath(filename), arch.archvalue)
        if item in recent_items:
            recent_items = [i for i in recent_items if i != item]
        recent_items.insert(0, item)
        qs.setValue("welcome_recent_items", recent_items)
        qs.sync()

        if len(self.open_windows) > 0:
            r = self.open_windows[len(self.open_windows) - 1].geometry()
            r.moveLeft(r.left() + 20)
            r.moveTop(r.top() + 20)
            window.setGeometry(r)

        self.progress_dialog.close()
        window.show()
        self.open_windows.append(window)

        return True

    def window_closed(self, window):
        if window in self.open_windows:
            self.open_windows.remove(window)
            if len(self.open_windows) == 0:
                self.welcome_dialog = WelcomeDialog(self)
                self.welcome_dialog.show()

    def bring_to_front(self):
        global pid, cmd
        pid = os.getpid()
        cmd = '''/usr/bin/osascript -e 'tell app "System Events" to set frontmost of the first process whose unix id is %d to true' ''' % pid
        os.system(cmd)

    def appdata_dir(self):
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        strings = QStandardPaths.standardLocations(QStandardPaths.AppLocalDataLocation)
        dirname = strings[0]
        mkdir_p(dirname)
        return dirname

    def run(self):
        qapp = QApplication([])
        qapp.setApplicationName("Cricket")
        self.qapp = qapp
        qapp.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        qapp.setAttribute(Qt.AA_DontShowIconsInMenus, False)
        d = os.path.dirname(os.path.abspath(__file__)) + "/"
        qapp.setWindowIcon(QIcon(d + "icons/violin.png"))

        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.show()

        def excepthook(excType, excValue, tracebackobj):
            box = QMessageBox()
            box.setText(str(excValue))
            box.setIcon(QMessageBox.Critical)
            box.exec_()

        sys.excepthook = excepthook

        self.bring_to_front()
        qapp.exec_()





if __name__ == "__main__":
    App().run()
