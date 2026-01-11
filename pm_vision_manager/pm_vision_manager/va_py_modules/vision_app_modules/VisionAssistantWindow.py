import sys
from functools import partial
from typing import Optional

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QTabWidget, QTabBar)
from PyQt6.QtGui import QCloseEvent, QGuiApplication
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot, QTimer

import numpy as np
from rclpy.node import Node

from pm_vision_manager.va_py_modules.vision_app_modules.ImageDisplayWidget import ImageDisplayWidget
from pm_vision_manager.va_py_modules.vision_app_modules.MainMenuWidget import MainMenuWidget
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass

# ============================================================================
# SIGNAL CLASSES
# ============================================================================

class StartExecutionSignal(QObject):
    """Signal to start vision execution."""
    signal = pyqtSignal(VisionProcessClass, int)

class StartVisionAssistantSignal(QObject):
    """Signal to start vision assistant."""
    signal = pyqtSignal(str, str)

# ============================================================================
# WORKER CLASSES
# ============================================================================

class VisionAssistantWorker(QRunnable):
    """Worker thread for running vision assistant."""
    
    def __init__(self, vision_instance: VisionProcessClass):
        super().__init__()
        self.vision_instance = vision_instance
    
    @pyqtSlot()
    def run(self):
        """Start the vision assistant."""
        self.vision_instance.start_vision_assistant()

class CrossValWorker(QRunnable):
    """Worker thread for running cross-validation."""
    
    def __init__(self, vision_instance: VisionProcessClass, image_display: ImageDisplayWidget):
        super().__init__()
        self.vision_instance = vision_instance
        self.image_display = image_display
    
    @pyqtSlot()
    def run(self):
        """Execute cross-validation and update display."""
        try:
            # Initialize and execute cross-validation
            self.vision_instance.cross_validation.init_images()
            self.vision_instance.execute_crossvalidation()
            
            # Update UI with results
            images = self.vision_instance.cross_validation.get_images_names()
            self.image_display._update_image_list(images)
            
            self.image_display.set_crossval_info(
                self.vision_instance.cross_validation.get_error_count(),
                self.vision_instance.cross_validation.get_total_number_images()
            )
            
            self.image_display.set_vision_ok_for_images(
                self.vision_instance.cross_validation.get_failed_images()
            )
            
        except Exception as e:
            print(f"✗ Cross-validation failed: {e}")

# ============================================================================
# MAIN WINDOW CLASS
# ============================================================================

