from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget


class MyTreeWidget(QTreeWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            selected_item = self.selectedItems()[0] if len(self.selectedItems()) > 0 else None
            if selected_item:
                if selected_item.childCount() == 0 or selected_item.isExpanded() == False:
                    p = selected_item.parent()
                    if p is not None:
                        selected_item.setSelected(False)
                        p.setSelected(True)
                        self.setCurrentItem(p)
                        return

        super(MyTreeWidget, self).keyPressEvent(event)
