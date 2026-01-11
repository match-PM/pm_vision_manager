import sys
from PyQt6.QtGui import QCloseEvent, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTabWidget, QLabel, QGridLayout, QTabBar
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot, QThread, QTimer
import numpy as np
from functools import partial
from rclpy.node import Node
from pm_vision_manager.va_py_modules.vision_app_modules.ImageDisplayWidget import ImageDisplayWidget
from pm_vision_manager.va_py_modules.vision_app_modules.MainMenuWidget import MainMenuWidget
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass


class VisionAssistantWindow(QMainWindow):
    def __init__(self, ros_node:Node):
        super().__init__()
        self.ros_node = ros_node
        self.setWindowTitle("Vision Assistant")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.ros_logger = self.ros_node.get_logger()
        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        self.layout.addWidget(self.tab_widget)
        self.start_execution_widget_signal = StartExecutionSignal()
        self.start_execution_widget_signal.signal.connect(self.start_vision_execution)
        
        self.start_vision_assistant_wiget_signal = StartVisionAssistantSignal()
        self.start_vision_assistant_wiget_signal.signal.connect(self.start_vision_assistant)

        # Create main tab
        self.main_widget = MainMenuWidget(self.ros_node)

        self.main_widget.start_assistant_button.clicked.connect(self.start_vision_assistant_button_click)
        self.tab_widget.addTab(self.main_widget, "Main")
        # Remove the close button from the main tab
        self.tab_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.thread_pool = QThreadPool()
        self.timer = QTimer()
        self.timer.timeout.connect(self.log_running_threads)
        self.timer.start(1000)

        desktop_widget = QGuiApplication.primaryScreen()
        screen_geometry = desktop_widget.availableGeometry()
        window_width = screen_geometry.width() // 2
        window_height = screen_geometry.height()
        
        self.setGeometry(0, 0, window_width, window_height)

    def log_running_threads(self):
        self.ros_logger.debug(f"Running threads: {self.thread_pool.activeThreadCount()}")

    def start_vision_assistant(self, camera_file:str = None, 
                               process_file:str = None):
        
        if camera_file is None or process_file is None:
            self.ros_logger.error("Camera or Process file not selected")
            return
        
        # create the class
        _new_vision_process = VisionProcessClass(self.ros_node, 
                                                 launch_as_assistant=True,
                                                 process_filename=process_file,
                                                 camera_config_filename=camera_file,
                                                 process_UID='test')
        
        # create the new image display widget
        new_image_display = ImageDisplayWidget(_new_vision_process.camera_subscription_topic)
        #new_image_display.process_filename_widget.setText(_process_file)
        
        #setup of the new image display widget
        new_image_display.camera_name_widget.setText(camera_file)
        new_image_display.vision_builder_widget.open_process_file(_new_vision_process.process_file_path)
        new_image_display.set_crossval_images(_new_vision_process.cross_validation.get_images_names())
        new_image_display.image_select_signal.signal.connect(_new_vision_process.set_processing_source)
        _new_vision_process.results_signal.signal.connect(new_image_display.set_image_result)
        new_image_display.exit_assistant_signal.signal.connect(_new_vision_process.close_vision_assistant)
        new_image_display.execute_cross_val_button.clicked.connect(partial(self.start_cross_val, _new_vision_process, new_image_display))
        _new_vision_process.set_crossval_results_signal.signal.connect(new_image_display.set_vision_ok_for_images)
        
        # connect the results signal to the image display widget

        tab_name=f"VA_{process_file.strip('.json')}_{camera_file.strip('.yaml')}"
        # add the new image display widget to the tab widget
        self.add_new_vision_tab(new_image_display, tab_name)
        
        # create a new worker for the vision assistant
        _new_instance_worker = VisionAssistantWorker(_new_vision_process)
        # start the worker in the thread pool
        self.thread_pool.start(_new_instance_worker)
        #self.thread_pool.start(self.cross_val_worker)
    
    def start_vision_assistant_button_click(self):
        _camera_file = self.main_widget.get_selected_camera()
        _process_file = self.main_widget.get_selected_process()

        self.start_vision_assistant(camera_file=_camera_file,
                                   process_file=_process_file)
        
        
    def start_cross_val(self, vision_instance:VisionProcessClass, image_display:ImageDisplayWidget):
        self.cross_val_worker = CrossValWorker(vision_instance, image_display)
        # Connect the refresh button on the GUI (main) thread so the
        # getter is executed when the user clicks the button.
        # Use a lambda to call the getter at click time (avoids binding
        # a stale snapshot and avoids connecting GUI from the worker thread).
        image_display.refresh_database_button.clicked.connect(
            lambda checked=False, vi=vision_instance, idisp=image_display: idisp.set_crossval_images(
                vi.cross_validation.get_images_names()
            )
        )

        self.thread_pool.start(self.cross_val_worker)

    def add_new_vision_tab(self, new_widget:ImageDisplayWidget, window_name:str):
        self.tab_widget.addTab(new_widget, window_name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)


    def start_vision_execution(self, vision_instance:VisionProcessClass, tab_timeout: int):
        
        new_image_display = ImageDisplayWidget(vision_instance.camera_subscription_topic)
        new_image_display.execute_cross_val_button.setDisabled(True)
        new_image_display.sub_topic_button.setDisabled(True)
        new_image_display.set_image_source(vision_instance.camera_subscription_topic)
        #new_image_display.process_filename_widget.setText(_process_file)
        new_image_display.camera_name_widget.setText(vision_instance.camera_config_filename)
        new_image_display.vision_builder_widget.open_process_file(vision_instance.process_file_path)
        vision_instance.results_signal.signal.connect(new_image_display.set_image_result)
        vision_instance.set_crossval_results_signal.signal.connect(new_image_display.set_vision_ok_for_images)
        new_image_display.set_crossval_images(vision_instance.cross_validation.get_images_names())
        #new_image_display.image_select_signal.signal.connect(_new_vision_process.set_processing_source)
        #new_image_display.exit_assistant_signal.signal.connect(new_image_display.exit_class)
        tab_name=f"VA_{vision_instance.process_UID}"
        self.add_new_vision_tab(new_image_display, tab_name)
        timer = QTimer()
        timer.singleShot(tab_timeout*1000, partial(self.close_vision_execution_widget, tab_name))

        # this is signal is only executed if the vision process emits; this only happens when initialized with run_cross_validation=True
        

        #if vision_instance.run_cross_validation:
        #    self.start_cross_val(vision_instance, new_image_display)

    def close_vision_execution_widget(self, tab_name:str):
        self.delete_tab_by_name(tab_name)

    def close_tab(self, index):
        _current_widget:ImageDisplayWidget = self.tab_widget.widget(index)
        _current_widget.exit_assistant_signal.signal.emit()
        _current_widget.deleteLater()
        self.tab_widget.removeTab(index)

    def delete_tab_by_name(self, window_name: str):
        # Find the index of the tab with the specified name
        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index) == window_name:
                # Remove the tab with the found index
                self.tab_widget.removeTab(index)
                return  # Stop searching after deleting the first occurrence
    
    # overwriting the closeEvent method to close all vision assistants
    def closeEvent(self, event: QCloseEvent) -> None:
        # Close all vision assistants
        # Index 0 is the main tab
        for index in range(1,self.tab_widget.count()):
            _current_widget:ImageDisplayWidget = self.tab_widget.widget(index)
            _current_widget.exit_assistant_signal.signal.emit()
        self.ros_logger.warn("Closing Vision Assistant")
        return event.accept()
    
