There are three levels to the SLMP software, inherited from the original platform.



# Level 1: Data Collection and Control
  This level defines the functions that will be used to interact with the motors,
  encoders, IMU, LIDAR, camera, and servos.  This code is hardware specific.

# Level 2: Mid-Level Functionality
  This level processs information from L1 programs, and can perform more complex actions,
  but they still have a very narrow focus, for example, datalogging or motor speed control.

# Level 3: High-Level Functionality
  This level handles multiple L2 programs, and combines them into tasks.

The data flows up from each level to the next, allowing for subsystem testing.

# Why not ROS?
While an ROS2 implementation was considered, due to the difficulty in sourcing nodes
and establishing the environment, it was decided to stay with the structures that we
already knew.
