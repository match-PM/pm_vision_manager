import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QFrame,
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
    QSpinBox,
    QFileDialog,
    QMenu,
)
import os
from ament_index_python.packages import get_package_share_directory
from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QPixmap, QCursor
from functools import partial
import yaml
from yaml.loader import SafeLoader
from PyQt6.QtCore import pyqtSignal, QTimer

try:
    from py_modules.vision_functions_loader import VisionFunctionsLoader
    from py_modules.vision_pipeline_class import VisionPipeline
    import py_modules.type_classes as TC
except:
    from pm_vision_app.py_modules.vision_functions_loader import VisionFunctionsLoader
    from pm_vision_app.py_modules.vision_pipeline_class import VisionPipeline
    import pm_vision_app.py_modules.type_classes as TC

N_INF_INT = -2147483647
INF_INT = 2147483647
N_INF_FLOAT = -1e20
INF_FLOAT = 1e20


class HoverInfoPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)  # Solid background
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)  # Don't steal focus
        # Remove transparent background attribute
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setObjectName("HoverInfoPanel")
        self.setStyleSheet("""
        QFrame#HoverInfoPanel {
            background-color: black;
            border: 2px solid #555;
            border-radius: 6px;
        }
        QLabel {
            color: white;
            font-size: 12px;
            background-color: transparent;
        }
        """)
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")

        self.desc_label = QLabel()
        self.desc_label.setWordWrap(True)
        self.desc_label.setMinimumWidth(280)
        self.desc_label.setMaximumWidth(300)
        self.desc_label.setStyleSheet("color: #e0e0e0;")

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._delayed_hide)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.desc_label)

    def _delayed_hide(self):
        super().hide()

    def hide(self):
        self.hide_timer.start(50)

    def show(self):
        self.hide_timer.stop()
        super().show()

    def update_content(self, title, description, image_path=None):
        # Clear previous pixmap to free memory
        self.image_label.clear()
        
        self.title_label.setText(title)
        self.desc_label.setText(description)
        
        if image_path and os.path.exists(image_path):
            pix = QPixmap(image_path)
            if not pix.isNull():
                pix = pix.scaled(280, 160,
                                 Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(pix)
                self.image_label.show()
            else:
                self.image_label.hide()
        else:
            self.image_label.hide()
        self.adjustSize()
    
    def hide(self):
        # Clear pixmap when hiding to free memory
        self.image_label.clear()
        self.hide_timer.start(50)


class VisionBuilderWidget(QWidget):
    def __init__(self, initial_pipeline_file: str = None):
        super().__init__()

        self.hover_panel = HoverInfoPanel()
        self.contextMenu = None
        self.hover_timer = QTimer()
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self._show_hover_panel)

        self.pending_action = None
        self.pending_menu = None
        self.captured_submenu_left = None
        self.function_parameter_widgets = []

        self.initializeAppPaths()
        self.current_vision_pipeline = VisionPipeline(self.functions_library_path)

        self.initUI()
        self.save_as = False
        self.print_available_functions()
        self.vision_library = self.current_vision_pipeline.vision_functions_library.return_vision_library()
        
        # Build function info with only essential data (no large objects)
        self.function_info = self._build_function_info_from_yaml()
        
        # Cache for currently visible menu to prevent multiple instances
        self.current_menu = None
        self.menu_connections = []  # Track connections for cleanup

        if initial_pipeline_file is not None:
            self.open_process_file(initial_pipeline_file)

    def initUI(self):
        # Create layout for the main container widget
        layout = QGridLayout()

        self.pipeline_name_widget = QLabel()
        self.set_widget_pipeline_name("Not saved yet!")
        layout.addWidget(self.pipeline_name_widget, 0, 0, 1, 2)

        open_action_menu_button = QPushButton('Add \n Action')
        open_action_menu_button.clicked.connect(self.show_vision_action_menu)
        layout.addWidget(open_action_menu_button, 1, 0)

        # Add combobox for vision pipeline building
        self.checkbox_list = ReorderableCheckBoxListWidget(delete_callback=self.delete_function_from_pipeline)
        self.checkbox_list.itemClicked.connect(self.create_function_parameters_layout)
        self.checkbox_list.itemChanged.connect(self.set_function_states)
        self.checkbox_list.CustDragSig.connect(self.on_drop)
        layout.addWidget(self.checkbox_list, 2, 0)

        # add textbox for string output
        self.text_output = AppTextOutput()
        layout.addWidget(self.text_output, 3, 0, 1, 2)

        # create sub layout for the function parameter widgets
        self.sub_layout = QVBoxLayout()
        # add a textlabel to the sublayout
        self.sub_layout.addWidget(QLabel("Function parameters:"))

        # add sublayout to app layout
        layout.addLayout(self.sub_layout, 2, 1, Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)
        self.setGeometry(100, 100, 600, 800)

    def _build_function_info_from_yaml(self):
        """Build minimal function info without storing large objects"""
        info = {}
        library_path = self.functions_library_path
        if not os.path.exists(library_path):
            return info

        for root, dirs, files in os.walk(library_path):
            for file in files:
                if file.endswith(('.yaml', '.yml')):
                    yaml_path = os.path.join(root, file)
                    try:
                        with open(yaml_path, 'r', encoding='utf-8') as f:
                            data = yaml.load(f, Loader=SafeLoader)
                            if data and 'function_name' in data:
                                name = data['function_name']
                                img_path = None
                                if 'image' in data and data['image']:
                                    candidate = data['image']
                                    if not os.path.isabs(candidate):
                                        candidate = os.path.join(os.path.dirname(yaml_path), candidate)
                                    if os.path.exists(candidate):
                                        img_path = candidate
                                # Store only what's needed - no large objects
                                info[name] = {
                                    'description': data.get('description', 'No description available.')[:500],  # Limit description length
                                    'image': img_path
                                }
                    except Exception as e:
                        self.text_output.append(f"Error reading {yaml_path}: {e}")

        # Fallback for functions without YAML
        loader = self.current_vision_pipeline.vision_functions_library
        for name in loader.names:
            if name not in info:
                obj = loader.return_by_name(name)
                desc = getattr(obj, 'description', 'No description available.')
                info[name] = {
                    'description': desc[:500] if desc else 'No description available.',
                    'image': getattr(obj, 'image', None)
                }
        return info

    def _cleanup_menu(self, menu):
        """Recursively clean up menu and all its actions"""
        if not menu:
            return
        
        # Clear all actions
        for action in menu.actions():
            # Disconnect all signals from this action
            action.triggered.disconnect() if action.triggered else None
            # If it's a submenu, clean it too
            if action.menu():
                self._cleanup_menu(action.menu())
        
        # Clear the menu
        menu.clear()

    def _on_menu_hide(self):
        """Clean up when menu hides"""
        self.hover_timer.stop()
        self.hover_panel.hide()
        self.pending_action = None
        self.captured_submenu_left = None   # Clear submenu reference

    def show_vision_action_menu(self):
        # Clean up previous menu if it exists
        if self.contextMenu:
            self._cleanup_menu(self.contextMenu)
            self.contextMenu.deleteLater()
            self.contextMenu = None
        
        self.contextMenu = QMenu(self)
        self.create_menu_from_data(self.contextMenu, self.vision_library)

        # Store connections for cleanup
        self.menu_connections.append(
            self.contextMenu.hovered.connect(self._on_menu_action_hovered)
        )
        self.menu_connections.append(
            self.contextMenu.aboutToHide.connect(self._on_menu_hide)
        )

        # Execute menu
        self.contextMenu.exec(QCursor.pos())

        # Clean up after menu closes
        self.hover_panel.hide()
        self.hover_timer.stop()
        
        if self.contextMenu:
            self._cleanup_menu(self.contextMenu)
            self.contextMenu.deleteLater()
            self.contextMenu = None
        
        # Clear pending references
        self.pending_action = None
        self.pending_menu = None
        self.captured_submenu_left = None

    def _on_menu_action_hovered(self, action):
        """Handle hover over a menu action - capture submenu edge when available"""
        if not action or not hasattr(action, 'text'):
            return
        
        # Check if we're still hovering the same action
        if self.pending_action == action:
            return
        
        # Hide panel when moving to a different item
        self.hover_panel.hide()
        
        self.pending_action = action
        
        # Try to get the category menu from the action
        category_menu = action.property("parent_category_menu")
        
        if category_menu and category_menu.isVisible():
            # Capture the submenu position
            submenu_global_pos = category_menu.mapToGlobal(category_menu.rect().topLeft())
            self.captured_submenu_left = submenu_global_pos.x()
        
        # ALWAYS use the main context menu
        self.pending_menu = self.contextMenu
        
        self.hover_timer.stop()
        self.hover_timer.start(200)

    def _show_hover_panel(self):
        """Show the hover panel only for function items (not categories)"""
        if not self.pending_action:
            return

        try:
            # Check if this is a category item (has a submenu)
            if self.pending_action.menu():
                # This is a category - don't show the info box
                return
            
            name = self.pending_action.text()
            
            # Get info from cache
            info = self.function_info.get(name, {})
            desc = info.get("description", "No description available.")
            image = info.get("image", None)

            # Update panel content
            self.hover_panel.update_content(title=name, description=desc, image_path=image)

            # Position the panel based on main menu
            main_menu = self.contextMenu
            x = 100
            y = 100
            
            if main_menu and not main_menu.isHidden():
                # Get main menu's global position
                main_menu_global_pos = main_menu.mapToGlobal(main_menu.rect().topLeft())
                main_menu_height = main_menu.height()
                main_menu_width = main_menu.width()
                
                # Try to get the category menu from the action
                category_menu = self.pending_action.property("parent_category_menu")
                
                if category_menu and category_menu.isVisible():
                    # Get the submenu's position
                    submenu_global_pos = category_menu.mapToGlobal(category_menu.rect().topLeft())
                    self.captured_submenu_left = submenu_global_pos.x()
                    
                    # Position to the LEFT of submenu
                    x = self.captured_submenu_left - self.hover_panel.width() - 15
                else:
                    # Use constant position based on main menu's right edge
                    x = main_menu_global_pos.x() + main_menu_width + 15
                
                # Position below the main menu
                y = main_menu_global_pos.y() + main_menu_height + 10
                
                # If panel would go off the bottom, place above instead
                if y + self.hover_panel.height() > self.screen().availableGeometry().bottom():
                    y = main_menu_global_pos.y() - self.hover_panel.height() - 10

            # Screen bounds checking
            screen_geom = self.screen().availableGeometry()
            
            if x < screen_geom.left():
                x = screen_geom.left() + 5
            if x + self.hover_panel.width() > screen_geom.right():
                x = screen_geom.right() - self.hover_panel.width() - 5
            if y + self.hover_panel.height() > screen_geom.bottom():
                y = screen_geom.bottom() - self.hover_panel.height() - 5
            if y < screen_geom.top():
                y = screen_geom.top() + 5

            # Position and show
            self.hover_panel.move(x, y)
            self.hover_panel.raise_()
            self.hover_panel.show()
            
        except Exception as e:
            self.hover_panel.hide()
            self.pending_action = None

    def create_menu_from_data(self, menu, menu_data):
        """Create menu structure with proper cleanup"""
        for menu_dict in menu_data:
            for menu_title, submenu_items in menu_dict.items():
                menu_cat = menu.addMenu(menu_title)
                
                # Store the category menu reference
                menu_cat.setProperty("category_name", menu_title)
                
                for submenu_item in submenu_items:
                    action = QAction(submenu_item, self)
                    action.setData(submenu_item)
                    # Store which category menu this action belongs to
                    action.setProperty("parent_category_menu", menu_cat)
                    action.triggered.connect(
                        partial(self.add_function_to_pipeline, submenu_item)
                    )
                    menu_cat.addAction(action)

    def _capture_submenu_position(self, submenu):
        """Capture submenu position when it's about to show"""
        if submenu and self.captured_submenu_left is None:
            # Use a single-shot timer to capture after it's fully shown
            QTimer.singleShot(50, lambda: self._capture_submenu_geometry(submenu))

    def _capture_submenu_geometry(self, submenu):
        """Actually capture the submenu geometry"""
        if submenu and submenu.isVisible() and self.captured_submenu_left is None:
            submenu_global_pos = submenu.mapToGlobal(submenu.rect().topLeft())
            self.captured_submenu_left = submenu_global_pos.x()

    def set_widget_pipeline_name(self, text):
        self.pipeline_name_widget.setText("Process name: " + text)

    def open_process_file(self, file_path_load=None):
        if self.current_vision_pipeline.vision_pipeline_json_dir is None:
            self.current_vision_pipeline.vision_pipeline_json_dir = self.default_process_library_path

        if not file_path_load:
            file_filter = "JSON Files (*.json);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open JSON File",
                self.current_vision_pipeline.vision_pipeline_json_dir,
                file_filter,
            )
        else:
            file_path = file_path_load

        if file_path:
            self.current_vision_pipeline.vision_pipeline_json_dir = os.path.dirname(file_path)
            self.text_output.append(f"Opening: {file_path}")
            success = self.current_vision_pipeline.set_vision_pipeline_from_process_json(file_path)
            if success:
                self.set_vision_ui_from_pipeline()
                self.set_widget_pipeline_name(self.current_vision_pipeline.process_name)
            else:
                self.text_output.append("Error Opening File!")

    def save_process_as(self):
        self.save_as = True
        self.create_new_file()

    def print_available_functions(self):
        for fun in self.current_vision_pipeline.vision_functions_library.init_output:
            self.text_output.append(str(fun))

    def set_function_states(self):
        for index in range(self.checkbox_list.count()):
            w_item = self.checkbox_list.item(index)
            check_state = w_item.checkState()
            if check_state == Qt.CheckState.Checked:
                self.current_vision_pipeline.vision_functions[index].set_function_check_state(True)
            elif check_state == Qt.CheckState.Unchecked:
                self.current_vision_pipeline.vision_functions[index].set_function_check_state(False)
        self.current_vision_pipeline.process_to_JSON()

    def create_new_file(self):
        try:
            if self.current_vision_pipeline.vision_pipeline_json_dir is None:
                self.current_vision_pipeline.vision_pipeline_json_dir = self.default_process_library_path

            file_filter = "JSON Files (*.json)"
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save JSON File",
                self.current_vision_pipeline.vision_pipeline_json_dir,
                file_filter,
            )
            if not file_name:
                return

            file_name = os.path.splitext(file_name)[0]
            self.current_vision_pipeline.vision_pipeline_json_dir = os.path.dirname(file_name)

            if not self.save_as and self.current_vision_pipeline.process_name is not None:
                self.current_vision_pipeline.vision_functions.clear()

            self.current_vision_pipeline.process_name = os.path.basename(file_name)
            with open(file_name + ".json", "w") as file:
                file.write("")
            self.current_vision_pipeline.process_to_JSON()
            self.set_vision_ui_from_pipeline()
            self.set_widget_pipeline_name(self.current_vision_pipeline.process_name)
            self.save_as = False

        except Exception as e:
            self.text_output.append("Error while saving file!")
            self.text_output.append(str(e))

    def add_function_to_pipeline(self, function_name: str):
        if function_name and self.current_vision_pipeline.vision_functions_library.return_by_name(function_name):
            self.current_vision_pipeline.append_vision_funciton_by_name(function_name)
            self.set_vision_ui_from_pipeline()
            self.text_output.append(f"Inserted function: {function_name}")
            self.current_vision_pipeline.process_to_JSON()
        else:
            self.text_output.append(f"ERROR: Function {function_name} not found!")

    def set_vision_ui_from_pipeline(self):
        self.checkbox_list.clear()
        for function in self.current_vision_pipeline.vision_functions:
            item = ReorderableCheckBoxListItem(function.vision_function_name)
            item.setCheckState(Qt.CheckState.Checked if function.get_function_check_state() else Qt.CheckState.Unchecked)
            self.checkbox_list.addItem(item)

    def delete_function_from_pipeline(self):
        selected = self.checkbox_list.currentItem()
        idx = self.checkbox_list.currentRow()
        if selected:
            self.current_vision_pipeline.remove_function_by_index(idx)
            self.checkbox_list.takeItem(idx)
            self.text_output.append(f"Deleted function: {selected.text()}")
            self.current_vision_pipeline.process_to_JSON()
        else:
            self.text_output.append("No function selected to delete")

    def create_function_parameters_layout(self):
        self.remove_all_function_parameter_widgets_from_layout()
        selected_item = self.checkbox_list.currentItem()
        if not selected_item:
            return
        idx = self.checkbox_list.currentRow()
        function = self.current_vision_pipeline.return_function_by_index(idx)
        if not function:
            return

        # Bool params
        for param in function.bool_params_list:
            if param.param_name != "active":
                cb = QCheckBox(param.param_name)
                cb.setToolTip(param.description)
                cb.setChecked(param.get_value())
                cb.stateChanged.connect(partial(self.bool_checkbox_cbk, cb, param))
                self.function_parameter_widgets.append(cb)

        # String params
        for param in function.string_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            le = QLineEdit()
            le.setToolTip(param.description)
            le.setText(param.get_value())
            le.textChanged.connect(partial(self.stringBox_cbk, le, param))
            self.function_parameter_widgets.append(le)

        # Int params
        for param in function.int_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            sb = QSpinBox()
            sb.setToolTip(param.description)
            sb.setMinimum(N_INF_INT)
            sb.setMaximum(INF_INT)
            if isinstance(param.min_val, int):
                sb.setMinimum(param.min_val)
            if isinstance(param.max_val, int):
                sb.setMaximum(param.max_val)
            sb.setValue(param.get_value())
            sb.valueChanged.connect(partial(self.intspinBox_cbk, sb, param))
            self.function_parameter_widgets.append(sb)

        # Float params
        for param in function.float_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            dsb = QDoubleSpinBox()
            dsb.setToolTip(param.description)
            dsb.setMinimum(N_INF_FLOAT)
            dsb.setMaximum(INF_FLOAT)
            if isinstance(param.min_val, float):
                dsb.setMinimum(param.min_val)
            if isinstance(param.max_val, float):
                dsb.setMaximum(param.max_val)
            dsb.setSingleStep(0.1)
            dsb.setDecimals(3)
            dsb.setValue(param.get_value())
            dsb.valueChanged.connect(partial(self.float_box_cbk, dsb, param))
            self.function_parameter_widgets.append(dsb)

        # Unsigned int params
        for param in function.unsigned_int_params_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            usb = QSpinBox()
            usb.setToolTip(param.description)
            usb.setMinimum(0)
            usb.setMaximum(INF_INT)
            if isinstance(param.min_val, int):
                usb.setMinimum(param.min_val)
            if isinstance(param.max_val, int):
                usb.setMaximum(param.max_val)
            usb.setValue(param.get_value())
            usb.valueChanged.connect(partial(self.unsigned_intspinBox_cbk, usb, param))
            self.function_parameter_widgets.append(usb)

        # Kernel params
        for param in function.kernel_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            ksb = QSpinBox()
            ksb.setToolTip(param.description)
            ksb.setMinimum(0)
            ksb.setMaximum(INF_INT)
            if isinstance(param.max_val, int):
                ksb.setMaximum(param.max_val)
            ksb.setValue(param.get_value())
            ksb.valueChanged.connect(partial(self.kernelspinBox_cbk, ksb, param))
            self.function_parameter_widgets.append(ksb)

        # List params (combo)
        for param in function.list_param_list:
            label = QLabel(param.param_name)
            self.function_parameter_widgets.append(label)
            combo = QComboBox()
            combo.setToolTip(param.description)
            combo.addItems(param.values)
            combo.setCurrentText(param.get_value())
            combo.activated.connect(partial(self.param_list_cbk, combo, param))
            self.function_parameter_widgets.append(combo)

        self.add_function_paramter_widgets_to_layout()

    def add_function_paramter_widgets_to_layout(self):
        for w in self.function_parameter_widgets:
            self.sub_layout.addWidget(w)

    def remove_all_function_parameter_widgets_from_layout(self):
        for w in self.function_parameter_widgets:
            self.sub_layout.removeWidget(w)
            w.deleteLater()
        self.function_parameter_widgets.clear()

    # Callbacks
    def kernelspinBox_cbk(self, widget, param):
        val = widget.value()
        if val % 2 == 0:
            val += 1
            widget.setValue(val)
        param.set_value(val)
        self.current_vision_pipeline.process_to_JSON()

    def bool_checkbox_cbk(self, widget, param):
        param.set_value(widget.isChecked())
        self.current_vision_pipeline.process_to_JSON()

    def float_box_cbk(self, widget, param):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()

    def intspinBox_cbk(self, widget, param):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()

    def stringBox_cbk(self, widget, param):
        param.set_value(widget.text())
        self.current_vision_pipeline.process_to_JSON()

    def unsigned_intspinBox_cbk(self, widget, param):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()

    def param_list_cbk(self, widget, param):
        param.set_value(widget.currentText())
        self.current_vision_pipeline.process_to_JSON()

    def on_drop(self):
        self.current_vision_pipeline.move_function_to_indice(
            old_index=self.checkbox_list.drag_source_position,
            new_index=self.checkbox_list.currentRow(),
        )
        self.create_function_parameters_layout()
        self.set_vision_ui_from_pipeline()
        self.current_vision_pipeline.process_to_JSON()

    def initializeAppPaths(self):
        try:
            share = get_package_share_directory("pm_vision_manager")
            config_path = os.path.join(share, "vision_assistant_path_config.yaml")
            with open(config_path, 'r') as f:
                data = yaml.load(f, Loader=SafeLoader)
                cfg = data["vision_assistant_path_config"]
                self.functions_library_path = cfg["function_library_path"]
                self.default_process_library_path = cfg["process_library_path"]
        except Exception as e:
            self.text_output.append(f"Error loading paths: {e}")
            self.functions_library_path = "./functions"
            self.default_process_library_path = "./processes"


class AppTextOutput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)


class ReorderableCheckBoxListWidget(QListWidget):
    CustDragSig = pyqtSignal()

    def __init__(self, delete_callback=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.delete_callback = delete_callback
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        if menu.exec(self.mapToGlobal(pos)) == delete_action and self.delete_callback:
            self.delete_callback()

    def dropEvent(self, event):
        self.drag_source_position = self.currentRow()
        super().dropEvent(event)
        event.accept()
        self.CustDragSig.emit()

    def dragEnterEvent(self, event):
        self.drag_source_position = self.currentRow()
        super().dragEnterEvent(event)


class ReorderableCheckBoxListItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)


if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"   # Avoid Wayland crashes

    pipeline_file = None
    for arg in sys.argv:
        if arg.startswith("pipeline_file_path:"):
            pipeline_file = arg.split(":", 1)[1]
    app = QApplication(sys.argv)
    window = VisionBuilderWidget(initial_pipeline_file=pipeline_file)
    window.show()
    sys.exit(app.exec())