class VisionAssistantWorker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''
    def __init__(self, vision_instance:VisionProcessClass):
        super(VisionAssistantWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.vision_instance = vision_instance

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        #self.vision_instance.vision_assistant_loop()
        self.vision_instance.start_vision_assistant()
    
class StartExecutionSignal(QObject):
    signal = pyqtSignal(VisionProcessClass, int)
    
class StartVisionAssistantSignal(QObject):
    signal = pyqtSignal(str, str)

class CrossValWorker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''
    def __init__(self, vision_instance:VisionProcessClass, image_display:ImageDisplayWidget):
        super(CrossValWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.vision_instance = vision_instance
        self.image_display = image_display

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.vision_instance.cross_validation.init_images()
        self.vision_instance.execute_crossvalidation()
        self.image_display.set_crossval_images(self.vision_instance.cross_validation.get_images_names())
        self.image_display.set_crossval_info(self.vision_instance.cross_validation.get_error_count(),
                                             self.vision_instance.cross_validation.get_total_number_images())
    # NOTE: do not connect GUI buttons from a worker thread — that is unsafe.
    # The connection for the refresh button is done on the main thread in
    # start_cross_val so the getter is called when the user clicks.
        
        self.image_display.set_vision_ok_for_images(self.vision_instance.cross_validation.get_failed_images())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisionAssistantWindow()
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec())
