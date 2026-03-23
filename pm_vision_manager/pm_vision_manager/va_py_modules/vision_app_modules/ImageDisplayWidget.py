from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QGridLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtGui import QColor, QImage, QPixmap
from pm_vision_manager.va_py_modules.vision_utils import get_screen_resolution
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QRectF
import cv2
import numpy as np
from pm_vision_app.py_modules.vision_builder_widget import VisionBuilderWidget
from pm_vision_manager.va_py_modules.vision_assistant_class import VisionProcessClass
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from pm_vision_manager.va_py_modules.image_processing_handler import DisplayImages

class ImageSelectSignal(QObject):
    signal = pyqtSignal(str)

class ExitAssistantSignal(QObject):
    signal = pyqtSignal()


# ---------------------------------------------------------------------------
# Padding around the image in the scene (pixels at original image resolution).
# Allows panning so any edge or corner can be centered in the viewport.
# ---------------------------------------------------------------------------
_SCENE_PADDING = 1000


class ZoomableImageView(QGraphicsView):
    """
    Zoomable image view with two explicit modes:

    FIT MODE (default):
        - Active after first image, reset_for_new_image(), or double-click
        - Every new image via set_pixmap() with a different size resets and refits
        - Window resize refits the image (debounced 150ms)

    ZOOM MODE:
        - Active after mouse wheel scroll
        - Window resize does absolutely nothing
        - set_pixmap() updates content but never touches the transform

    Sync:
        - Call view_a.sync_with(view_b) to link two views
        - Whichever view is scrolled becomes master and pushes
          its transform + scroll position to the peer
        - Sync is bidirectional: no need to call sync_with on both

    The scene is padded by _SCENE_PADDING on all sides so that edges and
    corners of the image can be fully centered in the viewport when zoomed in.

    Tooltip overlay shows current mode, auto-hides after 2.5s.
    Double-click always returns to FIT MODE (on both views if synced).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Scene setup
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item = None
        self._last_image_size = None

        # Mode tracking
        self._fit_mode = True

        # Sync peer — set via sync_with()
        self._peer: "ZoomableImageView | None" = None
        self._syncing = False  # Guard against recursive sync calls

        # View configuration
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("background-color: #1e1e1e;")

        # Timer: debounce window resize — only fires when resizing stops
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(150)
        self._resize_timer.timeout.connect(self._fit)

        # Connect scrollbars to sync peer on change
        self.horizontalScrollBar().valueChanged.connect(self._on_scroll)
        self.verticalScrollBar().valueChanged.connect(self._on_scroll)

        # Overlay tooltip label
        self._tooltip = QLabel(self)
        self._tooltip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._tooltip.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: white;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
            }
        """)
        self._tooltip.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._tooltip.hide()

        # Timer: auto-hide tooltip after 2.5s
        self._tooltip_hide_timer = QTimer(self)
        self._tooltip_hide_timer.setSingleShot(True)
        self._tooltip_hide_timer.setInterval(2500)
        self._tooltip_hide_timer.timeout.connect(self._tooltip.hide)

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def sync_with(self, peer: "ZoomableImageView"):
        """
        Link this view with a peer. Whichever view is scrolled/zoomed
        becomes master and pushes its state to the other.
        Call once on either view — sets up both sides.
        """
        self._peer = peer
        peer._peer = self

    def _push_sync(self):
        """Push current transform and scroll position to peer."""
        if self._peer is None or self._syncing:
            return
        self._peer._syncing = True
        self._peer.setTransform(self.transform())
        self._peer.horizontalScrollBar().setValue(self.horizontalScrollBar().value())
        self._peer.verticalScrollBar().setValue(self.verticalScrollBar().value())
        self._peer._fit_mode = self._fit_mode
        self._peer._syncing = False

    def _on_scroll(self):
        """Called when scrollbars change — push to peer."""
        if not self._syncing:
            self._push_sync()

    # ------------------------------------------------------------------
    # Tooltip helpers
    # ------------------------------------------------------------------

    def _show_tooltip(self):
        if self._fit_mode:
            self._tooltip.setText("🔍 Scroll to zoom  |  FIT MODE")
        else:
            self._tooltip.setText("✅ Double-click to fit  |  ZOOM MODE")
        self._tooltip.adjustSize()
        self._position_tooltip()
        self._tooltip.show()
        self._tooltip.raise_()
        self._tooltip_hide_timer.stop()
        self._tooltip_hide_timer.start()

    def _position_tooltip(self):
        margin = 8
        self._tooltip.adjustSize()
        x = (self.width() - self._tooltip.width()) // 2
        y = self.height() - self._tooltip.height() - margin
        self._tooltip.move(x, y)

    # ------------------------------------------------------------------
    # Image loading
    # ------------------------------------------------------------------

    def set_pixmap(self, pixmap: QPixmap):
        """
        Update displayed image.
        - Size changed → always reset zoom and refit, regardless of current mode
        - Same size → update content only, transform untouched
        """
        new_size = (pixmap.width(), pixmap.height())
        size_changed = new_size != self._last_image_size

        self._scene.clear()
        self._pixmap_item = self._scene.addPixmap(pixmap)

        img_rect = self._pixmap_item.boundingRect()
        padded_rect = QRectF(
            img_rect.x() - _SCENE_PADDING,
            img_rect.y() - _SCENE_PADDING,
            img_rect.width() + 2 * _SCENE_PADDING,
            img_rect.height() + 2 * _SCENE_PADDING,
        )
        self._scene.setSceneRect(padded_rect)

        if size_changed:
            self._last_image_size = new_size
            self._fit_mode = True
            self.resetTransform()
            self._fit()
            QTimer.singleShot(50, self._fit)

    # ------------------------------------------------------------------
    # Core fit
    # ------------------------------------------------------------------

    def _fit(self):
        """Fit image into view. Never called directly from resizeEvent."""
        if self._pixmap_item and self._fit_mode:
            self.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset_for_new_image(self):
        """Call this whenever the user explicitly selects a new image."""
        self._fit_mode = True
        self._last_image_size = None  # Force refit on next set_pixmap
        if self._peer is not None:
            self._peer._fit_mode = True
            self._peer._last_image_size = None

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def wheelEvent(self, event):
        """Mouse wheel → ZOOM MODE. Syncs zoom to peer."""
        if event.angleDelta().y() == 0:
            return
        was_fit_mode = self._fit_mode
        self._fit_mode = False  # Must be set before scale()
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)
        self._push_sync()
        if was_fit_mode:
            self._show_tooltip()
        event.accept()

    def mouseDoubleClickEvent(self, event):
        """Double-click → FIT MODE on both views."""
        self._fit_mode = True
        self.resetTransform()
        QTimer.singleShot(50, self._fit)
        if self._peer is not None:
            self._peer._fit_mode = True
            self._peer.resetTransform()
            QTimer.singleShot(50, self._peer._fit)
        self._show_tooltip()
        super().mouseDoubleClickEvent(event)

    def resizeEvent(self, event):
        """Window resize: reposition tooltip, refit only if in FIT MODE (debounced)."""
        super().resizeEvent(event)
        self._position_tooltip()
        if self._fit_mode:
            self._resize_timer.start()


