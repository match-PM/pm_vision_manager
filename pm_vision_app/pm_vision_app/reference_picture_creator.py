import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PyQt6.QtCore import QEvent, QPointF, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QDragEnterEvent, QDropEvent, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


SUPPORTED_IMAGE_EXTENSIONS = {".bmp", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}
SUPPORTED_METADATA_EXTENSIONS = {".json"}


@dataclass
class ReferenceExtractionSettings:
    source_path: str = ""
    rotation_angle_deg: float = 0.0
    roi_center_x: int = 0
    roi_center_y: int = 0
    roi_width_px: int = 128
    roi_height_px: int = 128
    keypoint_x_px: int = 64
    keypoint_y_px: int = 64
    circular_selection: bool = False


@dataclass
class ReferenceSaveResult:
    image_path: str
    metadata_path: str
    metadata: dict


class ReferenceImageExtractor:
    def __init__(self):
        self.source_path = ""
        self.source_image: np.ndarray | None = None
        self.rotated_image: np.ndarray | None = None

    def load_image(self, path: str) -> np.ndarray:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not read image: {path}")

        self.source_path = path
        self.source_image = image
        self.rotated_image = image.copy()
        return self.rotated_image

    def has_image(self) -> bool:
        return self.source_image is not None

    def rotate_source(self, angle_deg: float) -> np.ndarray:
        if self.source_image is None:
            raise ValueError("No source image loaded.")

        self.rotated_image = self.rotate_image_bound(self.source_image, angle_deg)
        return self.rotated_image

    @staticmethod
    def rotate_image_bound(image: np.ndarray, angle_deg: float) -> np.ndarray:
        if abs(angle_deg) < 1e-9:
            return image.copy()

        matrix, output_size = ReferenceImageExtractor.rotation_matrix_bound(image.shape, angle_deg)
        return cv2.warpAffine(
            image,
            matrix,
            output_size,
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0),
        )

    @staticmethod
    def rotation_matrix_bound(image_shape: tuple[int, ...], angle_deg: float) -> tuple[np.ndarray, tuple[int, int]]:
        h, w = image_shape[:2]
        center = (w / 2.0, h / 2.0)
        matrix = cv2.getRotationMatrix2D(center, angle_deg, 1.0)

        cos_v = abs(matrix[0, 0])
        sin_v = abs(matrix[0, 1])
        new_w = int((h * sin_v) + (w * cos_v))
        new_h = int((h * cos_v) + (w * sin_v))

        matrix[0, 2] += (new_w / 2.0) - center[0]
        matrix[1, 2] += (new_h / 2.0) - center[1]

        return matrix, (new_w, new_h)

    @staticmethod
    def clamped_settings(settings: ReferenceExtractionSettings,
                         image_shape: tuple[int, ...]) -> ReferenceExtractionSettings:
        h, w = image_shape[:2]
        width = int(max(1, min(settings.roi_width_px, w)))
        height = int(max(1, min(settings.roi_height_px, h)))

        half_width = width / 2.0
        half_height = height / 2.0
        min_x = int(np.floor(half_width))
        max_x = int(np.ceil(w - half_width))
        min_y = int(np.floor(half_height))
        max_y = int(np.ceil(h - half_height))

        if max_x < min_x:
            min_x = max_x = w // 2
        if max_y < min_y:
            min_y = max_y = h // 2

        return ReferenceExtractionSettings(
            source_path=settings.source_path,
            rotation_angle_deg=float(settings.rotation_angle_deg),
            roi_center_x=int(np.clip(settings.roi_center_x, min_x, max_x)),
            roi_center_y=int(np.clip(settings.roi_center_y, min_y, max_y)),
            roi_width_px=width,
            roi_height_px=height,
            keypoint_x_px=int(np.clip(settings.keypoint_x_px, 0, width - 1)),
            keypoint_y_px=int(np.clip(settings.keypoint_y_px, 0, height - 1)),
            circular_selection=bool(settings.circular_selection),
        )

    @staticmethod
    def roi_rect(settings: ReferenceExtractionSettings) -> tuple[int, int, int, int]:
        width = int(settings.roi_width_px)
        height = int(settings.roi_height_px)
        x0 = int(round(settings.roi_center_x - width / 2.0))
        y0 = int(round(settings.roi_center_y - height / 2.0))
        return x0, y0, x0 + width, y0 + height

    def extract(self, settings: ReferenceExtractionSettings) -> tuple[np.ndarray, ReferenceExtractionSettings]:
        if self.rotated_image is None:
            raise ValueError("No image loaded.")

        settings = self.clamped_settings(settings, self.rotated_image.shape)
        x0, y0, x1, y1 = self.roi_rect(settings)
        reference = self.rotated_image[y0:y1, x0:x1].copy()

        if reference.shape[0] != settings.roi_height_px or reference.shape[1] != settings.roi_width_px:
            raise ValueError("Invalid ROI dimensions after clamping.")

        return reference, settings

    @staticmethod
    def expected_reference_paths(vision_process_path: str) -> tuple[Path, Path]:
        process_path = Path(vision_process_path)
        if process_path.suffix.lower() != ".json":
            raise ValueError("Select a vision process JSON file.")
        base = process_path.parent / f"{process_path.stem}_matcher_reference_image"
        return base.with_suffix(".png"), process_path.parent / f"{base.name}_metadata.json"

    def save_for_vision_process(self,
                                vision_process_path: str,
                                settings: ReferenceExtractionSettings) -> ReferenceSaveResult:
        if self.rotated_image is None:
            raise ValueError("No image loaded.")

        image, clamped = self.extract(settings)
        image_path, metadata_path = self.expected_reference_paths(vision_process_path)

        if not cv2.imwrite(str(image_path), image):
            raise RuntimeError(f"Could not save reference image: {image_path}")

        x0, y0, x1, y1 = self.roi_rect(clamped)
        metadata = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "source_path": self.source_path,
            "vision_process_path": str(Path(vision_process_path)),
            "expected_reference_name": image_path.stem,
            "output_image_path": str(image_path),
            "output_metadata_path": str(metadata_path),
            "settings": asdict(clamped),
            "rotated_image_shape": {
                "height": int(self.rotated_image.shape[0]),
                "width": int(self.rotated_image.shape[1]),
                "channels": int(self.rotated_image.shape[2]) if self.rotated_image.ndim == 3 else 1,
            },
            "source_image_shape": {
                "height": int(self.source_image.shape[0]),
                "width": int(self.source_image.shape[1]),
                "channels": int(self.source_image.shape[2]) if self.source_image.ndim == 3 else 1,
            },
            "roi_rect_px": {
                "x": int(x0),
                "y": int(y0),
                "width": int(x1 - x0),
                "height": int(y1 - y0),
            },
            "reference_image_shape": {
                "height": int(image.shape[0]),
                "width": int(image.shape[1]),
                "channels": int(image.shape[2]) if image.ndim == 3 else 1,
            },
            "reference_keypoint_px": {
                "x": int(clamped.keypoint_x_px),
                "y": int(clamped.keypoint_y_px),
            },
        }

        with open(metadata_path, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

        return ReferenceSaveResult(
            image_path=str(image_path),
            metadata_path=str(metadata_path),
            metadata=metadata,
        )


def cv_image_to_pixmap(image: np.ndarray) -> QPixmap:
    if image.ndim == 2:
        rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w = rgb.shape[:2]
    qimage = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimage.copy())


