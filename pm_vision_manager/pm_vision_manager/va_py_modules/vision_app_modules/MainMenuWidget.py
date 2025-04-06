from PyQt6.QtWidgets import QScrollArea, QMenuBar, QMenu, QDialog, QHBoxLayout, QInputDialog, QTreeWidget, QTreeWidgetItem, QApplication, QGridLayout, QFrame, QMainWindow, QListWidget, QListWidgetItem, QDoubleSpinBox, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QComboBox, QTextEdit,QLabel,QSlider, QSpinBox, QFontDialog, QFileDialog
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from threading import Thread 
import sys
#from ros_sequential_action_programmer.submodules.action_classes.RecomGenerator import RecomGenerator
from ros_sequential_action_programmer.submodules.RsapApp_submodules.AppTextWidget import AppTextOutput
import yaml
from ament_index_python.packages import PackageNotFoundError
from functools import partial
import json

from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass


class MainMenuWidget(QWidget):
    def __init__(self, node:Node):
        super().__init__()
        self.node = node
        self.initUI()
        self.update_files()
    
    def initUI(self):
        # Grid layout
        self.main_layout = QGridLayout()
        #self.running_assistans_widget = QListWidget()
        #self.vision_processes_widget = QListWidget()
        self.vision_processes_widget = QTreeWidget()
        self.vision_processes_widget.setHeaderHidden(True)
        self.camera_configs_widget = QListWidget()
        # add button
        #self.stop_assistant_button = QPushButton("Stop Vision Assistant")

        self.start_assistant_button = QPushButton("Start Vision Assistant")
        #self.start_assistant_button.clicked.connect(self.start_vision_assistant)
        
        #self.referesh_running_assistant_button = QPushButton("Refresh Assistants")
        self.new_process_button = QPushButton("Create New Process")
        self.new_process_button.clicked.connect(self.create_new_process_file)
        label_processes = QLabel("Vision Processes:")
        label_cameras = QLabel("Camera Configs:")
        #label_assistants = QLabel("Running Assistants:")
        label_text_output = QLabel("Log Output:")
        # add a text output box
        self.text_output = AppTextOutput()
        self.main_layout.addWidget(self.new_process_button, 0, 0)
        self.main_layout.addWidget(self.start_assistant_button, 0, 1)
        self.main_layout.addWidget(label_processes,1,0)
        self.main_layout.addWidget(self.vision_processes_widget,2,0)
        self.main_layout.addWidget(label_cameras,1,1)
        self.main_layout.addWidget(self.camera_configs_widget,2,1)
        #self.main_layout.addWidget(label_assistants,3,0)
        #self.main_layout.addWidget(self.running_assistans_widget, 4, 0, 1, 2)
        #self.main_layout.addWidget(self.stop_assistant_button, 5, 0)
        #self.main_layout.addWidget(self.referesh_running_assistant_button, 5, 1)
        self.main_layout.addWidget(label_text_output, 3, 0)
        self.main_layout.addWidget(self.text_output, 4, 0, 1, 2)
        self.setGeometry(100, 100, 2000, 1600)
        self.setLayout(self.main_layout)


    def update_files(self):
        self.node.get_logger().info("Updating files...")
        package_share_directory = get_package_share_directory('pm_vision_manager')
        path_config_path = package_share_directory + '/vision_assistant_path_config.yaml'
        with open(path_config_path, 'r') as file:
            FileData = yaml.safe_load(file)
            config = FileData["vision_assistant_path_config"]
            self.process_library_path=config["process_library_path"]
            camera_config_path=config["camera_config_path"]
            self.node.get_logger().info("Start getting files...")
            vision_processes = self.get_files_in_dir(directory=self.process_library_path,file_end='.json', exclude_str=['results'])
            vision_cameras = self.get_files_in_dir(directory=camera_config_path,file_end='.yaml', exclude_str=['vision_assistant'])
            self.node.get_logger().info("End getting files...")
            self.vision_processes_widget.clear()
            self.camera_configs_widget.clear()
            self.populate_tree(vision_processes)
            
            # for process in vision_processes:
            #     self.vision_processes_widget.addItem(process)
            # # Add sub-items or attributes if needed
            
            for camera in vision_cameras:
                self.camera_configs_widget.addItem(camera)

        self.node.get_logger().info("Updating files...")

    def populate_tree(self, paths):
        root_items = {}

        for path in paths:
            parts = os.path.normpath(path).split(os.sep)
            current_items = root_items

            for i, part in enumerate(parts):
                if part not in current_items:
                    item = QTreeWidgetItem([part])
                    current_items[part] = {"item": item, "children": {}}

                    if i == 0:
                        self.vision_processes_widget.addTopLevelItem(item)
                    else:
                        parent_item = current_items_parent["item"]
                        parent_item.addChild(item)

                current_items_parent = current_items[part]
                current_items = current_items_parent["children"]
    
    def create_new_process_file(self):
        new_process_file, _ = QFileDialog.getSaveFileName(self, "Save File", self.process_library_path, "JSON Files (*.json)")
        if new_process_file:
            process_name = new_process_file.split('/')[-1]
            if not new_process_file.endswith('.json'):
                new_process_file = new_process_file + '.json'
            with open(new_process_file, 'w') as file:
                default_process_dict = VisionProcessClass.create_default_process_dict(process_name)
                json.dump(default_process_dict, file, indent=4)
                
            self.update_files()

    # def get_selected_process(self):
    #     selected_process = self.vision_processes_widget.currentItem()
    #     if selected_process:
    #         return selected_process.text()
    #     else:
    #         return None
        
    def get_selected_process(self):
        item = self.vision_processes_widget.currentItem()
        if item and item.text(0).endswith('.json'):
            full_path = []
            while item:
                full_path.insert(0, item.text(0))
                item = item.parent()
            return os.path.join(*full_path)
        else:
            return None
    def get_selected_camera(self):
        selected_camera = self.camera_configs_widget.currentItem()
        if selected_camera:
            return selected_camera.text()
        else:
            return None
        
    def start_vision_assistant(self):
        selected_process = self.get_selected_process()
        self.node.get_logger().error("Selected process: " + str(selected_process))
        selected_camera = self.camera_configs_widget.currentItem()
        if selected_process and selected_camera:
            new_id, dialog_ok = self.enter_id_dialog()
            if not dialog_ok:
                return
            if new_id == '':
                self.text_output.append_red_text("No Id entered!")
                return

        else:
            self.text_output.append_red_text("No process or camera selected!")

    def enter_id_dialog(self) -> bool:
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter a unique process Id for new assistant:')
        return text, ok
    
    @staticmethod
    def get_files_in_dir(directory: str, file_end: str, exclude_str: list[str] = []):
        """
        This function returns a list of files in the directory with the given file_end.
        Parameters:
        param: directory: str
        file_end: str
        exclude_str: list[str]
        """
        files = []
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(file_end):
                    valid_file = True
                    for string in exclude_str:
                        if string in filename:
                            valid_file = False
                            break  # No need to continue checking once a match is found
                    if valid_file:    
                        files.append(os.path.relpath(os.path.join(foldername, filename), directory))
        return files
    

class DummyMain(QMainWindow):

    def __init__(self, node:Node):
        super().__init__()
        self.node = node
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = MainMenuWidget(self.node)
        self.w.show()

def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=6) 

    app = QApplication(sys.argv)
    just_a_node = Node('my_Node')
    executor.add_node(just_a_node)

    thread = Thread(target=executor.spin)
    thread.start()
    ex = DummyMain(just_a_node)
    try:
        ex.show()
        sys.exit(app.exec())

    finally:
        just_a_node.destroy_node()
        executor.shutdown()
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()

