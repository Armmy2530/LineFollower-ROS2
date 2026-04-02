# Line Follower Robot (ROS2)

A ROS2-based autonomous line follower robot using computer vision and PID control.

## Preview
![Simulation Preview](assets/armmyRobotCam_1stWorking.gif)

## Introduction

This project implements an autonomous line-following robot using ROS2. The robot uses a camera to detect a line on the ground and follows it using a PID controller. The system consists of:

- **Image Processing**: OpenCV-based line detection using thresholding and contour analysis
- **PID Controller**: Precise steering control based on line position error
- **Gazebo Simulation**: Full simulation environment with robot model and track

## Project Structure

```
LineFollower-ROS2/
├── src/
│   ├── line_follower/           # Main line follower package
│   │   ├── line_follower/       # Python nodes
│   │   │   ├── pid_follow.py    # PID controller node
│   │   │   ├── image_pub.py     # Image publisher node
│   │   │   ├── image_sub.py     # Image subscriber node
│   │   │   ├── image_process.py # Image processing utilities
│   │   │   └── test_plotter.py  # Testing utilities
│   │   ├── config/
│   │   │   └── line_follower_params.yaml
│   │   ├── data/test_data/      # Test images
│   │   └── package.xml
│   │
│   ├── line_interfaces/         # Custom ROS interfaces
│   │   ├── msg/
│   │   │   └── LineError.msg    # Custom message for error position
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   └── gazebo_simulation/       # Gazebo simulation files
│       ├── urdf/                # Robot URDF files
│       ├── worlds/              # Gazebo world files
│       ├── models/              # Gazebo models
│       ├── rviz/                # RViz configurations
│       ├── CMakeLists.txt
│       └── package.xml
│
└── armmyRobotCam_1stWorking.mp4 # Demo video
```

### Packages Overview

| Package | Description |
|---------|-------------|
| `line_follower` | Main node handling image processing and PID control |
| `line_interfaces` | Custom ROS message definitions |
| `gazebo_simulation` | Gazebo robot models and simulation worlds |

## How to run


```bash
# Launch Gazebo with track world
ros2 launch gazebo_simulation robot_world.launch.py

# Start line follower nodes
ros2 run line_follower pid_follow
```

### Configuration

Edit `src/line_follower/config/line_follower_params.yaml` to tune PID parameters:

```yaml
pid:
  kp: 0.015
  ki: 0.0
  kd: 0.0
```

## Architecture

```
[Camera] -> [image_pub] -> [Image Processing] -> [LineError] -> [PID Controller] -> [cmd_vel] -> [Robot]
```

1. **image_pub**: Publishes camera images
2. **image_process**: Detects line position and calculates error
3. **pid_follow**: Subscribes to error, publishes velocity commands
