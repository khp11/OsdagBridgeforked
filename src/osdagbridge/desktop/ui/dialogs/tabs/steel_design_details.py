from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

from osdagbridge.desktop.ui.docks.output_dock import (
    apply_field_style,
    NoScrollComboBox,
)
from osdagbridge.desktop.ui.utils.styled_scroll_area import StyledScrollArea


class SteelDesignDetailsTab(QWidget):

    def __init__(self, parent=None):
        self.member_fields = {}
        self.dim_fields = {}
        self.shear_fields = {}
        self.section_fields = {}
        self.stiffener_fields = {}

        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = StyledScrollArea()
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        container_layout.setSpacing(8)

        # ── TOP ROW: Member info (left) + CAD placeholder (right) ──────────
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        top_layout.setContentsMargins(0, 0, 0, 0)

        member_group = self._create_member_info_group()
        top_layout.addWidget(member_group, 2)

        self.cad_placeholder = QLabel()
        self.cad_placeholder.setFixedSize(300, 160)
        self.cad_placeholder.setAlignment(Qt.AlignCenter)
        self.cad_placeholder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cad_placeholder.setStyleSheet("""
            QLabel {
                border: 1px solid #CFCFCF;
                background-color: #F5F5F5;
            }
        """)
        top_layout.addWidget(self.cad_placeholder, 1)
        container_layout.addLayout(top_layout)

        # ── BODY: Dimensional + Shear (left) | Section Properties (right) ──
        body_layout = QHBoxLayout()
        body_layout.setSpacing(8)
        body_layout.setContentsMargins(0, 0, 0, 0)

        left_side = QVBoxLayout()
        left_side.setSpacing(8)
        left_side.setContentsMargins(0, 0, 0, 0)
        left_side.addWidget(self._create_dimensional_group())
        left_side.addWidget(self._create_shear_group())
        left_side.addStretch()

        right_side = QVBoxLayout()
        right_side.setSpacing(8)
        right_side.setContentsMargins(0, 0, 0, 0)
        right_side.addWidget(self._create_section_properties_group())
        right_side.addStretch()

        body_layout.addLayout(left_side, 2)
        body_layout.addLayout(right_side, 1)
        container_layout.addLayout(body_layout)

        # ── STIFFENER TABLE ─────────────────────────────────────────────────
        container_layout.addWidget(self._create_stiffener_group())

        # ── BOTTOM CAD placeholder ──────────────────────────────────────────
        container_layout.addWidget(self._create_bottom_cad_section())

        container_layout.addStretch()

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    # ── HELPERS ─────────────────────────────────────────────────────────────

    def _apply_groupbox_style(self, group):
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #333;
                border: 1px solid #90AF13;
                border-radius: 4px;
                margin-top: 6px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 8px;
                padding: 0 4px;
                background-color: white;
            }
            QLabel {
                color: #222222;
                font-size: 10px;
            }
        """)

    def _readonly_field(self):
        field = QLineEdit()
        field.setReadOnly(True)
        field.setFixedWidth(150)
        field.setFixedHeight(22)
        field.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        apply_field_style(field)
        return field

    def _tight_grid(self, group):
        """Return a QGridLayout attached to group with tight spacing."""
        layout = QGridLayout(group)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setVerticalSpacing(3)
        layout.setHorizontalSpacing(8)
        return layout

    # ── MEMBER INFO ──────────────────────────────────────────────────────────

    def _create_member_info_group(self):
        group = QGroupBox()
        self._apply_groupbox_style(group)

        layout = self._tight_grid(group)

        self.member_combo = NoScrollComboBox()
        apply_field_style(self.member_combo)
        self.member_combo.setFixedWidth(150)
        self.member_combo.setFixedHeight(22)
        self.member_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.grade_field = self._readonly_field()
        self.type_field  = self._readonly_field()

        layout.addWidget(QLabel("Member ID"),          0, 0)
        layout.addWidget(self.member_combo,             0, 1)
        layout.addWidget(QLabel("Grade of Material:"), 1, 0)
        layout.addWidget(self.grade_field,              1, 1)
        layout.addWidget(QLabel("Type:"),               2, 0)
        layout.addWidget(self.type_field,               2, 1)

        self.member_fields["member_id"]       = self.member_combo
        self.member_fields["grade_of_material"] = self.grade_field
        self.member_fields["section_type"]    = self.type_field

        return group

    # ── DIMENSIONAL ──────────────────────────────────────────────────────────

    def _create_dimensional_group(self):
        group = QGroupBox("Dimensional Details")
        self._apply_groupbox_style(group)

        layout = self._tight_grid(group)

        labels = {
            "section_designation":    "Section Designation",
            "section_class":          "Section Class",
            "total_depth":            "Total Depth (mm)",
            "web_thickness":          "Web Thickness (mm)",
            "top_flange_width":       "Top Flange Width (mm)",
            "top_flange_thickness":   "Top Flange Thickness (mm)",
            "bottom_flange_width":    "Bottom Flange Width (mm)",
            "bottom_flange_thickness":"Bottom Flange Thickness (mm)",
            "torsional_restraint":    "Torsional Restraint",
            "warping_restraint":      "Warping Restraint",
            "web_type":               "Web Type",
            "effective_slab_width":   "Effective Width of Slab (mm)",
        }

        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)
            field = self._readonly_field()
            layout.addWidget(field, row, 1)
            self.dim_fields[key] = field

        return group

    # ── SHEAR ────────────────────────────────────────────────────────────────

    def _create_shear_group(self):
        group = QGroupBox("Shear Connector Details")
        self._apply_groupbox_style(group)

        layout = self._tight_grid(group)

        labels = {
            "shear_material":             "Material",
            "shear_diameter":             "Diameter (mm)",
            "shear_height":               "Height (mm)",
            "shear_transverse_spacing":   "Transverse Spacing (mm)",
            "shear_studs_per_section":    "No. of Shear Studs per Section",
            "shear_longitudinal_spacing": "Average Longitudinal Spacing (mm)",
        }

        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)
            field = self._readonly_field()
            layout.addWidget(field, row, 1)
            self.shear_fields[key] = field

        return group

    # ── SECTION PROPERTIES ───────────────────────────────────────────────────

    def _create_section_properties_group(self):
        group = QGroupBox("Section Properties")
        self._apply_groupbox_style(group)

        layout = self._tight_grid(group)

        labels = {
            "mass":  "Mass, M (Kg/m)",
            "area":  "Sectional Area (cm²)",
            "iz":    "2nd Moment of Area, Iz (cm⁴)",
            "iv":    "2nd Moment of Area, Iv (cm⁴)",
            "rz":    "Radius of Gyration, rz (cm)",
            "rv":    "Radius of Gyration, rv (cm)",
            "zz":    "Elastic Modulus, Zz (cm³)",
            "zv":    "Elastic Modulus, Zv (cm³)",
            "zuz":   "Plastic Modulus, Zuz (cm³)",
            "zuv":   "Plastic Modulus, Zuv (cm³)",
            "it":    "Torsion Constant, It (cm⁴)",
            "iw":    "Warping Constant, Iw (cm⁶)",
        }

        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)
            field = self._readonly_field()
            layout.addWidget(field, row, 1)
            self.section_fields[key] = field

        return group

    # ── STIFFENER TABLE ──────────────────────────────────────────────────────

    def _create_stiffener_group(self):
        group = QGroupBox("Stiffener Details")
        self._apply_groupbox_style(group)

        layout = QVBoxLayout(group)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(0)

        self.stiffener_table = QTableWidget()
        self.stiffener_table.setRowCount(3)
        self.stiffener_table.setColumnCount(5)
        self.stiffener_table.setHorizontalHeaderLabels([
            "Type", "Grade of Material", "Thickness (mm)", "Width (mm)", "Spacing (mm)"
        ])

        row_names = ["Intermediate", "Longitudinal", "Bearing"]
        for row, name in enumerate(row_names):
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEnabled)
            self.stiffener_table.setItem(row, 0, item)
            for col in range(1, 5):
                empty = QTableWidgetItem("")
                empty.setFlags(Qt.ItemIsEnabled)
                self.stiffener_table.setItem(row, col, empty)

        self.stiffener_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stiffener_table.verticalHeader().setVisible(False)
        self.stiffener_table.verticalHeader().setDefaultSectionSize(26)
        self.stiffener_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.stiffener_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stiffener_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Fit table height exactly to content (header + 3 rows)
        header_h = self.stiffener_table.horizontalHeader().height()
        row_h    = self.stiffener_table.verticalHeader().defaultSectionSize()
        self.stiffener_table.setFixedHeight(header_h + row_h * 3 + 2)

        self.stiffener_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #CFCFCF;
                color: black;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #EAEAEA;
                color: black;
                font-weight: bold;
                border: 1px solid #CFCFCF;
                padding: 3px;
            }
            QTableWidget::item {
                color: black;
            }
        """)

        layout.addWidget(self.stiffener_table)
        return group

    # ── BOTTOM CAD PLACEHOLDER ───────────────────────────────────────────────

    def _create_bottom_cad_section(self):
        group = QGroupBox()
        group.setStyleSheet("""
            QGroupBox {
                border: 0px solid #CFCFCF;
                border-radius: 0px;
                background-color: white;
                margin-top: 0px;
                padding: 4px;
            }
        """)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)

        bottom_cad = QLabel()
        bottom_cad.setFixedSize(400, 200)
        bottom_cad.setAlignment(Qt.AlignCenter)
        bottom_cad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bottom_cad.setStyleSheet("""
            QLabel {
                border: 1px solid #CFCFCF;
                background-color: #F5F5F5;
            }
        """)

        layout.addWidget(bottom_cad, alignment=Qt.AlignCenter)
        return group

    # ── LOAD DATA  ──────────────────────────────────────────

    def load_data(self, cad_state: dict):
        if not cad_state:
            return

        for key, field in self.member_fields.items():
            value = cad_state.get(key, "")
            if isinstance(field, NoScrollComboBox):
                field.clear()
                field.addItem(str(value))
            else:
                field.setText(str(value))

        for key, field in self.dim_fields.items():
            field.setText(str(cad_state.get(key, "")))

        for key, field in self.shear_fields.items():
            field.setText(str(cad_state.get(key, "")))

        for key, field in self.section_fields.items():
            field.setText(str(cad_state.get(key, "")))

        if hasattr(self, "stiffener_table"):
            stiffener_map = {0: "intermediate", 1: "longitudinal", 2: "bearing"}
            for row, prefix in stiffener_map.items():
                grade     = cad_state.get(f"stiff_{prefix}_grade",     "")
                thickness = cad_state.get(f"stiff_{prefix}_thickness", "")
                width     = cad_state.get(f"stiff_{prefix}_width",     "")
                spacing   = cad_state.get(f"stiff_{prefix}_spacing",   "")

                self.stiffener_table.setItem(row, 1, QTableWidgetItem(str(grade)))
                self.stiffener_table.setItem(row, 2, QTableWidgetItem(str(thickness)))
                self.stiffener_table.setItem(row, 3, QTableWidgetItem(str(width)))
                self.stiffener_table.setItem(row, 4, QTableWidgetItem(str(spacing)))