class ReferenceImageView(QGraphicsView):
    imageDropped = pyqtSignal(str)
    metadataDropped = pyqtSignal(str)
    roiCenterChanged = pyqtSignal(int, int)
    keyPointChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setAcceptDrops(True)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(QColor(28, 28, 28))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._pixmap_item: QGraphicsPixmapItem | None = None
        self._roi_rect_item: QGraphicsRectItem | None = None
        self._roi_circle_item: QGraphicsEllipseItem | None = None
        self._axis_items: list[QGraphicsLineItem] = []
        self._image_shape: tuple[int, int] | None = None
        self._dragging_roi = False
        self._dragging_keypoint = False
        self.drag_mode = "roi"
        self._apply_drag_mode()

    def set_drag_mode(self, mode: str):
        self.drag_mode = mode if mode in ("roi", "keypoint", "view") else "roi"
        self._dragging_roi = False
        self._dragging_keypoint = False
        self._apply_drag_mode()

    def _apply_drag_mode(self):
        drag_mode = (
            QGraphicsView.DragMode.ScrollHandDrag
            if self.drag_mode == "view"
            else QGraphicsView.DragMode.NoDrag
        )
        self.setDragMode(drag_mode)

    def set_image(self, image: np.ndarray, preserve_view: bool = False):
        old_transform = self.transform()
        old_center = self.mapToScene(self.viewport().rect().center())
        restore_view = preserve_view and self._pixmap_item is not None

        pixmap = cv_image_to_pixmap(image)
        self._scene.clear()
        self._axis_items.clear()
        self._roi_rect_item = None
        self._roi_circle_item = None
        self._pixmap_item = self._scene.addPixmap(pixmap)
        self._pixmap_item.setPos(0, 0)
        self._image_shape = image.shape[:2]
        self._scene.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))

        if restore_view:
            self.setTransform(old_transform)
            self.centerOn(old_center)
        else:
            self.fitInView(self._scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def update_overlay(self, settings: ReferenceExtractionSettings):
        if self._image_shape is None:
            return

        width = settings.roi_width_px
        height = settings.roi_height_px
        half_width = width / 2.0
        half_height = height / 2.0
        rect = QRectF(
            settings.roi_center_x - half_width,
            settings.roi_center_y - half_height,
            width,
            height,
        )

        if self._roi_rect_item is None or self._roi_rect_item.scene() is None:
            self._roi_rect_item = QGraphicsRectItem()
            self._scene.addItem(self._roi_rect_item)

        self._roi_rect_item.setRect(rect)
        self._roi_rect_item.setPen(QPen(QColor(255, 210, 0), 2))
        self._roi_rect_item.setBrush(QColor(255, 210, 0, 24))
        self._roi_rect_item.setZValue(10)

        if settings.circular_selection:
            if self._roi_circle_item is None or self._roi_circle_item.scene() is None:
                self._roi_circle_item = QGraphicsEllipseItem()
                self._scene.addItem(self._roi_circle_item)
            circle_size = min(width, height)
            circle_half = circle_size / 2.0
            circle_rect = QRectF(
                settings.roi_center_x - circle_half,
                settings.roi_center_y - circle_half,
                circle_size,
                circle_size,
            )
            self._roi_circle_item.setRect(circle_rect)
            self._roi_circle_item.setPen(QPen(QColor(0, 190, 255), 2))
            self._roi_circle_item.setBrush(QColor(0, 190, 255, 18))
            self._roi_circle_item.setZValue(11)
        elif self._roi_circle_item is not None and self._roi_circle_item.scene() is not None:
            self._scene.removeItem(self._roi_circle_item)
            self._roi_circle_item = None

        for item in self._axis_items:
            if item.scene() is not None:
                self._scene.removeItem(item)
        self._axis_items.clear()

        x0, y0, x1, y1 = ReferenceImageExtractor.roi_rect(settings)
        cx = x0 + settings.keypoint_x_px
        cy = y0 + settings.keypoint_y_px
        x_axis = self._scene.addLine(x0, cy, x1, cy, QPen(QColor(255, 60, 60), 2))
        y_axis = self._scene.addLine(cx, y1, cx, y0, QPen(QColor(60, 220, 90), 2))
        x_axis.setZValue(12)
        y_axis.setZValue(12)
        self._axis_items.extend([x_axis, y_axis])

    def dragEnterEvent(self, event: QDragEnterEvent):
        if self._drop_file(event) is not None:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        dropped = self._drop_file(event)
        if dropped is None:
            event.ignore()
            return
        kind, path = dropped
        if kind == "metadata":
            self.metadataDropped.emit(path)
        else:
            self.imageDropped.emit(path)
        event.acceptProposedAction()

    def wheelEvent(self, event):
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._image_shape is not None:
            point = self.mapToScene(event.pos())
            if self._point_in_image(point):
                if self.drag_mode == "view":
                    return super().mousePressEvent(event)
                if self.drag_mode == "keypoint":
                    self._dragging_keypoint = True
                    self.keyPointChanged.emit(int(round(point.x())), int(round(point.y())))
                    event.accept()
                    return
                self._dragging_roi = True
                self.roiCenterChanged.emit(int(round(point.x())), int(round(point.y())))
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging_roi and self._image_shape is not None:
            point = self.mapToScene(event.pos())
            if self._point_in_image(point):
                self.roiCenterChanged.emit(int(round(point.x())), int(round(point.y())))
            event.accept()
            return
        if self._dragging_keypoint and self._image_shape is not None:
            point = self.mapToScene(event.pos())
            if self._point_in_image(point):
                self.keyPointChanged.emit(int(round(point.x())), int(round(point.y())))
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._dragging_roi:
            self._dragging_roi = False
            event.accept()
            return
        if event.button() == Qt.MouseButton.LeftButton and self._dragging_keypoint:
            self._dragging_keypoint = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def _point_in_image(self, point: QPointF) -> bool:
        if self._image_shape is None:
            return False
        h, w = self._image_shape
        return 0 <= point.x() < w and 0 <= point.y() < h

    @staticmethod
    def _drop_file(event) -> tuple[str, str] | None:
        mime_data = event.mimeData()

        if mime_data.hasUrls():
            for url in mime_data.urls():
                path = url.toLocalFile()
                dropped = ReferenceImageView._classify_drop_path(path)
                if dropped is not None:
                    return dropped

        if mime_data.hasText():
            text = mime_data.text().strip()
            if text.startswith("file://"):
                text = text.removeprefix("file://")
            dropped = ReferenceImageView._classify_drop_path(text)
            if dropped is not None:
                return dropped

        return None

    @staticmethod
    def _classify_drop_path(path: str) -> tuple[str, str] | None:
        file_path = Path(path)
        if not file_path.is_file():
            return None
        suffix = file_path.suffix.lower()
        if suffix in SUPPORTED_IMAGE_EXTENSIONS:
            return "image", str(file_path)
        if suffix in SUPPORTED_METADATA_EXTENSIONS:
            return "metadata", str(file_path)
        return None


class ZoomableImageView(QGraphicsView):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(QColor(28, 28, 28))
        self._pixmap_item = self._scene.addPixmap(pixmap)
        self._scene.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))
        self._fit_pending = True

    def showEvent(self, event):
        super().showEvent(event)
        if self._fit_pending:
            self.fit_to_view()
            self._fit_pending = False

    def wheelEvent(self, event):
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def fit_to_view(self):
        self.resetTransform()
        self.fitInView(self._scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def reset_zoom(self):
        self.resetTransform()


class ReferencePictureCreatorWidget(QWidget):
    saved = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.extractor = ReferenceImageExtractor()
        self.settings = ReferenceExtractionSettings()
        self._updating_controls = False

        self.image_view = ReferenceImageView()
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(180, 180)
        self.preview_label.setStyleSheet("background-color: #202020; color: #cfcfcf;")
        self.preview_label.setText("Reference preview")

        self.open_button = QPushButton("Open Image")
        self.save_button = QPushButton("Save Reference")
        self.test_matcher_button = QPushButton("Test Matcher")
        self.process_file_button = QPushButton("Browse")
        self.load_metadata_button = QPushButton("Load from Metadata")

        self.rotation_spin = QDoubleSpinBox()
        self.rotation_spin.setRange(-180.0, 180.0)
        self.rotation_spin.setSingleStep(0.5)
        self.rotation_spin.setDecimals(2)

        self.roi_x_spin = QSpinBox()
        self.roi_y_spin = QSpinBox()
        self.roi_width_spin = QSpinBox()
        self.roi_height_spin = QSpinBox()
        self.keypoint_x_spin = QSpinBox()
        self.keypoint_y_spin = QSpinBox()
        for spin in (self.roi_x_spin, self.roi_y_spin):
            spin.setRange(0, 100000)
        for spin in (self.roi_width_spin, self.roi_height_spin):
            spin.setRange(1, 100000)
            spin.setSingleStep(2)
        for spin in (self.keypoint_x_spin, self.keypoint_y_spin):
            spin.setRange(0, 100000)

        self.circular_check = QCheckBox("Circular selection")
        self.drag_roi_button = QPushButton("ROI")
        self.drag_keypoint_button = QPushButton("Key point")
        self.drag_view_button = QPushButton("Image view")
        self.drag_mode_buttons = {
            "roi": self.drag_roi_button,
            "keypoint": self.drag_keypoint_button,
            "view": self.drag_view_button,
        }
        for button in self.drag_mode_buttons.values():
            button.setCheckable(True)
            button.setMinimumHeight(30)
            button.setStyleSheet(
                "QPushButton {"
                "  border: 1px solid #6a6a6a;"
                "  background-color: #303030;"
                "  color: #e6e6e6;"
                "  padding: 5px 10px;"
                "}"
                "QPushButton:checked {"
                "  border: 1px solid #f0c400;"
                "  background-color: #b06b00;"
                "  color: #ffffff;"
                "}"
            )
        self.drag_roi_button.setChecked(True)
        self.process_file_edit = QLineEdit()
        self.process_file_edit.setPlaceholderText("Select a vision process .json file")
        self.status_label = QLabel("Drop an image here or open one.")

        self._build_layout()
        self._connect_signals()
        self._install_drop_filter()

    def _build_layout(self):
        controls = QWidget()
        form = QFormLayout(controls)
        mode_row = QHBoxLayout()
        mode_row.addWidget(self.drag_roi_button)
        mode_row.addWidget(self.drag_keypoint_button)
        mode_row.addWidget(self.drag_view_button)
        form.addRow("Mode", mode_row)
        form.addRow(self.open_button)
        form.addRow(self.load_metadata_button)
        form.addRow("Rotation [deg]", self.rotation_spin)
        form.addRow("ROI center x [px]", self.roi_x_spin)
        form.addRow("ROI center y [px]", self.roi_y_spin)
        form.addRow("ROI width [px]", self.roi_width_spin)
        form.addRow("ROI height [px]", self.roi_height_spin)
        form.addRow("Key point x [px]", self.keypoint_x_spin)
        form.addRow("Key point y [px]", self.keypoint_y_spin)
        form.addRow(self.circular_check)

        process_row = QHBoxLayout()
        process_row.addWidget(self.process_file_edit, 1)
        process_row.addWidget(self.process_file_button)
        form.addRow("Vision process", process_row)
        form.addRow(self.save_button)
        form.addRow(self.test_matcher_button)
        form.addRow(self.status_label)

        side = QVBoxLayout()
        side.addWidget(controls)
        side.addWidget(self.preview_label, 1)

        layout = QGridLayout(self)
        layout.addWidget(self.image_view, 0, 0)
        layout.addLayout(side, 0, 1)
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 1)

    def _connect_signals(self):
        self.open_button.clicked.connect(self.open_image_dialog)
        self.save_button.clicked.connect(self.save_reference)
        self.test_matcher_button.clicked.connect(self.test_matcher)
        self.process_file_button.clicked.connect(self.select_vision_process_file)
        self.load_metadata_button.clicked.connect(self.load_from_metadata_dialog)
        self.image_view.imageDropped.connect(self.load_image)
        self.image_view.metadataDropped.connect(self.load_from_metadata)
        self.image_view.roiCenterChanged.connect(self.set_roi_center)
        self.image_view.keyPointChanged.connect(self.set_keypoint_from_image)
        self.rotation_spin.valueChanged.connect(self.set_rotation)
        self.roi_x_spin.valueChanged.connect(self._controls_to_settings)
        self.roi_y_spin.valueChanged.connect(self._controls_to_settings)
        self.roi_width_spin.valueChanged.connect(self._controls_to_settings)
        self.roi_height_spin.valueChanged.connect(self._controls_to_settings)
        self.keypoint_x_spin.valueChanged.connect(self._controls_to_settings)
        self.keypoint_y_spin.valueChanged.connect(self._controls_to_settings)
        self.circular_check.toggled.connect(self._controls_to_settings)
        self.drag_roi_button.clicked.connect(lambda: self._set_drag_mode("roi"))
        self.drag_keypoint_button.clicked.connect(lambda: self._set_drag_mode("keypoint"))
        self.drag_view_button.clicked.connect(lambda: self._set_drag_mode("view"))

    def open_image_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open source image",
            "",
            "Images (*.bmp *.png *.jpg *.jpeg *.tif *.tiff)",
        )
        if path:
            self.load_image(path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if ReferenceImageView._drop_file(event) is not None:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        dropped = ReferenceImageView._drop_file(event)
        if dropped is None:
            event.ignore()
            return
        self._load_dropped_file(dropped)
        event.acceptProposedAction()

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.Type.DragEnter, QEvent.Type.DragMove):
            if ReferenceImageView._drop_file(event) is not None:
                event.acceptProposedAction()
                return True
        elif event.type() == QEvent.Type.Drop:
            dropped = ReferenceImageView._drop_file(event)
            if dropped is not None:
                self._load_dropped_file(dropped)
                event.acceptProposedAction()
                return True

        return super().eventFilter(watched, event)

    def _load_dropped_file(self, dropped: tuple[str, str]):
        kind, path = dropped
        if kind == "metadata":
            self.load_from_metadata(path)
        else:
            self.load_image(path)

    def _install_drop_filter(self):
        self.setAcceptDrops(True)
        self.installEventFilter(self)
        for child in self.findChildren(QWidget):
            child.setAcceptDrops(True)
            child.installEventFilter(self)

    def load_image(self, path: str):
        try:
            rotated = self.extractor.load_image(path)
        except Exception as exc:
            QMessageBox.warning(self, "Could not open image", str(exc))
            return

        h, w = rotated.shape[:2]
        size = max(1, min(w, h) // 3)
        if size % 2 != 0:
            size -= 1
        size = max(1, size)

        self.settings = ReferenceExtractionSettings(
            source_path=path,
            rotation_angle_deg=0.0,
            roi_center_x=w // 2,
            roi_center_y=h // 2,
            roi_width_px=size,
            roi_height_px=size,
            keypoint_x_px=size // 2,
            keypoint_y_px=size // 2,
            circular_selection=False,
        )

        self.image_view.set_image(rotated)
        self._sync_controls_from_settings()
        self._refresh_preview()
        self.status_label.setText(f"Loaded {Path(path).name}")

    def load_from_metadata_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load reference metadata",
            "",
            "Metadata (*.json)",
        )
        if not path:
            return
        self.load_from_metadata(path)

    def load_from_metadata(self, metadata_path: str):
        metadata_file = Path(metadata_path)
        if not metadata_file.is_file():
            QMessageBox.warning(
                self, "Metadata not found", f"Metadata file does not exist: {metadata_path}"
            )
            return

        try:
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            QMessageBox.warning(self, "Could not read metadata", str(exc))
            return

        if "settings" not in metadata or not isinstance(metadata["settings"], dict):
            QMessageBox.warning(
                self,
                "Invalid metadata",
                "The selected file does not contain a 'settings' block.",
            )
            return

        settings_data = dict(metadata["settings"])
        if "keypoint_x_px" not in settings_data or "keypoint_y_px" not in settings_data:
            keypoint = metadata.get("reference_keypoint_px")
            if isinstance(keypoint, dict):
                settings_data["keypoint_x_px"] = int(keypoint.get("x", settings_data.get("roi_width_px", 128) // 2))
                settings_data["keypoint_y_px"] = int(keypoint.get("y", settings_data.get("roi_height_px", 128) // 2))
            else:
                settings_data["keypoint_x_px"] = int(settings_data.get("roi_width_px", 128) // 2)
                settings_data["keypoint_y_px"] = int(settings_data.get("roi_height_px", 128) // 2)

        loaded_settings = ReferenceExtractionSettings(**settings_data)

        source_path_str = metadata.get("source_path") or loaded_settings.source_path
        source_path = Path(source_path_str) if source_path_str else None

        if source_path is None or not source_path.is_file():
            prompt = "The recorded source image could not be found."
            if source_path is not None:
                prompt += f"\n\nExpected location:\n{source_path}"
            prompt += "\n\nPlease select the correct source image."

            QMessageBox.information(self, "Source image missing", prompt)
            chosen, _ = QFileDialog.getOpenFileName(
                self,
                "Select source image",
                str(source_path.parent) if source_path is not None else "",
                "Images (*.bmp *.png *.jpg *.jpeg *.tif *.tiff)",
            )
            if not chosen:
                self.status_label.setText(
                    f"Metadata loaded from {metadata_file.name}, but source image was not provided."
                )
                return
            source_path = Path(chosen)

        try:
            rotated = self.extractor.load_image(str(source_path))
        except Exception as exc:
            QMessageBox.warning(self, "Could not open image", str(exc))
            return

        self.settings = loaded_settings
        try:
            rotated = self.extractor.rotate_source(self.settings.rotation_angle_deg)
        except Exception as exc:
            QMessageBox.warning(self, "Could not rotate image", str(exc))
            return

        # Apply loaded settings, then clamp against the actual rotated image shape.
        if self.extractor.rotated_image is not None:
            self.settings = self.extractor.clamped_settings(
                self.settings, self.extractor.rotated_image.shape
            )

        self.image_view.set_image(rotated)
        self._sync_controls_from_settings()
        self._refresh_preview()

        vision_process_path = metadata.get("vision_process_path")
        if vision_process_path:
            self.process_file_edit.setText(str(vision_process_path))

        source_match = (
            "source image OK"
            if source_path == Path(source_path_str or "")
            else "source image reassigned"
        )
        self.status_label.setText(
            f"Loaded metadata {metadata_file.name} ({source_match}); "
            f"image: {source_path.name}"
        )

    def set_rotation(self, angle: float):
        if self._updating_controls or not self.extractor.has_image():
            return

        self.settings.rotation_angle_deg = float(angle)
        rotated = self.extractor.rotate_source(angle)
        h, w = rotated.shape[:2]
        self.settings.roi_width_px = min(self.settings.roi_width_px, w)
        self.settings.roi_height_px = min(self.settings.roi_height_px, h)
        self.settings.roi_center_x = min(max(self.settings.roi_center_x, 0), w - 1)
        self.settings.roi_center_y = min(max(self.settings.roi_center_y, 0), h - 1)
        self.settings = self.extractor.clamped_settings(self.settings, rotated.shape)

        self.image_view.set_image(rotated, preserve_view=True)
        self._sync_controls_from_settings()
        self._refresh_preview()

    def set_roi_center(self, x: int, y: int):
        if not self.extractor.has_image():
            return
        self.settings.roi_center_x = x
        self.settings.roi_center_y = y
        self.settings = self.extractor.clamped_settings(self.settings, self.extractor.rotated_image.shape)
        self._sync_controls_from_settings()
        self._refresh_preview()

    def set_keypoint_from_image(self, x: int, y: int):
        if not self.extractor.has_image():
            return
        x0, y0, _x1, _y1 = self.extractor.roi_rect(self.settings)
        self.settings.keypoint_x_px = x - x0
        self.settings.keypoint_y_px = y - y0
        self.settings = self.extractor.clamped_settings(self.settings, self.extractor.rotated_image.shape)
        self._sync_controls_from_settings()
        self._refresh_preview()

    def _set_drag_mode(self, mode: str):
        if mode not in self.drag_mode_buttons:
            mode = "roi"
        for button_mode, button in self.drag_mode_buttons.items():
            button.setChecked(button_mode == mode)
        self.image_view.set_drag_mode(mode)

    def _matcher_parameters_from_process(self) -> dict:
        process_file = self.process_file_edit.text().strip()
        if process_file == "" or not Path(process_file).is_file():
            return {}

        try:
            with open(process_file, "r", encoding="utf-8") as file:
                process = json.load(file)
        except (OSError, json.JSONDecodeError):
            return {}

        for step in process.get("vision_pipeline", []):
            if not isinstance(step, dict):
                continue
            params = step.get("PictureReferenceMatcher")
            if params is None:
                params = step.get("CoarseFineChamferMatcher")
            if isinstance(params, dict):
                return params
        return {}

    def _expected_source_pose(self) -> tuple[float, float, float]:
        if self.extractor.source_image is None:
            return (
                float(self.settings.roi_center_x),
                float(self.settings.roi_center_y),
                0.0,
            )

        matrix, _output_size = self.extractor.rotation_matrix_bound(
            self.extractor.source_image.shape,
            self.settings.rotation_angle_deg,
        )
        inverse = cv2.invertAffineTransform(matrix)
        source_center = inverse @ np.array(
            [
                float(self.settings.roi_center_x),
                float(self.settings.roi_center_y),
                1.0,
            ],
            dtype=np.float64,
        )
        return (
            float(source_center[0]),
            float(source_center[1]),
            -float(self.settings.rotation_angle_deg),
        )

    def test_matcher(self):
        if self.extractor.source_image is None:
            QMessageBox.information(self, "No image", "Load an image before testing the matcher.")
            return

        try:
            reference_image, clamped = self.extractor.extract(self.settings)
            self.settings = clamped
        except Exception as exc:
            QMessageBox.warning(self, "Matcher test failed", str(exc))
            return

        try:
            from pm_vision_manager.va_py_modules.feature_detect_functions.picture_reference_matcher import (
                CoarseFineChamferMatcher,
            )
        except Exception as exc:
            QMessageBox.warning(self, "Matcher unavailable", str(exc))
            return

        params = self._matcher_parameters_from_process()
        matcher = CoarseFineChamferMatcher(
            pyramid_levels=int(params.get("pyramid_levels", 3)),
            canny_low=int(params.get("canny_low", 50)),
            canny_high=int(params.get("canny_high", 150)),
            max_template_points=int(params.get("max_template_points", 1500)),
            edge_mode=params.get("edge_mode", "gradient"),
            edge_percentile=float(params.get("edge_percentile", 92.0)),
            ignore_border=int(params.get("ignore_border", 2)),
            coarse_angle_min=float(params.get("coarse_angle_min", -45.0)),
            coarse_angle_max=float(params.get("coarse_angle_max", 45.0)),
            coarse_angle_step=float(params.get("coarse_angle_step", 5.0)),
            refine_angle_window=float(params.get("refine_angle_window", 5.0)),
            refine_angle_step=float(params.get("refine_angle_step", 1.0)),
            fine_angle_window=float(params.get("fine_angle_window", 1.0)),
            fine_angle_step=float(params.get("fine_angle_step", 0.2)),
            min_visible_fraction=float(params.get("min_visible_fraction", 0.90)),
            random_seed=int(params.get("random_seed", 0)),
            reference_keypoint=(self.settings.keypoint_x_px, self.settings.keypoint_y_px),
            use_appearance_score=bool(params.get("use_appearance_score", True)),
            appearance_weight=float(params.get("appearance_weight", 0.02)),
            max_appearance_points=int(params.get("max_appearance_points", 600)),
            verbose=bool(params.get("verbose", False)),
        )

        try:
            matcher.set_images(reference_image, self.extractor.source_image)
            expected_x, expected_y, expected_angle = self._expected_source_pose()
            xy_window = max(20.0, min(self.settings.roi_width_px, self.settings.roi_height_px) * 0.15)
            angle_window = 1.0
            result = matcher.match_near(
                center_x=expected_x,
                center_y=expected_y,
                angle=expected_angle,
                xy_window=xy_window,
                angle_window=angle_window,
            )
            overlay = matcher.verify(
                result=result,
                template=reference_image,
                image=self.extractor.source_image,
                show=False,
                draw_contour=True,
                tint=(0, 255, 255),
                alpha=0.25,
            )
        except Exception as exc:
            QMessageBox.warning(self, "Matcher test failed", str(exc))
            return

        output_path = Path("/tmp") / (
            f"reference_matcher_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        cv2.imwrite(str(output_path), overlay)

        self.status_label.setText(
            "Matcher: "
            f"x={result['x_abs']:.2f}px, y={result['y_abs']:.2f}px, "
            f"angle={result['angle']:.3f}deg, score={result['score']:.6f}; "
            f"local search around x={expected_x:.1f}, y={expected_y:.1f}; "
            f"overlay: {output_path}"
        )
        self._show_matcher_result_dialog(overlay, result, output_path)

    def _show_matcher_result_dialog(self, overlay: np.ndarray, result: dict, output_path: Path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Reference Matcher Test")
        dialog.setModal(True)

        result_text = QLabel(
            f"x={result['x_abs']:.2f}px, y={result['y_abs']:.2f}px, "
            f"angle={result['angle']:.3f}deg, score={result['score']:.6f}\n"
            f"Overlay saved to: {output_path}"
        )
        result_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        image_view = ZoomableImageView(cv_image_to_pixmap(overlay))

        fit_button = QPushButton("Fit")
        fit_button.clicked.connect(image_view.fit_to_view)
        actual_size_button = QPushButton("100%")
        actual_size_button.clicked.connect(image_view.reset_zoom)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)

        button_row = QHBoxLayout()
        button_row.addWidget(fit_button)
        button_row.addWidget(actual_size_button)
        button_row.addStretch(1)
        button_row.addWidget(close_button)

        layout = QVBoxLayout(dialog)
        layout.addWidget(result_text)
        layout.addWidget(image_view, 1)
        layout.addLayout(button_row)

        dialog.resize(1200, 800)
        dialog.exec()

    def _controls_to_settings(self):
        if self._updating_controls or not self.extractor.has_image():
            return
        self.settings.roi_center_x = self.roi_x_spin.value()
        self.settings.roi_center_y = self.roi_y_spin.value()
        self.settings.roi_width_px = self.roi_width_spin.value()
        self.settings.roi_height_px = self.roi_height_spin.value()
        self.settings.keypoint_x_px = self.keypoint_x_spin.value()
        self.settings.keypoint_y_px = self.keypoint_y_spin.value()
        self.settings.circular_selection = self.circular_check.isChecked()
        self.settings = self.extractor.clamped_settings(self.settings, self.extractor.rotated_image.shape)
        self._sync_controls_from_settings()
        self._refresh_preview()

    def _sync_controls_from_settings(self):
        self._updating_controls = True
        try:
            if self.extractor.rotated_image is not None:
                h, w = self.extractor.rotated_image.shape[:2]
                self.roi_x_spin.setMaximum(max(0, w - 1))
                self.roi_y_spin.setMaximum(max(0, h - 1))
                self.roi_width_spin.setMaximum(max(1, w))
                self.roi_height_spin.setMaximum(max(1, h))

            self.rotation_spin.setValue(float(self.settings.rotation_angle_deg))
            self.roi_x_spin.setValue(int(self.settings.roi_center_x))
            self.roi_y_spin.setValue(int(self.settings.roi_center_y))
            self.roi_width_spin.setValue(int(self.settings.roi_width_px))
            self.roi_height_spin.setValue(int(self.settings.roi_height_px))
            self.keypoint_x_spin.setMaximum(max(0, int(self.settings.roi_width_px) - 1))
            self.keypoint_y_spin.setMaximum(max(0, int(self.settings.roi_height_px) - 1))
            self.keypoint_x_spin.setValue(int(self.settings.keypoint_x_px))
            self.keypoint_y_spin.setValue(int(self.settings.keypoint_y_px))
            self.circular_check.setChecked(bool(self.settings.circular_selection))
            self.image_view.update_overlay(self.settings)
        finally:
            self._updating_controls = False

    def _refresh_preview(self):
        if self.extractor.rotated_image is None:
            return
        try:
            image, clamped = self.extractor.extract(self.settings)
            self.settings = clamped
        except Exception as exc:
            self.status_label.setText(str(exc))
            return

        preview_image = image.copy()
        keypoint = (int(self.settings.keypoint_x_px), int(self.settings.keypoint_y_px))
        cv2.line(
            preview_image,
            (0, keypoint[1]),
            (max(0, preview_image.shape[1] - 1), keypoint[1]),
            (0, 0, 255),
            2
        )
        cv2.line(
            preview_image,
            (keypoint[0], max(0, preview_image.shape[0] - 1)),
            (keypoint[0], 0),
            (0, 255, 0),
            2
        )
        pixmap = cv_image_to_pixmap(preview_image)
        scaled = pixmap.scaled(
            self.preview_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setPixmap(scaled)
        self.image_view.update_overlay(self.settings)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_preview()

    def select_vision_process_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select vision process",
            self.process_file_edit.text(),
            "Vision process (*.json)",
        )
        if path:
            self.process_file_edit.setText(path)
            image_path, _metadata_path = self.extractor.expected_reference_paths(path)
            self.status_label.setText(f"Reference will be saved as {image_path.name}")

    def save_reference(self):
        if not self.extractor.has_image():
            QMessageBox.information(self, "No image", "Load an image before saving a reference.")
            return

        process_file = self.process_file_edit.text().strip()
        if process_file == "":
            QMessageBox.information(self, "No vision process", "Select a vision process JSON file before saving.")
            return
        if not Path(process_file).is_file():
            QMessageBox.information(self, "Invalid vision process", "The selected vision process file does not exist.")
            return

        try:
            result = self.extractor.save_for_vision_process(process_file, self.settings)
        except Exception as exc:
            QMessageBox.warning(self, "Save failed", str(exc))
            return

        self.status_label.setText(f"Saved {Path(result.image_path).name}")
        self.saved.emit(result.image_path, result.metadata_path)

    def current_settings(self) -> ReferenceExtractionSettings:
        return self.settings


class ReferencePictureCreatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reference Picture Creator")
        self.creator_widget = ReferencePictureCreatorWidget(self)
        self.setCentralWidget(self.creator_widget)
        self.resize(1200, 800)


def main():
    app = QApplication(sys.argv)
    window = ReferencePictureCreatorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
