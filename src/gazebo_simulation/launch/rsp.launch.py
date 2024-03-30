from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()
    urdf_tutorial_path = FindPackageShare('gazebo_simulation')
    default_model_path = PathJoinSubstitution(['urdf', 'armmyRobot3_cam_gazebo.urdf'])
    default_rviz_config_path = PathJoinSubstitution([urdf_tutorial_path, 'rviz', 'urdf.rviz'])

    ld.add_action(DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                     description='Absolute path to rviz config file'))

    # This parameter has changed its meaning slightly from previous versions
    ld.add_action(DeclareLaunchArgument(name='model', default_value=default_model_path,
                                        description='Path to robot urdf file relative to urdf_tutorial package'))
                                        
    #  This parameter has changed its meaning slightly from previous versions
    ld.add_action(DeclareLaunchArgument(name='sim_time', default_value='false', choices=['true', 'false'],
                                        description='Use sim time if true'))
       
    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'description.launch.py']),
        launch_arguments={
            'urdf_package': 'gazebo_simulation',
            'urdf_package_path': LaunchConfiguration('model'),
            'rviz_config': LaunchConfiguration('rvizconfig'),
            'use_sim_time' : LaunchConfiguration('sim_time')
            }.items()
    ))

    return ld