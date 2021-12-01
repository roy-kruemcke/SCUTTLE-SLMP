# Theory of Operation

## Architecture
There are three levels to the SLMP software, inherited from the original platform.

### Level 1: Data Collection and Control
  This level defines the functions that will be used to interact with the motors,
  encoders, IMU, LIDAR, camera, and servos.  This code is hardware specific.

### Level 2: Mid-Level Functionality
  This level processs information from L1 programs, and can perform more complex actions,
  but they still have a very narrow focus, for example, datalogging or motor speed control.

### Level 3: High-Level Functionality
  This level handles multiple L2 programs, and combines them into tasks.

The data flows up from each level to the next, allowing for subsystem testing.

# Why not ROS?
While an ROS2 implementation was considered, due to the difficulty in sourcing nodes
and establishing the environment, it was decided to stay with the structures that we
already knew.

# Program Flow
## Odometry
  The robot will rely on wheel encoders and an IMU for odometry data; using a Kalman filter,
  the pose will be estimated and used for localization.
## SLAM
  The SLAM implementation, based off xiaofeng's 2D LIDAR SLAM, will use an occupancy matrix
  to build the environment; as more and more scans are taken, there will be more certainty
  in the map data.
## Autonomous Navigation (Possible)
  The original proposal contained autonomous navigation using algorithms such as A* - while this
  is still a goal that could be implemented, it is not likely to happen due to time constraints.
