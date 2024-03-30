import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    
    package_name='gazebo_simulation' #<--- CHANGE ME

    # Set the path to the Gazebo ROS package
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')  
    
    # Set the path to this package.
    pkg_share = FindPackageShare(package='gazebo_simulation').find('gazebo_simulation')

    default_rviz_config_path = PathJoinSubstitution([get_package_share_directory(package_name), 'rviz', 'urdf.rviz'])
    
    # Set the path to the world file
    world_file_name = 'line_track.world'
    world_path = os.path.join(pkg_share, 'worlds', world_file_name)
    world = LaunchConfiguration('world')

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','load_world_gazebo.launch.py'
                    )]), 
                    launch_arguments={'world': world}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=["-topic", "robot_description", "-entity", "robot"],    
                        # arguments=["-topic", "robot_description", "-entity", "robot", "-x", "0.0", "-y", "0.0", "-z", "0.0"],    
                        output='screen')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config_path]
    )

    # Launch them all!
    return LaunchDescription([
        declare_world_cmd,
        rsp,
        gazebo,
        spawn_entity,
        rviz_node,
    ])