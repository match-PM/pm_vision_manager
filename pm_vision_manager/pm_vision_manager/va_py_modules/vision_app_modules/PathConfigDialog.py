import os
from PyQt6.QtWidgets import (QDialog, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFileDialog, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt

from pm_vision_manager.va_py_modules.manager_configuration import (get_path_config,
                                                                   path_exists_with_timeout,
                                                                   set_process_library_path,
                                                                   set_camera_config_path,
                                                                   set_vision_database_path)


class PathConfigDialog(QDialog):
    """
    Dialog to view and change the folders used by the vision manager.
    """

    # config key -> (display name, setter)
    PATH_ENTRIES = {
        "process_library_path": ("Process Library", set_process_library_path),
        "camera_config_path": ("Camera Config", set_camera_config_path),
        "vision_database_path": ("Vision Database", set_vision_database_path),
    }

    def __init__(self, logger=None, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.line_edits = {}
        self.status_labels = {}

        self.setWindowTitle("Vision Manager - Paths")
        self.setMinimumWidth(800)

        config = get_path_config(self.logger)

        grid = QGridLayout()
        for row, (key, (name, _)) in enumerate(self.PATH_ENTRIES.items()):
            line_edit = QLineEdit(config.get(key, ""))
            line_edit.editingFinished.connect(lambda k=key: self._update_status(k))

            browse_button = QPushButton("Browse...")
            browse_button.clicked.connect(lambda _, k=key: self._browse(k))

            status_label = QLabel()
            status_label.setMinimumWidth(110)

            grid.addWidget(QLabel(f"{name}:"), row, 0)
            grid.addWidget(line_edit, row, 1)
            grid.addWidget(browse_button, row, 2)
            grid.addWidget(status_label, row, 3)

            self.line_edits[key] = line_edit
            self.status_labels[key] = status_label

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self._save)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(grid)
        layout.addWidget(button_box)

        for key in self.PATH_ENTRIES:
            self._update_status(key)

    def _browse(self, key: str):
        name, _ = self.PATH_ENTRIES[key]
        current_path = self.line_edits[key].text()
        # Start in the current folder only if it is reachable, otherwise the dialog may block
        start_dir = current_path if path_exists_with_timeout(current_path) else os.path.expanduser("~")

        folder_path = QFileDialog.getExistingDirectory(self, f"Select Folder for the {name}", start_dir)
        if folder_path != "":
            self.line_edits[key].setText(folder_path + "/")
            self._update_status(key)

    def _update_status(self, key: str) -> bool:
        path = self.line_edits[key].text()
        reachable = path_exists_with_timeout(path)
        label = self.status_labels[key]
        if reachable:
            label.setText("✔ available")
            label.setStyleSheet("color: green;")
        else:
            label.setText("✘ not available")
            label.setStyleSheet("color: red;")
        return reachable

    def _save(self):
        unavailable = [self.PATH_ENTRIES[key][0] for key in self.PATH_ENTRIES if not self._update_status(key)]
        if unavailable:
            answer = QMessageBox.warning(
                self,
                "Vision Manager - Path not available",
                f"The following folders are not available:\n\n{chr(10).join(unavailable)}\n\nSave anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        for key, (_, setter) in self.PATH_ENTRIES.items():
            path = self.line_edits[key].text().strip()
            if path and not path.endswith("/"):
                path += "/"
            setter(path, self.logger)

        self.accept()
