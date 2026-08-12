from types import SimpleNamespace

import numpy as np

from pm_vision_manager.va_py_modules.vision_pipline_processing import (
    extract_component_uuid,
    saveImage,
)


def test_extracts_component_id_from_vision_measurement_uid():
    component_uuid = "01234567-89ab-cdef-0123-456789abcdef"
    process_uid = f"Component ID: {component_uuid}, Frame: test_frame"

    assert extract_component_uuid(process_uid) == component_uuid


def test_accepts_explicit_component_uuid_marker():
    component_uuid = "01234567-89ab-cdef-0123-456789abcdef"

    assert extract_component_uuid(
        f"component uuid={component_uuid}; frame=test_frame"
    ) == component_uuid


def test_returns_none_when_process_uid_has_no_component():
    assert extract_component_uuid("Frame: test_frame") is None


def test_rejects_component_id_that_is_not_filename_safe():
    assert extract_component_uuid("Component ID: ../../test, Frame: test") is None


def test_save_image_adds_only_component_uuid_to_filename(tmp_path, monkeypatch):
    component_uuid = "01234567-89ab-cdef-0123-456789abcdef"
    written_paths = []
    image = np.zeros((2, 2), dtype=np.uint8)
    response = SimpleNamespace(
        results=SimpleNamespace(saved_images=[]),
    )
    handler = SimpleNamespace(
        cross_val_running=False,
        process_db_path=str(tmp_path),
        get_mode=lambda: 0,
        get_vision_response=lambda: response,
        get_initial_image=lambda: image,
        get_processing_image=lambda: image,
    )

    monkeypatch.setattr(
        "pm_vision_manager.va_py_modules.vision_pipline_processing.cv2.imwrite",
        lambda path, saved_image: written_paths.append(path) or True,
    )

    saveImage(
        handler,
        save_input_image=True,
        save_input_image_with_results=False,
        save_current_image=False,
        save_function_prefix="save_image_1",
        execution_timestamp="2026-08-12_12-00-00",
        process_uid=f"Component ID: {component_uuid}, Frame: a_very_long_frame_name",
    )

    assert written_paths == [
        str(tmp_path / f"2026-08-12_12-00-00_{component_uuid}_input.png")
    ]
