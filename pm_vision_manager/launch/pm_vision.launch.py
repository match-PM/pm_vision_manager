import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Define launch arguments
    my_param = DeclareLaunchArgument('my_param', default_value='default_value', description='An example parameter')

    # Define a ROS 2 node
    my_node = Node(
        package='pm_vision_manager',
        executable='vision_node',
        name='PM_Vision_node',
        #parameters=[{'param_name': LaunchConfiguration('my_param')}]
        emulate_tty=True
    )
    
    ld = LaunchDescription()
    ld.add_action(my_node)

    return ld