import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QFrame,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QDoubleSpinBox,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QLabel,
    QSlider,
    QSpinBox,
    QFontDialog,
    QFileDialog,
)
import os
from ament_index_python.packages import get_package_share_directory
from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from functools import partial
import yaml
from yaml.loader import SafeLoader
from PyQt6.QtCore import pyqtSignal

# from py_modules.vision_functions_loader import VisionFunctionsLoader
# from py_modules.vision_pipeline_class import VisionPipeline
# import py_modules.type_classes as TC

from pm_vision_app.py_modules.vision_builder_widget import VisionBuilderWidget


class VisionAssistantAppMain(QMainWindow):
    def __init__(self, initial_pipeline_file: str = None):
        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Vision Assistant App")

        main_layout = QVBoxLayout()
        self.main_widget = VisionBuilderWidget(initial_pipeline_file=initial_pipeline_file)
        main_layout.addWidget(self.main_widget)

        # Create a menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = QAction("Open process", self)
        open_action.triggered.connect(self.main_widget.open_process_file)
        file_menu.addAction(open_action)

        # Create "New" action
        new_action = QAction("New process", self)
        new_action.triggered.connect(self.main_widget.create_new_file)
        file_menu.addAction(new_action)

        # Create 'save as' action
        save_as_action = QAction("Save process as", self)
        save_as_action.triggered.connect(self.main_widget.save_process_as)

        file_menu.addAction(save_as_action)

        central_widget.setLayout(main_layout)
        self.setGeometry(100, 100, 600, 800)



if __name__ == "__main__":
    pipeline_file = None
    for arg in sys.argv:
        # Check if the argument starts with "pipeline_file:"
        if arg.startswith("pipeline_file_path:"):
            # Extract the filename after the colon
            pipeline_file = arg.split(":")[1]
    app = QApplication(sys.argv)

    window = VisionAssistantAppMain(initial_pipeline_file=pipeline_file)
    window.show()
    sys.exit(app.exec())
