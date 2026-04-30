from locale import normalize
import sys
from functools import partial
from typing import Optional
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QTabWidget, QTabBar, QLineEdit)
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QIcon, QPixmap
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot, QTimer, QDir, QSize
from ament_index_python.packages import get_package_share_directory
import numpy as np
from rclpy.node import Node



from pm_vision_manager.va_py_modules.vision_app_modules.ImageDisplayWidget import ImageDisplayWidget
from pm_vision_manager.va_py_modules.vision_app_modules.MainMenuWidget import MainMenuWidget, QInputDialog
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
        
        self.setWindowTitle("Vision Assistant")

        # ---- Central widget ----
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ---- Main layout ----
        self.main_layout = QVBoxLayout(central_widget)

        # ---- Tab widget ----
        self.tab_widget = QTabWidget()
        self.tab_widget.tabBar().tabBarDoubleClicked.connect(self._rename_tab)
        self.tab_widget.setTabsClosable(True)
        self.main_layout.addWidget(self.tab_widget)

        # ---- Main menu tab ----
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
        # Check for existing tabs with the same title
        existing_titles = [self.tab_widget.tabText(i) for i in range(self.tab_widget.count())]
        
        if title not in existing_titles:
            unique_title = title
        else:
            # Find the smallest available number
            numbers = []
            for existing in existing_titles:
                if existing.startswith(title + " "):
                    try:
                        num = int(existing.split()[-1])
                        numbers.append(num)
                    except ValueError:
                        pass
            
            counter = 2
            while counter in numbers:
                counter += 1
            unique_title = f"{title} {counter}"
        
        # Add tab with unique title
        index = self.tab_widget.addTab(widget, unique_title)
        
        tab_bar = self.tab_widget.tabBar()
        
        # Remove close button if tab is not closable
        if not closable:
            tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, None)
        
        # Set tooltip
        tab_bar.setTabToolTip(index, f"Double-click to rename\nCurrent: {unique_title}")
        
        self.tab_widget.setCurrentIndex(index)
        return index

    def _rename_tab(self, index: int):
        """Rename a tab via inline edit dialog."""
        # Validate index
        if index < 0 or index >= self.tab_widget.count():
            return
        
        current_title = self.tab_widget.tabText(index)
        
        # Show input dialog
        new_title, ok = QInputDialog.getText(
            self, 
            "Rename Tab", 
            "Enter new tab name:", 
            QLineEdit.EchoMode.Normal, 
            current_title
        )
        
        # Apply new name if valid
        if ok and new_title and new_title.strip():
            new_title = new_title.strip()
            self.tab_widget.setTabText(index, new_title)
            
            # Update tooltip with new name
            self.tab_widget.tabBar().setTabToolTip(index, f"Double-click to rename\nCurrent: {new_title}")
            
            # Optional: Emit signal that tab was renamed
            widget = self.tab_widget.widget(index)
            if hasattr(widget, 'tab_renamed_signal'):
                widget.tab_renamed_signal.emit(index, new_title)

    def _close_tab(self, index: int):
        """Close a tab at the specified index (connected to tabCloseRequested)."""
        # Validate index
        if index < 0 or index >= self.tab_widget.count():
            return
            
        widget = self.tab_widget.widget(index)
        if widget:
            # Emit exit signal if widget supports it (checking for proper signal)
            if hasattr(widget, 'exit_assistant_signal'):
                # Check if it's a Qt signal or a custom object
                if hasattr(widget.exit_assistant_signal, 'emit'):
                    widget.exit_assistant_signal.emit()
                elif hasattr(widget.exit_assistant_signal, 'signal'):
                    # If it's wrapped in a signal object
                    widget.exit_assistant_signal.signal.emit()
            widget.deleteLater()
        self.tab_widget.removeTab(index)

    def _close_tab_by_name(self, title: str):
        """Close tab by its title."""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                self._close_tab(i)
                return

    def _close_all_tabs(self):
        """Close all tabs (optional utility method)."""
        for i in range(self.tab_widget.count() - 1, -1, -1):
            self._close_tab(i)

    def _get_current_tab_title(self) -> str:
        """Get title of currently selected tab."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            return self.tab_widget.tabText(current_index)
        return ""

    def _get_tab_by_title(self, title: str) -> tuple:
        """Get index and widget of tab by title."""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                return i, self.tab_widget.widget(i)
        return -1, None
        
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
            tab_title = self.combine_labels(process_file, camera_file, 4) #int here for max words in title
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
    
    # def _generate_tab_title(self, process_file: str, camera_file: str) -> str:
    #     process_name = process_file.replace('.json', '')
    #     camera_name = camera_file.replace('.yaml', '')
    #     try:
    #         from abbreviate import abbreviate
    #         abbreviated_process = abbreviate(process_name, max_length=10)
    #         abbreviated_camera = abbreviate(camera_name, max_length=10)
    #         return f"VA_{abbreviated_process}_{abbreviated_camera}"
        
    #     except Exception as e:
    #         self.ros_logger.error(f"Failed to generate shortened tab title: {e}")
    #         return f"VA_{process_name}_{camera_name}"

    def combine_labels(self, name1: str, name2: str, max_words: int) -> str:
        # Combine two technical filenames into one clean UI label.
        def normalize_filename_tokens(name: str) -> list:
            """Internal: normalize a single filename into meaningful tokens."""
            redundant = {"ufc", "paper", "pm", "robot", "basler", "helper"}
            abbr = {"mes": "Meas", "cam": "Cam", "num": "Num"}
            generic = {"a", "an", "the", "of", "for", "with"}
                
            # Split and clean
            words = name.replace('_', ' ').split()
            words = [w for w in words if w.lower() not in redundant]
            words = [abbr.get(w.lower(), w) for w in words]
            words = [w for w in words if w.isdigit() or len(w) > 1 or w.lower() not in generic]
            return words

        def clean_name(name: str) -> str:
            import re
            # Remove file extension
            name = name.split('.')[0]
            # Remove parentheses and their contents
            name = re.sub(r'\([^)]*\)', '', name)
            return name.strip()
        
        tokens1 = clean_name(name1)
        tokens1 = normalize_filename_tokens(tokens1)
        tokens2 = clean_name(name2)
        tokens2 = normalize_filename_tokens(tokens2)
        # Combine tokens, avoiding duplicates
        combined = tokens1[:]
        for t in tokens2:
            if not any(t.lower() == existing.lower() for existing in combined):
                combined.append(t)

        # Keep numbers at the end if present
        numbers = [w for w in combined if w.isdigit()]
        words = [w for w in combined if not w.isdigit()]
        combined = (words + numbers)[-max_words:]
        
        # Capitalize and join
        final_title = ' '.join(w.capitalize() if not w.isdigit() else w for w in combined)
        return final_title




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