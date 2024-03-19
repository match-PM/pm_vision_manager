from PyQt6.QtWidgets import QTextEdit,QWidget,QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QApplication, QSizePolicy, QPushButton, QGridLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtGui import QColor, QTextCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QByteArray
from pm_vision_manager.va_py_modules.vision_utils import get_screen_resolution, image_resize
from PyQt6.QtCore import Qt, QByteArray, pyqtSignal, QObject
import cv2
import numpy as np
#from pm_vision_app.py_modules.vision_builder_widget import VisionAssistantApp
from pm_vision_app.py_modules.vision_builder_widget import VisionBuilderWidget

class ImageSelectSignal(QObject):
    signal = pyqtSignal(str)

class ExitAssistantSignal(QObject):
    signal = pyqtSignal()

class ImageDisplayWidget(QWidget):
    def __init__(self, camera_topic:str = None):
        super(ImageDisplayWidget, self).__init__()

        self.main_layout = QGridLayout()

        self.properties_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.camera_topic = camera_topic
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_topic_button = QPushButton("Subscribe to topic")
        
        self.sub_topic_button.clicked.connect(self.set_image_to_topic)
        
        self.execute_cross_val_button = QPushButton("Execute Crossvalidation")
        #self.textbox = QTextEdit()

        self.properties_layout = QVBoxLayout()
        self.init_metadata_widget()
        
        self.image_select_signal = ImageSelectSignal()
        self.exit_assistant_signal = ExitAssistantSignal()

        self.cross_val_images_widget = QListWidget()
        self.cross_val_images_widget.clicked.connect(self.cross_val_images_widget_clicked)

        self.screen_resolution = get_screen_resolution()
        self.screen_height = int(self.screen_resolution["height"].decode("UTF-8"))
        
        self.properties_layout.addWidget(self.execute_cross_val_button)
        self.properties_layout.addWidget(self.sub_topic_button)
        self.properties_layout.addWidget(self.cross_val_images_widget)
        #self.properties_layout.addWidget(self.textbox)

        self.main_layout.addWidget(self.image_label, 0, 0, 1, 1)
        self.main_layout.addLayout(self.properties_layout, 0, 1, 1, 1)
        self.add_builder_widget()
        self.setLayout(self.main_layout)

    def cross_val_images_widget_clicked(self):
        item = self.cross_val_images_widget.currentItem()
        if item is not None:
            self.image_select_signal.signal.emit(item.text())
            self.image_name_widget.setText(item.text())
    
    def add_builder_widget(self):
        self.vision_builder_widget = VisionBuilderWidget()
        self.main_layout.addWidget(self.vision_builder_widget, 0, 3, 1, 3)

    def set_image_to_topic(self):
        self.image_name_widget.setText(self.camera_topic)
        self.image_select_signal.signal.emit(self.camera_topic)

    def set_image(self, image:np.ndarray, screen_height = None):
        # Check if the image is empty
        if image is None:
            return
        
        height, width, channel = image.shape

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if screen_height is None:
            screen_height =self.screen_height

        image = image_resize(image,height=screen_height-400)

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
        #_process_filename_widget = QLabel("Process filename:")
        _camera_name_widget = QLabel("Camera name:")
        #_crossvalidation_only_widget = QLabel("Crossvalidation only:")
        _image_name_widget = QLabel("Image name:")
        _crossval_info_widget = QLabel("Images Crossvalidation:")

        self.process_uid_widget = QLabel()
        self.mode_widget = QLabel()
        #self.process_filename_widget = QLabel()
        self.camera_name_widget = QLabel()
        #self.crossvalidation_only_widget = QLabel()
        self.image_name_widget = QLabel()
        self.crossval_info_widget = QLabel()
        
        metadata_layout.addWidget(_process_uid_widget, 0, 0)
        metadata_layout.addWidget(self.process_uid_widget, 0, 1)
        metadata_layout.addWidget(_mode_widget, 1, 0)
        metadata_layout.addWidget(self.mode_widget, 1, 1)
        #metadata_layout.addWidget(_process_filename_widget, 2, 0)
        #metadata_layout.addWidget(self.process_filename_widget, 2, 1)
        metadata_layout.addWidget(_camera_name_widget, 2, 0)
        metadata_layout.addWidget(self.camera_name_widget, 2, 1)
        #metadata_layout.addWidget(_crossvalidation_only_widget, 3, 0)
        #metadata_layout.addWidget(self.crossvalidation_only_widget, 3, 1)
        metadata_layout.addWidget(_image_name_widget, 3, 0)
        metadata_layout.addWidget(self.image_name_widget, 3, 1)
        metadata_layout.addWidget(_crossval_info_widget, 4, 0)
        metadata_layout.addWidget(self.crossval_info_widget, 4, 1)

        self.properties_layout.addLayout(metadata_layout)

        self.result_dict_tree = QTreeWidget()
        # Set headers
        self.result_dict_tree.setHeaderLabels(["Key", "Value"])
        self.properties_layout.addWidget(self.result_dict_tree)

    def set_image_source(self, image_name:str):
        self.image_name_widget.setText(image_name)
    
    def set_crossval_info(self, current_image:int, total_images:int):
        self.crossval_info_widget.setText(f"{current_image}/{total_images}")

    
    def set_result_dict(self, result_dict:dict):
        """
        Set the result dictionary
        """
        self.result_dict_tree.clear()
        self.populate_tree(self.result_dict_tree, result_dict)
        

    def populate_tree(self, tree, dictionary, parent_item=None):
        for key, value in dictionary.items():
            item = QTreeWidgetItem(parent_item if parent_item else tree)
            item.setText(0, str(key))
            if isinstance(value, dict):
                self.populate_tree(tree, value, item)
            else:
                item.setText(1, str(value))

    def set_crossval_images(self, images:list):
        """
        Set the cross validation images
        """
        self.cross_val_images_widget.clear()
        for _image in images:
            _item = QListWidgetItem(_image)
            self.cross_val_images_widget.addItem(_item)

    def set_vision_ok_for_image(self, image_name:str, ok:bool):
        """
        Set the vision ok for image
        """
        _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
        if len(_item) > 0:
            _item[0].setBackground(QColor(0, 255, 0) if ok else QColor(255, 0, 0))

    def set_vision_ok_for_images(self, failed_image_names:list):
        """
        Set the vision ok for image
        """
        # Set all images to green
        for i in range(self.cross_val_images_widget.count()):
            _item = self.cross_val_images_widget.item(i)
            _item.setBackground(QColor(0, 255, 0))

        for image_name in failed_image_names:
            _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
            if len(_item) > 0:
                _item[0].setBackground(QColor(255, 0, 0))
            else:
                print(f"Image {image_name} not found in list")
    
        