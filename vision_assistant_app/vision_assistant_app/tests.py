import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QFrame, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox
from PyQt6.QtCore import Qt

class YourMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Parameter Widgets Example")
        self.function_parameter_widgets = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create a QGroupBox to hold the parameter widgets with a frame
        parameter_group_box = QGroupBox("Function Parameters")
        parameter_group_layout = QFormLayout()
        parameter_group_box.setLayout(parameter_group_layout)
        
        # Create and add your parameter widgets to the parameter_group_layout
        self.create_function_parameters_layout(parameter_group_layout)
        
        layout.addWidget(parameter_group_box)
        self.setLayout(layout)
        
    def create_function_parameters_layout(self, layout):
        # Add Bool Widgets
        # ... (your existing code)

        # Add all the created widgets to the layout
        self.add_function_parameter_widgets_to_layout(layout)

    # Define your callback functions here

    def add_function_parameter_widgets_to_layout(self, layout):
        for widget in self.function_parameter_widgets:
            layout.addRow(widget)

def main():
    app = QApplication(sys.argv)
    window = YourMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
