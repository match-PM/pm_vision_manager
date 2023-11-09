import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QFrame, QMainWindow, QListWidget, QListWidgetItem, QDoubleSpinBox, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QComboBox, QTextEdit,QLabel,QSlider, QSpinBox, QFontDialog, QFileDialog
import os
from ament_index_python.packages import get_package_share_directory
from PyQt6 import QtCore
from py_modules.vision_functions_loader import VisionFunctionsLoader
from py_modules.vision_pipeline_class import VisionPipeline
import py_modules.type_classes as TC 
from PyQt6.QtGui import QAction
from functools import partial
import yaml
from yaml.loader import SafeLoader
from PyQt6.QtCore import pyqtSignal

class VisionAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.function_parameter_widgets = []    # tis is a list of widgets that represent all the parameter of a vision function; it is used to display widgets when a vision function is klicked
        
        self.initializeAppPaths()
        self.current_vision_pipeline=VisionPipeline(self.functions_library_path)

        self.initUI()
        self.save_as = False    # This is a helper bool used for saving files
        self.print_available_functions()

    def initUI(self):
        self.setWindowTitle("Vision Assistant App")
        
        # Create main container widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout for the main container widget
        #layout = QVBoxLayout()
        layout = QGridLayout()

        self.pipeline_name_widget = QLabel()
        self.set_widget_pipeline_name('Not saved yet!')
        layout.addWidget(self.pipeline_name_widget,0,0,1,2)

        # Add vision functions combo box
        self.vision_functions_combo_box = QComboBox()
        self.vision_functions_combo_box.addItems(self.current_vision_pipeline.vison_functions_libary.names)
        self.vision_functions_combo_box.activated.connect(self.add_function_to_pipeline)  # Connect the activated signal to addItem
        layout.addWidget(self.vision_functions_combo_box,1,0)

        # Add combobox for vision pipline building
        self.checkbox_list = ReorderableCheckBoxListWidget()
        self.checkbox_list.itemClicked.connect(self.create_function_parameters_layout)
        self.checkbox_list.itemChanged.connect(self.set_function_states)
        self.checkbox_list.CustDragSig.connect(self.on_drop)
        layout.addWidget(self.checkbox_list,2,0)

        # add button for deleting selected vision function
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_function_from_pipeline)
        layout.addWidget(delete_button,3,0)

        # add textbox for string output
        self.text_output = AppTextOutput()
        layout.addWidget(self.text_output,4,0,1,2)

        # create sub layout for the function parameter widgetd
        self.sub_layout = QVBoxLayout()
        #add a textlabel to the sublayout
        self.sub_layout.addWidget(QLabel('Function parameters:'))
        
        # Create a menu bar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = QAction("Open process", self)
        open_action.triggered.connect(self.open_process_file)
        file_menu.addAction(open_action)

        # Create "New" action
        new_action = QAction("New process", self)
        new_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_action)

        # Create 'save as' action
        save_as_action = QAction("Save process as", self)
        save_as_action.triggered.connect(self.save_process_as)

        file_menu.addAction(save_as_action)
        # add sublayout to app layout
        layout.addLayout(self.sub_layout,2,1,Qt.AlignmentFlag.AlignTop)

        central_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 800)

    def set_widget_pipeline_name(self, text):
        self.pipeline_name_widget.setText("Process name: " + text)

    def testprint(self):
        print("YESSSs")

    def open_process_file(self):
        if self.current_vision_pipeline.vision_pipeline_json_dir == None:
            self.current_vision_pipeline.vision_pipeline_json_dir = self.default_process_libary_path
        
        file_filter = "JSON Files (*.json);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON File", 
                                                   self.current_vision_pipeline.vision_pipeline_json_dir, 
                                                   file_filter)
        self.current_vision_pipeline.vision_pipeline_json_dir = os.path.dirname(file_path)
        if file_path:
            self.text_output.append(f"Opening: {file_path}")
            success = self.current_vision_pipeline.set_vision_pipeline_from_process_json(file_path)
            # initialize the ui with the new pipeline
            if success:
                self.set_vision_ui_from_pipeline()
                self.set_widget_pipeline_name(self.current_vision_pipeline.process_name)
            else:
                self.text_output.append("Error Opening File!")

    def save_process_as(self):
        self.save_as = True
        self.create_new_file()

    def print_available_functions(self):
        for fun in self.current_vision_pipeline.vison_functions_libary.init_output:
            self.text_output.append(str(fun))

    def set_function_states(self):
        for index in range(self.checkbox_list.count()):
            w_item = self.checkbox_list.item(index)
            check_state = w_item.checkState()
            if check_state == Qt.CheckState.Checked:
                self.current_vision_pipeline.vision_functions[index].set_function_check_state(True)
            elif check_state == Qt.CheckState.Unchecked:
                self.current_vision_pipeline.vision_functions[index].set_function_check_state(False)
            else:
                print("Item is in an intermediate state (partially checked)")
        self.current_vision_pipeline.process_to_JSON()

    def create_new_file(self):
        try:
            if self.current_vision_pipeline.vision_pipeline_json_dir == None:
                self.current_vision_pipeline.vision_pipeline_json_dir = self.default_process_libary_path

            # Set the file filters to show only JSON files
            file_filter = "JSON Files (*.json)"
            file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", self.current_vision_pipeline.vision_pipeline_json_dir, file_filter)

            # this is for the case the user entered .json to his filename 
            file_name = os.path.splitext(file_name)[0]

            self.current_vision_pipeline.vision_pipeline_json_dir = os.path.dirname(file_name)

            if not self.save_as and self.current_vision_pipeline.process_name is not None:
                self.current_vision_pipeline.vision_functions.clear()

            if file_name:
                self.current_vision_pipeline.process_name = os.path.basename(os.path.splitext(file_name)[0])
                with open(file_name+'.json', "w") as file:
                    file.write("")
                self.current_vision_pipeline.process_to_JSON()
                self.set_vision_ui_from_pipeline()  # This is needed in case functions from the pipeline were deleted when cleared.
                self.set_widget_pipeline_name(self.current_vision_pipeline.process_name)

            self.save_as = False                
            
        except Exception as e:
            self.text_output.append("Error while opening file. Please report the bug!")
            self.text_output.append(e)
            
    def add_function_to_pipeline(self):
        selected_function = self.vision_functions_combo_box.currentText()

        if selected_function:
            if self.current_vision_pipeline.vison_functions_libary.return_by_name(selected_function):
                # Add function to the vision pipeline
                self.current_vision_pipeline.append_vision_funciton_by_name(selected_function)

                self.set_vision_ui_from_pipeline()
                # print
                self.text_output.append(f"Inserted function: {selected_function}")
                # Save JSON
                self.current_vision_pipeline.process_to_JSON()
                #self.text_output.append("Saving...")
            else:
                self.text_output.append("ERROR appending function to internal list!")

    def set_vision_ui_from_pipeline(self):
        self.checkbox_list.clear()
        for function in self.current_vision_pipeline.vision_functions:

            function_checkbox = ReorderableCheckBoxListItem(function.vision_function_name)
            function_checkbox.setCheckState(Qt.CheckState.Checked if function.get_function_check_state() else Qt.CheckState.Unchecked)
                    
            self.checkbox_list.addItem(function_checkbox)
            
    def delete_function_from_pipeline(self):
        selected_function = self.checkbox_list.currentItem()
        index_selected_function = self.checkbox_list.currentRow()
        if selected_function:
            function_name = selected_function.text()
            # Remove the function from the pipeline and the list
            self.current_vision_pipeline.remove_function_by_index(index_selected_function)
            self.checkbox_list.takeItem(index_selected_function)
            self.text_output.append(f"Deleted function: {function_name}")
            # Save JSON
            self.current_vision_pipeline.process_to_JSON()
        else:
            self.text_output.append("No function selected to delete")

    def create_function_parameters_layout(self):
        """
        This function (cbk function) iterates through the function parameter of a selected function from the checkbox_list. It is triggered when the user klicks on a function in the combox.
        This function basically creates a layout to interact with the values of all the parameters of a function.
        The widgets are connected to a clb function which sets the parameter in the internal vision_pipeline and then saves the pipeline to json.
        """
        selected_function = None
        self.remove_all_function_parameter_widgets_from_layout()
        
        selected_function_name = self.checkbox_list.currentItem()
        if selected_function_name is not None:

            function_position_in_pipeline = self.checkbox_list.currentIndex().row()
            selected_function = self.current_vision_pipeline.return_function_by_index(function_position_in_pipeline)

            if selected_function:
                # Add Bool Widgets
                for param in selected_function.bool_params_list:
                    if param.param_name != 'active':
                        bool_widget = QCheckBox(param.param_name)
                        bool_widget.setToolTip(param.description)
                        bool_widget.setChecked(param.get_value())
                        bool_widget.stateChanged.connect(partial(self.bool_checkbox_cbk, bool_widget, param))
                        self.function_parameter_widgets.append(bool_widget)

                for param in selected_function.string_list:
                    param_label = QLabel(param.param_name)
                    self.function_parameter_widgets.append(param_label)

                    string_input = QLineEdit()
                    string_input.setReadOnly = False
                    string_input.setToolTip(param.description)
                    string_input.setText(param.get_value())
                    string_input.textChanged.connect(partial(self.stringBox_cbk, string_input, param))
                    self.function_parameter_widgets.append(string_input)  

                # Add Int Widgets
                for param in selected_function.int_list:
                    param_label = QLabel(param.param_name)
                    self.function_parameter_widgets.append(param_label)

                    int_spin_box = QSpinBox()
                    int_spin_box.setToolTip(param.description)
                    if isinstance(param.max_val,int):
                        int_spin_box.setMinimum(param.min_val)

                    if isinstance(param.max_val,int):
                        int_spin_box.setMaximum(param.max_val)

                    int_spin_box.setValue(param.get_value())  # Set the initial value of the slider
                    int_spin_box.setReadOnly(False)  # Make the spin box non-editable
                    int_spin_box.setSingleStep(1)
                    int_spin_box.valueChanged.connect(partial(self.intspinBox_cbk, int_spin_box, param))
                    self.function_parameter_widgets.append(int_spin_box)
                    
                # Add Float Widgets
                for param in selected_function.float_list:
                    param_label = QLabel(param.param_name)
                    self.function_parameter_widgets.append(param_label)   
                    double_spinbox = QDoubleSpinBox()
                    double_spinbox.setToolTip(param.description)
                    if isinstance(param.max_val,float):
                        double_spinbox.setMaximum(param.max_val)

                    if isinstance(param.min_val,float):
                        double_spinbox.setMinimum(param.max_val) 

                    double_spinbox.setSingleStep(1.0)
                    double_spinbox.setDecimals(2)
                    double_spinbox.setValue(param.get_value())
                    
                    double_spinbox.valueChanged.connect(partial(self.float_box_cbk, double_spinbox, param))
                    self.function_parameter_widgets.append(double_spinbox)      

                # Add unsigned int Widgets
                for param in selected_function.unsigned_int_params_list:
                    param_label = QLabel(param.param_name)
                    param_label.setToolTip(param.description)
                    self.function_parameter_widgets.append(param_label)

                    unsigned_int_spin_box = QSpinBox()
                    unsigned_int_spin_box.setToolTip(param.description)
                    unsigned_int_spin_box.setMinimum(param.min_val)

                    if isinstance(param.max_val,int):
                        unsigned_int_spin_box.setMaximum(param.max_val)
                        
                    unsigned_int_spin_box.setValue(param.get_value())  # Set the initial value of the slider
                    unsigned_int_spin_box.setReadOnly(False)  # Make the spin box non-editable
                    unsigned_int_spin_box.setSingleStep(1)
                    unsigned_int_spin_box.valueChanged.connect(partial(self.unsigned_intspinBox_cbk, unsigned_int_spin_box, param))
                    self.function_parameter_widgets.append(unsigned_int_spin_box)

                # Add kernel int Widgets
                for param in selected_function.kernel_list:
                    param_label = QLabel(param.param_name)
                    self.function_parameter_widgets.append(param_label)

                    kernel_spin_box = QSpinBox()
                    kernel_spin_box.setToolTip(param.description)
                    kernel_spin_box.setMinimum(param.min_val)

                    if isinstance(param.max_val,float):
                        kernel_spin_box.setMaximum(param.max_val)
                        
                    kernel_spin_box.setValue(param.get_value())  # Set the initial value of the slider
                    kernel_spin_box.setReadOnly(False)  # Make the spin box non-editable
                    kernel_spin_box.setSingleStep(2)
                    kernel_spin_box.valueChanged.connect(partial(self.kernelspinBox_cbk, kernel_spin_box, param))
                    self.function_parameter_widgets.append(kernel_spin_box)

                # Add param list int Widgets
                for param in selected_function.list_param_list:
                    param_label = QLabel(param.param_name)
                    self.function_parameter_widgets.append(param_label)

                    list_param_box = QComboBox()
                    list_param_box.setToolTip(param.description)
                    list_param_box.addItems(param.values)
                    list_param_box.setCurrentText(param.get_value())
                    list_param_box.activated.connect(partial(self.param_list_cbk, list_param_box, param))
                    self.function_parameter_widgets.append(list_param_box)

                # Add all the created widgets from the widget list to the layout
                self.add_function_paramter_widgets_to_layout()
            else:
                print("Error creating functions parameter layout")

    def add_function_paramter_widgets_to_layout(self):
        for widget in self.function_parameter_widgets:
            self.sub_layout.addWidget(widget)

    def remove_all_function_parameter_widgets_from_layout(self):
        for widget in self.function_parameter_widgets:
            self.sub_layout.removeWidget(widget)
            widget.deleteLater()
        self.function_parameter_widgets.clear()

    def kernelspinBox_cbk(self, widget, param:TC.Kernel):
        value = widget.value()
        if value % 2 == 0:
            value = value + 1
            widget.setValue(value)
        param.set_value(value)
        self.current_vision_pipeline.process_to_JSON()

    def bool_checkbox_cbk(self, widget, param:TC.BoolParam):
        if widget.checkState() == Qt.CheckState.Checked:
            param.set_value(True)
            widget.setChecked(True)
        else:
            param.set_value(False)
            widget.setChecked(False)
        self.current_vision_pipeline.process_to_JSON()

    def float_box_cbk(self, widget, param: TC.ParamFloat):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()

    def intspinBox_cbk(self, widget, param:TC.ParamInt):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()
       
    def stringBox_cbk(self, widget, param:TC.StringParam):
        param.set_value(widget.text())
        self.current_vision_pipeline.process_to_JSON()

    def unsigned_intspinBox_cbk(self, widget, param:TC.UnsignedInt):
        param.set_value(widget.value())
        self.current_vision_pipeline.process_to_JSON()

    def param_list_cbk(self, widget, param:TC.ParamList):
        param.set_value(widget.currentText())
        self.current_vision_pipeline.process_to_JSON()

    def on_drop(self):
        #print(window.checkbox_list.get_widget_list_names())
        print(window.checkbox_list.drag_source_position)
        print(window.checkbox_list.currentRow())
        # print(window.checkbox_list.currentItem().text())
        self.current_vision_pipeline.swap_functions_by_indices(old_index=window.checkbox_list.drag_source_position,
                                                                 new_index=window.checkbox_list.currentRow())
        #window.current_vision_pipeline.sort_functions_accto_names_list(window.checkbox_list.get_widget_list_names())
        self.current_vision_pipeline.process_to_JSON()
    
    def initializeAppPaths(self):
      try:
        vision_manager_share_directory = get_package_share_directory('pm_vision_manager')
        vision_manager_path_config_path = vision_manager_share_directory + '/vision_assistant_path_config.yaml'
        f = open(vision_manager_path_config_path)
        FileData = yaml.load(f,Loader=SafeLoader)
        config=FileData["vision_assistant_path_config"]
        self.functions_library_path=config["function_libary_path"]
        self.default_process_libary_path = config["process_library_path"]
        f.close()
      except:
        print(f"Error opening {vision_manager_path_config_path}!")

class AppTextOutput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

class ReorderableCheckBoxListWidget(QListWidget):
    CustDragSig = QtCore.pyqtSignal()
    def __init__(self):
        super(ReorderableCheckBoxListWidget,self).__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)

    def get_widget_list_names(self):
        name_list=[]
        for index in range(self.count()):
            item = self.item(index)
            if item:
                name_list.append(item.text())
        return name_list
    
    def dropEvent(self, event):
        super(ReorderableCheckBoxListWidget,self).dropEvent(event)
        event.accept()
        self.CustDragSig.emit()

    def dragEnterEvent(self, event):
        self.drag_source_position = self.currentRow()  # Capture the source position
        super(ReorderableCheckBoxListWidget, self).dragEnterEvent(event)

class ReorderableCheckBoxListItem(QListWidgetItem):
    def __init__(self, function_name):
        super().__init__(function_name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VisionAssistantApp()
    window.show()
    sys.exit(app.exec())
