
"""
    The script uses on-board camera to detect color squares on the back of the SLMP dock
    the size of the detected colors is compared to determine if direction adjustment is needed while reversing
    
    used by calling the main() function, main() returns one of 3 values:
        0 = if SLMP has dropped off a load
        1 = if SLMP has picked up a load
        None = if SLMP did not or could not change load status
"""

#### TODO ####

# Search for dock                       -done
# Func for 1 color square               -done
# Func for other color square           -done
# get radii and distance to squares     -done
# Compare radii                         -done
# adjust alignment                      -done
# back into dock                        -done
# repeat aligning as needed             -done
# call pickup or dropoff script         -done


import time
import L2_color_track as tra
import L2_speed_control as sc 
#import Servo_RPi as ser           #implement the new servo script

# BLUE HSV ((90 60 100),(125 105 255))
colorLeft_HSV = [(90,70,70),(125,125,255)]

# ORANGE HSV ((0 100 180),(25 145 255))
colorRight_HSV = [(0,70,110),(25,225,255)]

leftRadius,rightRadius = 0,0
diff = 0                                        # positive = left color closer, negative = right color closer
hasLoad = 0                                     # hasLoad decides if load or unload is called at end of dock
tol = 5                                         # tol used to check if reverse needs adjusting
pdl,pdr = 0,0
global k 
k = 0
max_phi = 9.75                                  # maximum possible wheel speed

leftLast3 = [0,0,0]                         # values to store last 3 adius values for both targets
rightLast3 = [0,0,0]

# get a more accurate value for radii
def average(lis):
    
    sum = 0
    zeros = 0
    for i in lis:
        if not i == 0:
            zeros = zeros + 1
        sum = sum + i 
    return sum/3-zeros

# find if left color is in vision
def find_ColorLeft(HSV = [(0,0,0),(255,255,255)]):
     arr = tra.colorTarget(HSV)     # returns target as [x,y,radius]
     if arr[2] > 2:
         leftRadius = arr[2]
     else: 
         leftRadius = 0
     return leftRadius

# find if right color is in vision
def find_ColorRight(HSV = [(0,0,0),(255,255,255)]):
    arr = tra.colorTarget(HSV)      # returns target as [x,y,radius]
    if arr[2] > 2:
        rightRadius = arr[2]
    else:
        rightRadius = 0
    
    return rightRadius

# compare radii to check if adjustment needed
def diff_In_Radii(leftRadius,rightRadius):
    diff = leftRadius - rightRadius
    
    return diff

# find the dock after navigation
def search(leftRadius,rightRadius):
    pdl = -(max_phi * 0.4)                                   # turn left until targets spotted
    pdr = max_phi * 0.4
    if rightRadius > 0 and leftRadius == 0:     # continue turning left if right target spotted
        #print('orange target found')
        pdl = -(max_phi * 0.4)
        pdr = max_phi * 0.4
        return 0
    elif rightRadius ==0 and leftRadius > 0:    # turn right if left target is spotted
        #print('blue target found')
        pdl = max_phi * 0.4
        pdr = -(max_phi * 0.4)
        return 0
    elif rightRadius > 0 and leftRadius > 0:    # both targets found, return 1
        #print('both targets found')
        return 1
    #print('no targets found')
    return 0

# back into dock, adjust as needed
def reverse(diff):
    pdl,pdr = -(max_phi * 0.4),-(max_phi * 0.4)                 # pdl, pdr equal to reverse straight
    if diff < -tol:                 # adjust left if left target bigger
        pdr = -(max_phi * 0.3)
        pdl = -(max_phi * 0.7)
    elif diff > tol:                # adjust right if right target bigger
        pdr = -(max_phi * 0.7)
        pdl = -(max_phi * 0.3)
    
    sc.driveOpenLoop(sc.openLoop(pdl,pdr))
    #print('pd vals: ',[pdl,pdr])
    return

# check if squares are close enough
def isDocked(leftRadius):
    if leftRadius > 220:
        return 1

def main(hasLoad):
    k = 0
    while(1):
        leftRadius = find_ColorLeft(colorLeft_HSV)
        rightRadius = find_ColorRight(colorRight_HSV)

        leftLast5[k] = leftRadius
        rightLast5[k] = rightRadius
        ''' print('Last 5 values:')
        print('Left: ',leftLast5)
        print('Right: ',rightLast5)
        print(average(leftLast5))'''
        diff = diff_In_Radii(average(leftLast5),average(rightLast5))
        #print("Radii difference: ",diff)

        #print()
        #print()
        #time.sleep(0.5)
        k = k + 1
        if k > 4:
            k = 0

        if search(leftRadius,rightRadius):
            reverse(diff)
            if isDocked(average(leftLast5)) or isDocked(average(rightLast5)):
                print('Docked!')
                break

    if hasLoad:
        #ser.setAngle(0)
        return 0
    else:
        #ser.setAngle(90)
        return 1

    return None


k = 0
main(0)

