from PyQt6.QtWidgets import QTextEdit,QWidget,QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QTreeView, QApplication, QSizePolicy, QPushButton, QGridLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtGui import QColor, QTextCursor, QFont, QImage, QPixmap, QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt, QByteArray
from pm_vision_manager.va_py_modules.vision_utils import get_screen_resolution, image_resize
from PyQt6.QtCore import Qt, QByteArray, pyqtSignal, QObject
import cv2
import numpy as np
from pm_vision_app.py_modules.vision_builder_widget import VisionBuilderWidget
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass

class ImageSelectSignal(QObject):
    signal = pyqtSignal(str)

class ExitAssistantSignal(QObject):
    signal = pyqtSignal()

class ImageDisplayWidget(QWidget):
    def __init__(self, vision_instance: VisionProcessClass = None, camera_topic:str = None):
        super(ImageDisplayWidget, self).__init__()
        
        self.main_layout = QGridLayout()
        self.properties_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_topic_button = QPushButton("Subscribe to topic")
        self.execute_cross_val_button = QPushButton("Execute Crossvalidation")
        self.refresh_database_button = QPushButton("Refresh database")
        
        self.init_metadata_widget()
        
        self.image_select_signal = ImageSelectSignal()
        self.exit_assistant_signal = ExitAssistantSignal()

        self.cross_val_images_widget = QListWidget()
        self.cross_val_images_widget.clicked.connect(self.cross_val_images_widget_clicked)

        self.screen_resolution = get_screen_resolution()
        self.screen_height = int(self.screen_resolution["height"].decode("UTF-8"))
        
        self.properties_layout.addWidget(self.execute_cross_val_button)
        self.properties_layout.addWidget(self.sub_topic_button)
        self.properties_layout.addWidget(self.refresh_database_button)
        self.properties_layout.addWidget(self.cross_val_images_widget)
        
        self.main_layout.addWidget(self.image_label, 0, 0, 1, 1)
        self.main_layout.addLayout(self.properties_layout, 0, 1, 1, 1)
        self.add_builder_widget()
        self.setLayout(self.main_layout)
        
        # Store references
        self.camera_topic = camera_topic
        self.vi = None
        
        # Set vision instance if provided
        if vision_instance is not None:
            self.set_vision_instance(vision_instance)
        
        # Connect refresh button ONCE
        self.refresh_database_button.clicked.connect(self.refresh_database)

    def cross_val_images_widget_clicked(self):
        item = self.cross_val_images_widget.currentItem()
        if item is not None:
            self.image_select_signal.signal.emit(item.text())
            self.image_name_widget.setText(item.text())
    
    def add_builder_widget(self):
        self.vision_builder_widget = VisionBuilderWidget()
        self.main_layout.addWidget(self.vision_builder_widget, 0, 3, 1, 3)

    def set_image_to_topic(self):
        if self.camera_topic:
            self.image_name_widget.setText(self.camera_topic)
            self.image_select_signal.signal.emit(self.camera_topic)

    def set_image(self, image:np.ndarray, screen_height = None):
        if image is None:
            return
        
        height, width, channel = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if screen_height is None:
            screen_height = self.screen_height

        image = image_resize(image, height=screen_height-400)
        height, width, channel = image.shape
        bytes_per_line = 3 * width

        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.clear()
        self.image_label.setPixmap(pixmap)
        self.image_label.repaint()
        self.update()
    
    def set_image_result(self, image:np.ndarray, result_dict:dict, screen_height = None):
        self.set_image(image, screen_height)
        self.set_result_dict(result_dict)

    def init_metadata_widget(self):
        metadata_layout = QGridLayout()
        _process_uid_widget = QLabel("Process UID:")
        _mode_widget = QLabel("Mode:")
        _camera_name_widget = QLabel("Camera name:")
        _image_name_widget = QLabel("Image name:")
        _crossval_info_widget = QLabel("Images Crossvalidation:")

        self.process_uid_widget = QLabel()
        self.mode_widget = QLabel()
        self.camera_name_widget = QLabel()
        self.image_name_widget = QLabel()
        self.crossval_info_widget = QLabel()
        
        metadata_layout.addWidget(_process_uid_widget, 0, 0)
        metadata_layout.addWidget(self.process_uid_widget, 0, 1)
        metadata_layout.addWidget(_mode_widget, 1, 0)
        metadata_layout.addWidget(self.mode_widget, 1, 1)
        metadata_layout.addWidget(_camera_name_widget, 2, 0)
        metadata_layout.addWidget(self.camera_name_widget, 2, 1)
        metadata_layout.addWidget(_image_name_widget, 3, 0)
        metadata_layout.addWidget(self.image_name_widget, 3, 1)
        metadata_layout.addWidget(_crossval_info_widget, 4, 0)
        metadata_layout.addWidget(self.crossval_info_widget, 4, 1)

        self.properties_layout.addLayout(metadata_layout)
        self.results_dict_tree = QTreeWidget()
        self.results_dict_tree.setHeaderLabels(["Vision results"])
        self.properties_layout.addWidget(self.results_dict_tree)

    def set_image_source(self, image_name:str):
        self.image_name_widget.setText(image_name)
    
    def set_crossval_info(self, current_image:int, total_images:int):
        self.crossval_info_widget.setText(f"{current_image}/{total_images}")
    
    def set_result_dict(self, result_dict:dict):
        self.results_dict_tree.clear()
        self.populate_log_widget(result_dict)
        self.results_dict_tree.expandAll()
    
    def populate_log_widget(self, data, parent=None):
        if parent is None:
            parent = self.results_dict_tree

        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent, [str(key)])
                self.populate_log_widget(value, item)
        elif isinstance(data, list):
            for index, item_data in enumerate(data):
                item = QTreeWidgetItem(parent, [f"[{index}]"])
                self.populate_log_widget(item_data, item)
        else:
            item = QTreeWidgetItem(parent, [str(data)])

    def set_vision_instance(self, vision_instance: VisionProcessClass):
        """Set or update the vision instance"""
        self.vi = vision_instance
        if self.vi is not None:
            # Auto-set camera topic if available
            if hasattr(self.vi, 'camera_subscription_topic'):
                self.camera_topic = self.vi.camera_subscription_topic
                self.sub_topic_button.clicked.connect(self.set_image_to_topic)
            
            # Auto-refresh database when instance is set
            self.refresh_database()
        else:
            print("WARNING: Vision instance set to None")

    def refresh_database(self):
        """Refresh database using stored vision instance"""
        if self.vi is not None and hasattr(self.vi, 'cross_validation'):
            try:
                # CRITICAL: Initialize/refresh images from disk first!
                self.vi.cross_validation.init_images()
                
                # Now get the updated list
                images = self.vi.cross_validation.get_images_names()
                self.set_crossval_images(images)
                
                print(f"✓ Database refreshed: {len(images)} images found")
            except Exception as e:
                print(f"✗ ERROR: Failed to refresh database: {e}")
        else:
            print("⚠ WARNING: Cannot refresh - vision instance not available")

    def set_crossval_images(self, images_list=None):
        """
        Set the cross validation images
        Accepts optional list for backward compatibility
        """   
        # Use provided list or get from vision instance
        if images_list is None:
            if self.vi is not None and hasattr(self.vi, 'cross_validation'):
                images_list = self.vi.cross_validation.get_images_names()
            else:
                print("✗ ERROR: No images list provided and no vision instance")
                return
        
        self.cross_val_images_widget.clear()
        if images_list:
            for _image in images_list:
                _item = QListWidgetItem(_image)
                self.cross_val_images_widget.addItem(_item)
            print(f"✓ Displaying {len(images_list)} images")
        else:
            _item = QListWidgetItem("No images found")
            self.cross_val_images_widget.addItem(_item)
            print("ℹ INFO: No images found in database")

    def set_vision_ok_for_image(self, image_name:str, ok:bool):
        _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
        if len(_item) > 0:
            _item[0].setBackground(QColor(0, 255, 0) if ok else QColor(255, 0, 0))

    def set_vision_ok_for_images(self, failed_image_names:list):
        # Set all images to green
        for i in range(self.cross_val_images_widget.count()):
            _item = self.cross_val_images_widget.item(i)
            _item.setBackground(QColor(0, 255, 0))

        for image_name in failed_image_names:
            _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
            if len(_item) > 0:
                _item[0].setBackground(QColor(255, 0, 0))
            else:
                print(f"⚠ Image {image_name} not found in list")

    def open_process_file(self, file_path: str):
        """Open a process file in the vision builder widget."""
        if hasattr(self, 'vision_builder_widget') and self.vision_builder_widget:
            return self.vision_builder_widget.open_process_file(file_path)
        return False

    def set_metadata(self, key: str, value: str):
        """Set metadata field value (for compatibility with refactored code)."""
        # Map to actual widgets
        metadata_map = {
            'process_uid': self.process_uid_widget,
            'mode': self.mode_widget,
            'camera_name': self.camera_name_widget,
            'image_name': self.image_name_widget,
            'crossval_info': self.crossval_info_widget
        }
        
        if key in metadata_map and metadata_map[key] is not None:
            metadata_map[key].setText(str(value))