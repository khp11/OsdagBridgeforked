from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)
from PySide6.QtCore import Qt


class SteelDesignAnalysisTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(scroll)
