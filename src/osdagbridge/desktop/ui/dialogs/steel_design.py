from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy


from osdagbridge.desktop.ui.dialogs.tabs.steel_design_details import SteelDesignDetailsTab
from osdagbridge.desktop.ui.dialogs.tabs.steel_design_analysis import SteelDesignAnalysisTab
from osdagbridge.desktop.ui.dialogs.tabs.steel_design_check import SteelDesignCheckTab



class SteelDesign(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Steel Design")
        self.resize(800, 800)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(2)

        # HEADER 
        header = QLabel("Steel Design")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(40)

        header.setStyleSheet("""
            background-color: #90AF13;
            color: white;
            font-weight: bold;
            font-size: 14px;
            border-radius: 6px;
        """)

        main_layout.addWidget(header)
        main_layout.setStretch(0, 0)  # header


        # TABS 
        self.tabs = QTabWidget()
        # Make tab widget expand fully
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make tabs stretch equally across full width
        self.tabs.setDocumentMode(True)  # important
        self.tabs.tabBar().setExpanding(True)
        self.tabs.tabBar().setUsesScrollButtons(False)


        self.tabs.setStyleSheet("""
    QTabWidget::pane {
        border: none;
    }

    QTabBar {
        qproperty-drawBase: 0;
    }

    QTabBar::tab {
        background: #E6E6E6;
        color: black;
        border: 1px solid #CCCCCC;
        padding: 8px 0px;
        border-radius: 8px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #90AF13;
        color: white;   
        font-weight: bold;
        border: 1px solid #90AF13;
    }

    QTabBar::tab:hover {
        background: #DADADA;
    }
""")




        self.details_tab = SteelDesignDetailsTab(self)
        self.tabs.addTab(self.details_tab, "Details")
        self.tabs.addTab(SteelDesignAnalysisTab(self), "Analysis Results")
        self.tabs.addTab(SteelDesignCheckTab(self), "Design Check")


        main_layout.addWidget(self.tabs)
        main_layout.setStretch(1, 1)  # tabs take full space


        # LOAD cad_state INTO DETAILS TAB
        main_window = self.parent()

        if hasattr(main_window, "cad_state"):
            self.details_tab.load_data(main_window.cad_state)