class VisionAssistantWindow(QMainWindow):
    """
    Main application window for Vision Assistant.
    
    Features:
    - Tabbed interface for multiple vision processes
    - Thread pool for concurrent operations
    - Integration with ROS 2 node
    """
    
    def __init__(self, ros_node: Node):
        super().__init__()
        self.ros_node = ros_node
        self.ros_logger = ros_node.get_logger()
        
        self._init_ui()
        self._init_workers()
        self._init_signals()
        self._init_connections()
        
        self._setup_window_geometry()
    
    # ============================================================================
    # INITIALIZATION METHODS
    # ============================================================================
    
    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Vision Assistant")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.main_layout.addWidget(self.tab_widget)
        
        # Main menu tab
        self.main_menu = MainMenuWidget(self.ros_node)
        self._add_tab(self.main_menu, "Main", closable=False)
    
    def _init_workers(self):
        """Initialize worker thread pool."""
        self.thread_pool = QThreadPool()
        self._start_thread_monitor()
    
    def _init_signals(self):
        """Initialize signal objects."""
        self.start_execution_signal = StartExecutionSignal()
        self.start_assistant_signal = StartVisionAssistantSignal()
    
    def _init_connections(self):
        """Connect signals and slots."""
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        self.main_menu.start_assistant_button.clicked.connect(self._start_assistant_from_menu)
        
        self.start_execution_signal.signal.connect(self.start_vision_execution)
        self.start_assistant_signal.signal.connect(self.start_vision_assistant)
    
    def _setup_window_geometry(self):
        """Set window size and position."""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, screen.width() // 2, screen.height())
    
    # ============================================================================
    # TAB MANAGEMENT
    # ============================================================================
    
    def _add_tab(self, widget: QWidget, title: str, closable: bool = True):
        """Add a new tab to the tab widget."""
        index = self.tab_widget.addTab(widget, title)
        if not closable:
            self.tab_widget.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)
        self.tab_widget.setCurrentIndex(index)
        return index
    
    def _close_tab(self, index: int):
        """Close a tab at the specified index."""
        widget = self.tab_widget.widget(index)
        if widget:
            # Emit exit signal if widget supports it
            if hasattr(widget, 'exit_assistant_signal'):
                widget.exit_assistant_signal.signal.emit()
            widget.deleteLater()
        self.tab_widget.removeTab(index)
    
    def _close_tab_by_name(self, title: str):
        """Close tab by its title."""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                self._close_tab(i)
                return
    
    # ============================================================================
    # VISION ASSISTANT MANAGEMENT
    # ============================================================================
    
    def start_vision_assistant(self, camera_file: Optional[str] = None, 
                            process_file: Optional[str] = None):
        """Start a new vision assistant instance."""
        if not camera_file or not process_file:
            self.ros_logger.error("Camera or Process file not selected")
            return
        
        try:
            # Create vision process
            vision_process = self._create_vision_process(
                process_file, camera_file, is_assistant=True
            )
            
            # Create display widget
            display_widget = self._create_display_widget(vision_process)
            
            # Connect signals
            self._connect_vision_signals(vision_process, display_widget)
            
            # Open process file in builder (FIXED: Use direct access)
            if hasattr(display_widget, 'vision_builder_widget'):
                display_widget.vision_builder_widget.open_process_file(vision_process.process_file_path)
            
            # Add to tabs
            tab_title = self._generate_tab_title(process_file, camera_file)
            self._add_tab(display_widget, tab_title)
            
            # Start worker thread
            self._start_vision_worker(vision_process)
            
        except Exception as e:
            self.ros_logger.error(f"Failed to start vision assistant: {e}")

    def start_vision_execution(self, vision_instance: VisionProcessClass, tab_timeout: int):
        """Start vision execution with timeout."""
        try:
            # Create display widget
            display_widget = self._create_display_widget(vision_instance)
            
            # Configure for execution mode
            display_widget.execute_cross_val_button.setEnabled(False)
            display_widget.sub_topic_button.setEnabled(False)
            
            # FIXED: Direct widget access instead of set_metadata()
            if hasattr(display_widget, 'image_name_widget'):
                display_widget.image_name_widget.setText(vision_instance.camera_subscription_topic)
            if hasattr(display_widget, 'camera_name_widget'):
                display_widget.camera_name_widget.setText(vision_instance.camera_config_filename)
            
            # Open process file in builder (ONCE, not twice)
            if hasattr(display_widget, 'vision_builder_widget'):
                display_widget.vision_builder_widget.open_process_file(vision_instance.process_file_path)
            
            # Connect results signal
            vision_instance.results_signal.signal.connect(display_widget.set_image_result)
            vision_instance.set_crossval_results_signal.signal.connect(display_widget.set_vision_ok_for_images)
            
            # Add to tabs
            tab_title = f"Exec_{vision_instance.process_UID}"
            self._add_tab(display_widget, tab_title)
            
            # Set auto-close timer
            QTimer.singleShot(tab_timeout * 1000, 
                            lambda: self._close_tab_by_name(tab_title))
            
        except Exception as e:
            self.ros_logger.error(f"Failed to start vision execution: {e}")
        
    def start_cross_validation(self, vision_instance: VisionProcessClass, 
                              image_display: ImageDisplayWidget):
        """Start cross-validation for a vision instance."""
        worker = CrossValWorker(vision_instance, image_display)
        self.thread_pool.start(worker)
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    def _create_vision_process(self, process_file: str, camera_file: str, 
                              is_assistant: bool = True) -> VisionProcessClass:
        """Create a VisionProcessClass instance."""
        return VisionProcessClass(
            self.ros_node,
            launch_as_assistant=is_assistant,
            process_filename=process_file,
            camera_config_filename=camera_file,
            process_UID='vision_assistant'
        )
    
    def _create_display_widget(self, vision_process: VisionProcessClass) -> ImageDisplayWidget:
        """Create an ImageDisplayWidget for a vision process."""
        return ImageDisplayWidget(
            vision_instance=vision_process,
            camera_topic=vision_process.camera_subscription_topic
        )
    
    def _connect_vision_signals(self, vision_process: VisionProcessClass, 
                               display_widget: ImageDisplayWidget):
        """Connect signals between vision process and display widget."""
        display_widget.image_select_signal.signal.connect(vision_process.set_processing_source)
        vision_process.results_signal.signal.connect(display_widget.set_image_result)
        display_widget.exit_assistant_signal.signal.connect(vision_process.close_vision_assistant)
        
        display_widget.execute_cross_val_button.clicked.connect(
            lambda: self.start_cross_validation(vision_process, display_widget)
        )
        
        vision_process.set_crossval_results_signal.signal.connect(
            display_widget.set_vision_ok_for_images
        )
    
    def _generate_tab_title(self, process_file: str, camera_file: str) -> str:
        """Generate a tab title from process and camera file names."""
        process_name = process_file.replace('.json', '')
        camera_name = camera_file.replace('.yaml', '')
        return f"VA_{process_name}_{camera_name}"
    
    def _start_vision_worker(self, vision_process: VisionProcessClass):
        """Start a worker thread for vision processing."""
        worker = VisionAssistantWorker(vision_process)
        self.thread_pool.start(worker)
    
    def _start_thread_monitor(self):
        """Start monitoring thread pool activity."""
        self.thread_monitor = QTimer()
        self.thread_monitor.timeout.connect(self._log_thread_count)
        self.thread_monitor.start(1000)
    
    def _log_thread_count(self):
        """Log current thread count for debugging."""
        self.ros_logger.debug(f"Active threads: {self.thread_pool.activeThreadCount()}")
    
    
    # ============================================================================
    # EVENT HANDLERS
    # ============================================================================
    
    def _start_assistant_from_menu(self):
        """Handle start assistant button click from main menu."""
        camera_file = self.main_menu.get_selected_camera()
        process_file = self.main_menu.get_selected_process()
        self.start_vision_assistant(camera_file, process_file)
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event."""
        # Close all assistant tabs
        for i in range(1, self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if widget and hasattr(widget, 'exit_assistant_signal'):
                widget.exit_assistant_signal.signal.emit()
        
        self.ros_logger.info("Vision Assistant closing")
        event.accept()

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Note: ROS node should be created separately and passed to the window
    # For testing without ROS:
    # window = VisionAssistantWindow(None)
    
    window = VisionAssistantWindow(None)  # Replace None with actual ROS node
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()