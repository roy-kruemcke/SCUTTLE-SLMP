# SCUTTLE-SLMP
A small logistics management robot using the SCUTTLE platform, LIDAR-based SLAM, odometry and more for warehouse internal logistics automation


This relies on the MXET/SCUTTLE project for many of the basics, which have been ported and organized. 
The link to the original project repository can be found [here](https://github.com/MXET/SCUTTLE)

## Hardware
Rather than using the BeagleBone Blue, this project uses a RaspberryPi due to the extra computing necessary for SLAM functionality.  In addition to the default SCUTTLE platform, this project uses the SICK TiM581 LIDAR, a USB webcam, two servo motors, and dedicated 9-axis IMU board.  These specific details are listed below.

<details><summary>Hardware Details</summary>
  <p>Computing Unit: RaspberryPi 4 Model B, 2GB</p>
  <p>LIDAR: SICK TiM581</p>
  <p>Camera: HP USB Webcam</p>
  <p>Servos: MG 996R 55g Servos</p>
  <p>IMU: HiLetgo MPU9250 9-Axis 16-bit IMU</p>
  </details>

