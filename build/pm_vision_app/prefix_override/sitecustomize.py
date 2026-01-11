import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/brotato211/ros2_humble/src/pm_vision_manager/install/pm_vision_app'
