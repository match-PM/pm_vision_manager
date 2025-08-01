cmake_minimum_required(VERSION 3.8)
project(pm_vision_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ExecuteVision.srv"
  "srv/DemoSetExposure.srv"
  "srv/CalibratePixelPerUm.srv"
  "srv/CalibrateAngle.srv"
  "msg/VisionPoint.msg"
  "msg/CrossValidation.msg"
  "msg/VisionResults.msg"
  "msg/VisionLine.msg"
  "msg/VisionArea.msg"
  "msg/VisionCircle.msg"
  "msg/VisionResponse.msg"
  DEPENDENCIES geometry_msgs # dd packages that above messages depend on, in this case geometry_msgs for Sphere.msg
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
