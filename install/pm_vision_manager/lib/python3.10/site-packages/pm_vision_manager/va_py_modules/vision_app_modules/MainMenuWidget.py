from PyQt6.QtWidgets import QScrollArea, QMenuBar, QMessageBox, QMenu, QDialog, QHBoxLayout, QInputDialog, QTreeWidget, QTreeWidgetItem, QApplication, QGridLayout, QFrame, QMainWindow, QListWidget, QListWidgetItem, QDoubleSpinBox, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QComboBox, QTextEdit,QLabel,QSlider, QSpinBox, QFontDialog, QFileDialog
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QPixmap
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
    
    ######!!!!!!!!!!!!!!!!!!!!!#####
    ######!!!!!!!!!!!!!!!!!!!!!#####
    # This Ui code has been changed for clairity and better structure.
    # The old code is still here in case of missing information.
    ######!!!!!!!!!!!!!!!!!!!!!#####
    ######!!!!!!!!!!!!!!!!!!!!!#####


    # def initUI(self):
    #     # Grid layout
    #     self.main_layout = QGridLayout()
    #     #self.running_assistans_widget = QListWidget()
    #     #self.vision_processes_widget = QListWidget()
    #     self.vision_processes_widget = DraggableTreeWidget(logger=self.node.get_logger())

    #     self.camera_configs_widget = QListWidget()
    #     # add button
    #     #self.stop_assistant_button = QPushButton("Stop Vision Assistant")

    #     self.start_assistant_button = QPushButton ("Start VisionAssistant")
    #     #self.start_assistant_button.clicked.connect(self.start_vision_assistant)
        
    #     #self.referesh_running_assistant_button = QPushButton("Refresh Assistants")
    #     self.new_process_button = QPushButton("Create New Process")
    #     self.new_process_button.clicked.connect(self.create_new_process_file)

    #     #benutz bereits bestehende funktion zum updaten
    #     self.refresh_dtbs_button = QPushButton("Refresh databases")
    #     self.refresh_dtbs_button.clicked.connect(self.update_files)

    #     label_processes = QLabel("Vision Processes:")
    #     label_cameras = QLabel("Camera Configs:")
    #     #label_assistants = QLabel("Running Assistants:")
    #     label_text_output = QLabel("Log Output:")
    #     # add a text output box
    #     self.text_output = AppTextOutput()
    #     self.main_layout.addWidget(self.new_process_button, 0, 0)
    #     self.main_layout.addWidget(self.refresh_dtbs_button, 1, 0)
    #     self.main_layout.addWidget(self.start_assistant_button, 0, 1)
    #     self.main_layout.addWidget(label_processes, 2, 0)
    #     self.main_layout.addWidget(self.vision_processes_widget,3,0)
    #     self.main_layout.addWidget(label_cameras,1,1)
    #     self.main_layout.addWidget(self.camera_configs_widget,2,1)
    #     #self.main_layout.addWidget(label_assistants,3,0)
    #     #self.main_layout.addWidget(self.running_assistans_widget, 4, 0, 1, 2)
    #     #self.main_layout.addWidget(self.stop_assistant_button, 5, 0)
    #     #self.main_layout.addWidget(self.referesh_running_assistant_button, 5, 1)
    #     self.main_layout.addWidget(label_text_output, 3, 0)
    #     self.main_layout.addWidget(self.text_output, 4, 0, 1, 2)
    #     self.setGeometry(100, 100, 1000, 800)
    #     self.setLayout(self.main_layout)

    # def initUI(self):

    #     # Main layout - Grid provides precise control over widget placement
    #     self.main_layout = QGridLayout()
        
    #     # =============== WIDGET DEFINITIONS ===============
    #     # File management widgets
    #     self.vision_processes_widget = DraggableTreeWidget(logger=self.node.get_logger())
    #     self.camera_configs_widget = QListWidget()
        
    #     # Action buttons
    #     self.start_assistant_button = QPushButton("Start Vision Assistant")
    #     self.new_process_button = QPushButton("Create New Process")
    #     self.refresh_dtbs_button = QPushButton("Refresh Databases")
        
    #     # Log output
    #     self.text_output = AppTextOutput()
        
    #     # Labels for section headers
    #     label_processes = QLabel("Vision Processes:")
    #     label_cameras = QLabel("Camera Configs:")
    #     label_text_output = QLabel("Log Output:")
        
    #     # =============== CONNECT SIGNALS ===============
    #     self.new_process_button.clicked.connect(self.create_new_process_file)
    #     self.refresh_dtbs_button.clicked.connect(self.update_files)
        
    #     # =============== LAYOUT ORGANIZATION ===============
    #     # Row 0: Primary actions
    #     self.main_layout.addWidget(self.new_process_button, 0, 0)
    #     self.main_layout.addWidget(self.start_assistant_button, 0, 1)
        
    #     # Row 1: Secondary actions
    #     self.main_layout.addWidget(self.refresh_dtbs_button, 1, 0)
    #     self.main_layout.addWidget(label_cameras, 1, 1)
        
    #     # Row 2-3: File management section
    #     self.main_layout.addWidget(label_processes, 2, 0)
    #     self.main_layout.addWidget(self.vision_processes_widget, 3, 0)
    #     self.main_layout.addWidget(self.camera_configs_widget, 2, 2, 2, 1)  # Spans rows 2-3, column 2
        
    #     # Row 4-5: Log output section
    #     self.main_layout.addWidget(label_text_output, 4, 0)
    #     self.main_layout.addWidget(self.text_output, 5, 0, 2, 3)  # Spans 2 rows, 3 columns
        
    #     # =============== FINALIZE LAYOUT ===============
    #     self.setGeometry(100, 100, 2000, 1600)
    #     self.setLayout(self.main_layout)


    def initUI(self):
        """
        Initialize UI with modular sections using only QHBoxLayout and QVBoxLayout.

        """
        
        # =============== MAIN VERTICAL LAYOUT ===============
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # =============== TOP LAYER: jpg SECTIONS ===============
        top_bar = QWidget()  
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        package_share_dir = get_package_share_directory('pm_vision_manager')
        icon_path = os.path.join(package_share_dir, 'match.jpg')

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            image_label = QLabel()
            # Scale to wider size (e.g., 120 width, keep aspect ratio)
            pixmap = pixmap.scaled(200, 60, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            top_layout.addWidget(image_label)
            top_layout.addSpacing(10)  # Add some space after logo



        # =============== MIDDLE LAYER: FILE MANAGEMENT ===============
        middle_layer_layout = QHBoxLayout()
        middle_layer_layout.setSpacing(15)
        
        # ----- Section 3: Vision Processes -----
        vision_frame = QFrame()
        vision_frame.setFrameShape(QFrame.Shape.Box)
        vision_frame.setFrameShadow(QFrame.Shadow.Raised)
        vision_frame.setLineWidth(1)
        vision_frame.setMidLineWidth(0)
        
        vision_layout = QVBoxLayout()
        vision_layout.setSpacing(10)
        vision_layout.setContentsMargins(15, 15, 15, 15)

        vision_label = QLabel("Vision Processes")
        vision_label_font = QFont()
        vision_label_font.setBold(True)
        vision_label_font.setPointSize(11)
        vision_label.setFont(vision_label_font)
        vision_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        vision_buttons_layout = QHBoxLayout()
        
        self.start_assistant_button = QPushButton("Start Vision Assistant")
        self.new_process_button = QPushButton("Create New Process")
        self.refresh_dtbs_button = QPushButton("↻")
        self.refresh_dtbs_button.setStyleSheet("""
            QPushButton {
                color: green;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        self.start_assistant_button.setFixedWidth(200)
        self.new_process_button.setFixedWidth(200)

        self.start_assistant_button.clicked.connect(self.start_vision_assistant)
        self.new_process_button.clicked.connect(self.create_new_process_file)
        self.refresh_dtbs_button.clicked.connect(self.update_files)
        self.refresh_dtbs_button.setToolTip("Refresh vision processes and camera configs")

        vision_buttons_layout.addWidget(vision_label)
        vision_buttons_layout.addWidget(self.refresh_dtbs_button)
        vision_buttons_layout.addStretch(1)  # Push buttons to the left

        vision_buttons_layout.addWidget(self.start_assistant_button)
        vision_buttons_layout.addWidget(self.new_process_button)
        

        self.vision_processes_widget = DraggableTreeWidget(logger=self.node.get_logger())
        self.vision_processes_widget.setMinimumHeight(600)
        self.vision_processes_widget.setMinimumWidth(800)
        
        #vision_layout.addWidget(vision_label)
        vision_layout.addLayout(vision_buttons_layout)
        vision_layout.addWidget(self.vision_processes_widget)
        vision_frame.setLayout(vision_layout)
        
        # ----- Section 4: Camera Configs -----
        camera_frame = QFrame()
        camera_frame.setFrameShape(QFrame.Shape.Box)
        camera_frame.setFrameShadow(QFrame.Shadow.Raised)
        camera_frame.setLineWidth(1)
        camera_frame.setMidLineWidth(0)
        
        camera_layout = QVBoxLayout()
        camera_layout.setSpacing(10)
        camera_layout.setContentsMargins(15, 15, 15, 15)
        
        camera_label = QLabel("Camera Configs")
        camera_label_font = QFont()
        camera_label_font.setBold(True)
        camera_label_font.setPointSize(11)
        camera_label.setFont(camera_label_font)
        camera_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.camera_configs_widget = QListWidget()
        self.camera_configs_widget.setMinimumHeight(600)
        self.camera_configs_widget.setMinimumWidth(400)
        
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_configs_widget)
        camera_frame.setLayout(camera_layout)
        
        # Add sections to middle layer
        middle_layer_layout.addWidget(vision_frame)
        middle_layer_layout.addWidget(camera_frame)
        
        # Create middle layer widget
        middle_layer_widget = QWidget()
        middle_layer_widget.setLayout(middle_layer_layout)
        
        # =============== BOTTOM LAYER: LOG OUTPUT ===============
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.Shape.Box)
        log_frame.setFrameShadow(QFrame.Shadow.Raised)
        log_frame.setLineWidth(1)
        log_frame.setMidLineWidth(0)
        
        log_layout = QVBoxLayout()
        log_layout.setSpacing(10)
        log_layout.setContentsMargins(15, 15, 15, 15)
        
        log_label = QLabel("Log Output")
        log_label_font = QFont()
        log_label_font.setBold(True)
        log_label_font.setPointSize(11)
        log_label.setFont(log_label_font)
        log_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.text_output = AppTextOutput()
        self.text_output.setMinimumHeight(300)
        
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.text_output)
        log_frame.setLayout(log_layout)
        
        # =============== ASSEMBLE MAIN LAYOUT ===============
        # Add all layers to main layout
        main_layout.addWidget(top_bar)
        main_layout.addWidget(middle_layer_widget)
        main_layout.addWidget(log_frame)
        main_layout.addStretch(1)  # Small stretch at bottom
        
        # =============== SET WINDOW PROPERTIES ===============
        self.setGeometry(100, 100, 2000, 1600)
        self.setLayout(main_layout)

    def update_files(self):
        self.node.get_logger().info("Updating files...")
        self.text_output.append_white_text("Updating files...")  # Changed to blue for info
        
        package_share_directory = get_package_share_directory('pm_vision_manager')
        path_config_path = package_share_directory + '/vision_assistant_path_config.yaml'
        
        with open(path_config_path, 'r') as file:
            FileData = yaml.safe_load(file)
            config = FileData["vision_assistant_path_config"]
            self.process_library_path=config["process_library_path"]
            camera_config_path=config["camera_config_path"]
            
            self.node.get_logger().info("Start getting files...")
            self.text_output.append_white_text("Start getting files...")  # Changed to blue
            
            vision_processes = self.get_files_in_dir(directory=self.process_library_path,file_end='.json', exclude_str=['results'])
            vision_cameras = self.get_files_in_dir(directory=camera_config_path,file_end='.yaml', exclude_str=['vision_assistant'])
            
            self.node.get_logger().info("End getting files...")
            self.text_output.append_white_text("End getting files...")  # Changed to blue
            
            self.vision_processes_widget.clear()
            self.camera_configs_widget.clear()
            self.text_output.append_white_text("Cleared vision processes and camera configs widgets")
            
            self.populate_tree(vision_processes)
            self.text_output.append_green_text(f"Populated tree with {len(vision_processes)} vision processes")
            
            # for process in vision_processes:
            #     self.vision_processes_widget.addItem(process)
            # # Add sub-items or attributes if needed
            
            for camera in vision_cameras:
                self.camera_configs_widget.addItem(camera)
            
            self.text_output.append_green_text(f"Added {len(vision_cameras)} camera configs")

        self.node.get_logger().info("Updating files...")
        self.text_output.append_green_text("Files update completed successfully!")

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
            
            self.node.get_logger().info(f"Creating new process file: {new_process_file}")
            self.text_output.append_white_text(f"Creating new process file: {process_name}")
            
            with open(new_process_file, 'w') as file:
                default_process_dict = VisionProcessClass.create_default_process_dict(process_name)
                json.dump(default_process_dict, file, indent=4)
                
            self.text_output.append_green_text(f"Successfully created process file: {process_name}")
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
        self.text_output.append_orange_text(f"Selected process: {selected_process}")  # Changed to orange for warning
        
        selected_camera = self.camera_configs_widget.currentItem()
        if selected_process and selected_camera:
            self.text_output.append_white_text("Both process and camera selected, opening ID dialog...")
            new_id, dialog_ok = self.enter_id_dialog()
            if not dialog_ok:
                self.text_output.append_orange_text("ID dialog cancelled")
                return
            if new_id == '':
                self.text_output.append_red_text("No Id entered!")
                return
            else:
                self.text_output.append_green_text(f"ID entered: {new_id}")
                # Add your vision assistant startup logic here

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

class DraggableTreeWidget(QTreeWidget):
    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        #self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        #self.vision_processes_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropMode(QTreeWidget.DragDropMode.DragDrop)        
        self.setDefaultDropAction(Qt.DropAction.ActionMask)
        self.logger = logger

    def dropEvent(self, event):
        target_item = self.itemAt(event.position().toPoint())
        source_item = self.currentItem()

        if source_item and target_item:
            source_path = self.get_full_path(source_item)
            target_path = self.get_full_path(target_item)

            if not source_path.endswith('.json') or not target_path.endswith('.json'):
                self.logger.warn("Drag and drop only allowed between .json files")
                QMessageBox.warning(self, "Invalid Operation", "Drag and drop only allowed between .json files")
                return

            if source_path == target_path:
                self.logger.warn("Cannot drop onto the same file.")
                QMessageBox.warning(self, "Invalid Operation", "Cannot drop onto the same file.")
                return

            # ✅ Ask for confirmation
            reply = QMessageBox.question(
                self,
                "Copy Vision Pipeline",
                f"Do you want to copy the contents of:\n\n{source_path}\n\ninto:\n\n{target_path}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.logger.warn(f"Copying '{source_path}' into '{target_path}'")
                QMessageBox.information(self, "Copy Started", f"Copying '{os.path.basename(source_path)}' into '{os.path.basename(target_path)}'")
                
                copy_success = VisionProcessClass.copy_vision_pipeline_from_file_to_file(
                    source_path, target_path, self.logger
                )
                
                if copy_success:
                    self.logger.info("Copy completed successfully")
                    QMessageBox.information(self, "Copy Complete", "File copy completed successfully")
                else:
                    self.logger.error("Copy failed")
                    QMessageBox.warning(self, "Copy Failed", "File copy failed")
            else:
                self.logger.warn("Copy cancelled by user.")
                QMessageBox.information(self, "Cancelled", "Copy operation cancelled by user")
                return  # Don't proceed with UI drop

        event.ignore()  # prevent Qt from changing tree structure

    def startDrag(self, supported_actions):
        current = self.currentItem()
        if current:
            path = self.get_full_path(current)
            if not path.endswith('.json'):
                self.logger.warn("Only .json files can be dragged")
                QMessageBox.warning(self, "Invalid Operation", "Only .json files can be dragged")
                return  # Prevent dragging
        super().startDrag(supported_actions)

    def get_full_path(self, item):
        parts = []
        while item:
            parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(*parts)

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