# ---------------------------------------------------------------------------
# ImageDisplayWidget
# ---------------------------------------------------------------------------

class ImageDisplayWidget(QWidget):
    def __init__(self, 
                 vision_instance: VisionProcessClass = None, 
                 camera_topic: str = None):
        super(ImageDisplayWidget, self).__init__()

        self.main_layout = QGridLayout()
        self.properties_layout = QVBoxLayout()

        self.logger = vision_instance.vision_node.get_logger()

        # --- Dual image views (original top, result bottom), synced ---
        self.image_label = ZoomableImageView()          # original / single image (top)
        self.image_result_label = ZoomableImageView()   # processed result (bottom)
        self.image_label.sync_with(self.image_result_label)

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

        # Image views stacked vertically in column 0
        self.main_layout.addWidget(self.image_label,        0, 0, 1, 1)
        self.main_layout.addWidget(self.image_result_label, 1, 0, 1, 1)
        self.main_layout.addLayout(self.properties_layout,  0, 1, 2, 1)  # spans both rows
        self.add_builder_widget()
        self.setLayout(self.main_layout)

        # Store references
        self.camera_topic = camera_topic
        self.vi = None

        if vision_instance is not None:
            self.set_vision_instance(vision_instance)

        self.refresh_database_button.clicked.connect(self.refresh_database)

    # ------------------------------------------------------------------

    def cross_val_images_widget_clicked(self):
        item = self.cross_val_images_widget.currentItem()
        if item is not None:
            self.image_label.reset_for_new_image()
            self.image_select_signal.signal.emit(item.text())
            self.image_name_widget.setText(item.text())

    def add_builder_widget(self):
        self.vision_builder_widget = VisionBuilderWidget()
        self.main_layout.addWidget(self.vision_builder_widget, 0, 3, 2, 3)  # spans both rows

    def set_image_to_topic(self):
        if self.camera_topic:
            self.image_name_widget.setText(self.camera_topic)
            self.image_select_signal.signal.emit(self.camera_topic)

    # ------------------------------------------------------------------
    # Image setters
    # ------------------------------------------------------------------

    @staticmethod
    def _to_pixmap(image: np.ndarray) -> QPixmap:
        """Convert BGR numpy array to QPixmap."""
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.tobytes(), width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_image)

    def set_image_result(self, display_images: DisplayImages, result_dict: dict, screen_height=None):
        if display_images.get_original_image() is None or display_images.get_final_image() is None:
            return
        self.image_label.set_pixmap(self._to_pixmap(display_images.get_original_image()))
        self.image_result_label.set_pixmap(self._to_pixmap(display_images.get_final_image()))
        self.set_result_dict(result_dict)

    # ------------------------------------------------------------------

    def init_metadata_widget(self):
        metadata_layout = QGridLayout()
        _process_uid_widget    = QLabel("Process UID:")
        _mode_widget           = QLabel("Mode:")
        _camera_name_widget    = QLabel("Camera name:")
        _image_name_widget     = QLabel("Image name:")
        _crossval_info_widget  = QLabel("Images Crossvalidation:")

        self.process_uid_widget   = QLabel()
        self.mode_widget          = QLabel()
        self.camera_name_widget   = QLabel()
        self.image_name_widget    = QLabel()
        self.crossval_info_widget = QLabel()

        metadata_layout.addWidget(_process_uid_widget,   0, 0)
        metadata_layout.addWidget(self.process_uid_widget,   0, 1)
        metadata_layout.addWidget(_mode_widget,          1, 0)
        metadata_layout.addWidget(self.mode_widget,          1, 1)
        metadata_layout.addWidget(_camera_name_widget,   2, 0)
        metadata_layout.addWidget(self.camera_name_widget,   2, 1)
        metadata_layout.addWidget(_image_name_widget,    3, 0)
        metadata_layout.addWidget(self.image_name_widget,    3, 1)
        metadata_layout.addWidget(_crossval_info_widget, 4, 0)
        metadata_layout.addWidget(self.crossval_info_widget, 4, 1)

        self.properties_layout.addLayout(metadata_layout)
        self.results_dict_tree = QTreeWidget()
        self.results_dict_tree.setHeaderLabels(["Vision results"])
        self.properties_layout.addWidget(self.results_dict_tree)

    def set_image_source(self, image_name: str):
        self.image_name_widget.setText(image_name)

    def set_crossval_info(self, current_image: int, total_images: int):
        self.crossval_info_widget.setText(f"{current_image}/{total_images}")

    def set_result_dict(self, result_dict: dict):
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
            QTreeWidgetItem(parent, [str(data)])

    def set_vision_instance(self, vision_instance: VisionProcessClass):
        self.vi = vision_instance
        if self.vi is not None:
            if hasattr(self.vi, 'camera_subscription_topic'):
                self.camera_topic = self.vi.camera_subscription_topic
                self.sub_topic_button.clicked.connect(self.set_image_to_topic)
            self.refresh_database()
        else:
            print("WARNING: Vision instance set to None")

    def refresh_database(self):
        if self.vi is not None and hasattr(self.vi, 'cross_validation'):
            try:
                self.vi.cross_validation.init_images()
                images = self.vi.cross_validation.get_images_names()
                self.set_crossval_images(images)
                print(f"✓ Database refreshed: {len(images)} images found")
            except Exception as e:
                print(f"✗ ERROR: Failed to refresh database: {e}")
        else:
            print("⚠ WARNING: Cannot refresh - vision instance not available")

    def set_crossval_images(self, images_list=None):
        if images_list is None:
            if self.vi is not None and hasattr(self.vi, 'cross_validation'):
                images_list = self.vi.cross_validation.get_images_names()
            else:
                print("✗ ERROR: No images list provided and no vision instance")
                return
        self.cross_val_images_widget.clear()
        if images_list:
            for _image in images_list:
                self.cross_val_images_widget.addItem(QListWidgetItem(_image))
            print(f"✓ Displaying {len(images_list)} images")
        else:
            self.cross_val_images_widget.addItem(QListWidgetItem("No images found"))
            print("ℹ INFO: No images found in database")

    def set_vision_ok_for_image(self, image_name: str, ok: bool):
        _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
        if _item:
            _item[0].setBackground(QColor(0, 255, 0) if ok else QColor(255, 0, 0))

    def set_vision_ok_for_images(self, failed_image_names: list):
        for i in range(self.cross_val_images_widget.count()):
            self.cross_val_images_widget.item(i).setBackground(QColor(0, 255, 0))
        for image_name in failed_image_names:
            _item = self.cross_val_images_widget.findItems(image_name, Qt.MatchFlag.MatchExactly)
            if _item:
                _item[0].setBackground(QColor(255, 0, 0))
            else:
                print(f"⚠ Image {image_name} not found in list")

    def open_process_file(self, file_path: str):
        if hasattr(self, 'vision_builder_widget') and self.vision_builder_widget:
            return self.vision_builder_widget.open_process_file(file_path)
        return False

    def set_metadata(self, key: str, value: str):
        metadata_map = {
            'process_uid': self.process_uid_widget,
            'mode':        self.mode_widget,
            'camera_name': self.camera_name_widget,
            'image_name':  self.image_name_widget,
            'crossval_info': self.crossval_info_widget,
        }
        if key in metadata_map and metadata_map[key] is not None:
            metadata_map[key].setText(str(value))