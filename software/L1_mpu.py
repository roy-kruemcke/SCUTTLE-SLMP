# L1_mpu.py
# Author: Roy Kruemcke (roanoake)
# 30 NOV 2021
# Allows for the interfacing to the MPU9250 using the smbus2 i2c module
# Written for use with Raspberry Pi 4 Model B
import smbus2
import numpy as np
import data
import time

# Initialize Register Data
CONFIG = 0x1A
USER_CTRL = 0x6A
PWR_MGMT_1, PWR_MGMT_2 = 0x6B, 0x6C
GYRO_CONFIG = 0x1B
G_OFFSET = 0x13
GYRO_OUT = 0x43
ACCEL_CONFIG = 0x1C
ACCEL_CONFIG_2 = 0x1D
A_OFFSET = 0x77
ACCEL_OUT = 0x3B
TEMP_OUT = 0x41

# Initialize Scales
MAX_VAL = 2**16
ACCL_SCALE_2G=MAX_VAL/(2*2)         # +-2G
ACCL_SCALE_4G=MAX_VAL/(4*2)         # +-4G
ACCL_SCALE_8G=MAX_VAL/(8*2)         # +-8G
ACCL_SCALE_16G=MAX_VAL/(16*2)       # +-16G

GYRO_SCALE_250DG=MAX_VAL/(250*2)        # +-250 deg/s
GYRO_SCALE_500DG=MAX_VAL/(500*2)        # +-500 deg/s
GYRO_SCALE_1000DG=MAX_VAL/(1000*2)      # +-1000 deg/s
GYRO_SCALE_2000DG=MAX_VAL/(2000*2)      # +-2000 deg/s

# Open I2C bus
bus=smbus2.SMBus(1)

mpu = 0x68      # Default address for MPU

def getAccelScale():
    """
    Reads the current accelerometer scale, and returns the scaling factor.
    """
    acnfg=bus.read_byte_data(mpu,ACCEL_CONFIG)
    scale = (acnfg & 0x18) >> 3  # Bits 4:3 hold the full scale

    # Return the corresponding scale
    if scale==0:   return ACCL_SCALE_2G
    elif scale==1: return ACCL_SCALE_4G
    elif scale==2: return ACCL_SCALE_8G
    elif scale==3: return ACCL_SCALE_16G

    return None         # If you make it here, its bad

def setAccelScale(newScale:int):
    """
    Sets the accelerometer scale.  Returns True if successful, False otherwise.
    :param scale: integer 0-3 that corresponds to the scale.
    """
    # Check input
    if not(0<=newScale<=3):
        print(">> ERROR: attempted to set ACCEL_SCALE to an improper value")
        return False

    # First, read the current scale
    acnfg=bus.read_byte_data(mpu,ACCEL_CONFIG)      # Read ACCEL_CONFIG
    acnfg &= ~0x18                                  # Clear previous scale
    acnfg |= (newScale << 3)                        # Set new scale
    bus.write_byte_data(mpu,ACCEL_CONFIG,acnfg)     # Write new data

    time.sleep(0.01)                                # Wait 10ms

    # Check for completion
    tmp=bus.read_byte_data(mpu,ACCEL_CONFIG)        # Read ACCEL_CONFIG
    tmp=(tmp & 0x18) >> 3                           # Isolate scale

    if tmp==newScale:   # Scale was updated
        return True
    else:               # Scale was not updated
        print("> Warning: ACCEL_SCALE did not update")
        return False


def getGyroScale():
    print("Getting Gyrometer Scale.")
    gcnfg=bus.read_byte_data(mpu,GYRO_CONFIG)
    scale = (gcnfg & 0x18) >> 3  # Bits 4:3 hold the full scale

    # Return the corresponding scale
    if scale==0:   return GYRO_SCALE_250DG
    elif scale==1: return GYRO_SCALE_500DG
    elif scale==2: return GYRO_SCALE_1000DG
    elif scale==3: return GYRO_SCALE_2000DG

    return None         # If you make it here, its bad

def readAccelerometer():
    try:
        # Read Accelerometer Data, 2 bytes for 3 axes, 6 bytes total.
        twoByteReadings = bus.read_i2c_block_data(mpu, ACCEL_OUT, 6)
        
        # compile all the data into the 16-bit/axis readings.
        binaryVals = [(twoByteReadings[i*2] << 8) | twoByteReadings[i*2 + 1] for i in range(3)]
        
        # convert 16-bit unsigned into 16-bit signed
        binaryVals = [data.getSignedVal(i,16) for i in binaryVals]
        scale = getAccelScale()
        
        # scale binary to meaningful value
        accel_vals = [val/scale for val in binaryVals]
        
        # round to 3 decimal places
        accel_vals = np.round(accel_vals,3)
    
    except:
        print(">> ERROR: ACCEL_OUT could not be read.")
        accel_vals = [0,0,0]
    
    return accel_vals

def readGyrometer():
    print("Reading Gyrometer")

def readTemperature():
    print("Reading Temperature")

print(readAccelerometer())
