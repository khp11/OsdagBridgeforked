from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt

from osdagbridge.desktop.ui.docks.output_dock import (
    apply_field_style,
    NoScrollComboBox
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

        scroll_area = StyledScrollArea()
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(12)

        # TOP ROW - >MEMBER INFO + CAD

        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        member_group = self._create_member_info_group()
        top_layout.addWidget(member_group, 2)

        self.cad_placeholder = QWidget()
        self.cad_placeholder.setMinimumSize(260, 280)
        self.cad_placeholder.setMaximumWidth(300)
        self.cad_placeholder.setStyleSheet("""
            QWidget {
                border: 1px solid #CFCFCF;
                background-color: #F5F5F5;
            }
        """)

        top_layout.addWidget(self.cad_placeholder, 1)

        container_layout.addLayout(top_layout)

        # DIMENSIONAL 

        dim_row = QHBoxLayout()
        dim_row.setSpacing(15)

        dim_group = self._create_dimensional_group()
        dim_row.addWidget(dim_group, 2)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dim_row.addWidget(spacer, 1)

        container_layout.addLayout(dim_row)

        # SHEAR + SECTION PROPERTIES ROW

        shear_section_row = QHBoxLayout()
        shear_section_row.setSpacing(15)

        shear_group = self._create_shear_group()
        shear_section_row.addWidget(shear_group, 2)

        section_group = self._create_section_properties_group()
        shear_section_row.addWidget(section_group, 1)

        container_layout.addLayout(shear_section_row)

        # STIFFENER

        container_layout.addWidget(self._create_stiffener_group())
        #bottom cad
        container_layout.addWidget(self._create_bottom_cad_section())
        container_layout.addStretch()

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    
    #bottom cad
    def _create_bottom_cad_section(self):
        group = QGroupBox()
        #self._apply_groupbox_style(group)

        layout = QVBoxLayout(group)

        cad_area = QWidget()
        cad_area.setMinimumHeight(300)
        cad_area.setMinimumWidth(300)

        cad_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        cad_area.setStyleSheet("""
            QWidget {
                border: 0px solid #CFCFCF;
                background-color: #F5F5F5;
            }
        """)

        layout.addWidget(cad_area)

        return group

    
    # GROUP STYLE

    def _apply_groupbox_style(self, group):
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #333;
                border: 1px solid #90AF13;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
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

        #  Make size constant
        field.setFixedWidth(150)   # adjust width
        field.setFixedHeight(26)   # adjust height

        # Prevent expansion
        field.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        apply_field_style(field)

        return field


    # MEMBER INFO

    def _create_member_info_group(self):
        group = QGroupBox()
        self._apply_groupbox_style(group)

        layout = QGridLayout(group)
        layout.setVerticalSpacing(6)
        layout.setHorizontalSpacing(20)

        self.member_combo = NoScrollComboBox()
        apply_field_style(self.member_combo)
        self.member_combo.setFixedWidth(150)   # same width as your readonly fields
        self.member_combo.setFixedHeight(26)   # same height
        self.member_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.grade_field = self._readonly_field()
        self.type_field = self._readonly_field()
 


        layout.addWidget(QLabel("Member ID"), 0, 0)
        layout.addWidget(self.member_combo, 0, 1)

        layout.addWidget(QLabel("Grade of Material:"), 1, 0)
        layout.addWidget(self.grade_field, 1, 1)

        layout.addWidget(QLabel("Type:"), 2, 0)
        layout.addWidget(self.type_field, 2, 1)
        self.member_fields["member_id"] = self.member_combo
        self.member_fields["grade_of_material"] = self.grade_field
        self.member_fields["section_type"] = self.type_field


        return group

    # DIMENSIONAL

    def _create_dimensional_group(self):
        group = QGroupBox("Dimensional Details")
        self._apply_groupbox_style(group)

        layout = QGridLayout(group)
        layout.setVerticalSpacing(6)
        layout.setHorizontalSpacing(15)

        labels = {
    "section_designation": "Section Designation",
    "section_class": "Section Class",
    "total_depth": "Total Depth (mm)",
    "web_thickness": "Web Thickness (mm)",
    "top_flange_width": "Top Flange Width (mm)",
    "top_flange_thickness": "Top Flange Thickness (mm)",
    "bottom_flange_width": "Bottom Flange Width (mm)",
    "bottom_flange_thickness": "Bottom Flange Thickness (mm)",
    "torsional_restraint": "Torsional Restraint",
    "warping_restraint": "Warping Restraint",
    "web_type": "Web Type",
    "effective_slab_width": "Effective Width of Slab (mm)",
            }


        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)
            field = self._readonly_field()
            layout.addWidget(field, row, 1)
            self.dim_fields[key] = field
             # or correct dict

        return group

    # SHEAR

    def _create_shear_group(self):
        group = QGroupBox("Shear Connector Details")
        self._apply_groupbox_style(group)

        layout = QGridLayout(group)
        layout.setVerticalSpacing(6)
        layout.setHorizontalSpacing(15)

        # Dictionary: cad_state_key → UI Label
        labels = {
            "shear_material": "Material",
            "shear_diameter": "Diameter (mm)",
            "shear_height": "Height (mm)",
            "shear_transverse_spacing": "Transverse Spacing (mm)",
            "shear_studs_per_section": "No. of Shear Studs per Section",
            "shear_longitudinal_spacing": "Average Longitudinal Spacing (mm)",
        }

        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)

            field = self._readonly_field()
            layout.addWidget(field, row, 1)

            # Store reference for load_data()
            self.shear_fields[key] = field

        return group


    # SECTION PROPERTIES

    def _create_section_properties_group(self):
        group = QGroupBox("Section Properties")
        self._apply_groupbox_style(group)

        layout = QGridLayout(group)
        layout.setVerticalSpacing(6)
        layout.setHorizontalSpacing(15)

        labels = {
            "mass": "Mass, M (Kg/m)",
            "area": "Sectional Area (cm2)",
            "iz": "2nd Moment of Area, Iz (cm4)",
            "iv": "2nd Moment of Area, Iv (cm4)",
            "rz": "Radius of Gyration, rz (cm)",
            "rv": "Radius of Gyration, rv (cm)",
            "zz": "Elastic Modulus, Zz (cm3)",
            "zv": "Elastic Modulus, Zv (cm3)",
            "zuz": "Plastic Modulus, Zuz (cm3)",
            "zuv": "Plastic Modulus, Zuv (cm3)",
            "it": "Torsion Constant, It (cm4)",
            "iw": "Warping Constant, Iw (cm6)",
            }


        for row, (key, text) in enumerate(labels.items()):
            layout.addWidget(QLabel(text), row, 0)
            field = self._readonly_field()
            layout.addWidget(field, row, 1)
            self.section_fields[key] = field


        return group

    # STIFFENER

    def _create_stiffener_group(self):
        group = QGroupBox("Stiffener Details")
        self._apply_groupbox_style(group)

        layout = QGridLayout(group)
        layout.setVerticalSpacing(6)
        layout.setHorizontalSpacing(15)

        headers = ["Type", "Grade of Material", "Thickness (mm)", "Width (mm)", "Spacing (mm)"]

        for col, header in enumerate(headers):
            layout.addWidget(QLabel(header), 0, col)

        rows = ["Intermediate", "Longitudinal", "Bearing"]

        for row, name in enumerate(rows, start=1):
            layout.addWidget(QLabel(name), row, 0)
            for col in range(1, 5):
                layout.addWidget(self._readonly_field(), row, col)

        return group
    def load_data(self, cad_state: dict):
        if not cad_state:
            return

        # MEMBER
        for key, field in self.member_fields.items():
            value = cad_state.get(key, "")
            if isinstance(field, NoScrollComboBox):
                field.clear()
                field.addItem(str(value))
            else:
                field.setText(str(value))

        # DIMENSIONAL
        for key, field in self.dim_fields.items():
            field.setText(str(cad_state.get(key, "")))

        # SHEAR
        for key, field in self.shear_fields.items():
            field.setText(str(cad_state.get(key, "")))

        # SECTION PROPERTIES
        for key, field in self.section_fields.items():
            field.setText(str(cad_state.get(key, "")))

        # STIFFENER
        for key, field in self.stiffener_fields.items():
            field.setText(str(cad_state.get(key, "")))

