# This program takes an image using L1_camera, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).
# This program requires that opencv2 is installed for python3.



"""
***************************************************************************
                        HEAVILY MODIFIED FROM ORIGINAL
***************************************************************************
                            can be used to find HSV 
"""





# Import internal programs:
import L1_camera as cam

# Import external programs:
import cv2          # computer vision
import numpy as np  # for handling matrices
import time         # for keeping time

# Define global parameters
color_range = ((0,100,180),(25,145,255))  # This color range defines the color target
yote = 1
cont = 0
prev = None

def autoYeet(color_range,yote = 1,cont = 0,prev=None):
    h1,h2,s1,s2,v1,v2 = 0,0,0,0,0,0
    print('----------------')
    print('curr vals: ',color_range)
    print('----------------')
    ans = prev
    if not cont:
        print('val to test (hmin,smin,vmin,hmax,smax,vmax): ')
        ans = input()
        cont = 1
    print('up or down?(u,d,n,back): ')
    tmp = input()
    if tmp == 'back':
        cont = 0
        return color_range,yote,cont,ans
    if tmp == 'yeet' or ans =='yeet':
        yote = 0
        return color_range, yote,cont,ans
    if tmp =='n' or tmp =='':
        return color_range,yote,cont,ans
    
    
    h1 = color_range[0][0]
            
    s1 = color_range[0][1]
            
    v1 = color_range[0][2]
            
    h2 = color_range[1][0]
            
    s2 = color_range[1][1]
            
    v2 = color_range[1][2]
    
    # what do you wanna tell joe byron right now?
    # wassup baby, take me out to dinner *wink*
    # AYO?!         
            

    if ans == 'hmin':
        if tmp == 'u':
            h1 = h1 + 10
        elif tmp =='d':
            h1 = h1 - 10
    if ans == 'smin':
        if tmp == 'u':
            s1 = s1 + 10
        elif tmp =='d':
            s1 = s1 - 10
    if ans == 'vmin':
        if tmp == 'u':
            v1 = v1 + 10
        elif tmp =='d':
            v1 = v1 - 10
    if ans == 'hmax':
        if tmp == 'u':
            h2 = h2 + 10
        elif tmp =='d':
            h2 = h2 - 10
    if ans == 'smax':
        if tmp == 'u':
            s2 = s2 + 10 
        elif tmp =='d':
            s2 = s2 - 10
    if ans == 'vmax':
        if tmp == 'u':
            v2 = v2 + 10
        elif tmp =='d':
            v2 = v2 - 10
    color_range = ((h1,s1,v1),(h2,s2,v2))
    print("new vals: ",color_range)
    return color_range,yote,cont,ans


def testing(color_range,yote):
    print('----------------')
    print('curr vals: ',color_range)
    print('----------------')
    h1 = input('h min: ')
    if h1 == 'yeet':
        yote = 0
        return color_range,yote
    if h1 == '':
        return color_range,yote
    
    else:
        h1 = int(h1)
        s1 = int(input('s min: '))
        v1 = int(input('v min: '))
        print()
        h2 = int(input('h max: '))
        s2 = int(input('s max: '))
        v2 = int(input('v max: '))
        return ((h1,s1,v1),(h2,s2,v2)),yote

def colorTarget(color_range=((0, 0, 0), (255, 255, 255))): # function defaults to open range if no range is provided
    image = cam.newImage()
    if filter == 'RGB':
        image_hsv = image.copy()
    else:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # convert to hsv colorspace

    thresh = cv2.inRange(image_hsv, color_range[0], color_range[1])
    kernel = np.ones((5, 5), np.uint8)                                      # apply a blur function
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)                 # Apply blur
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)                  # Apply blur 2nd iteration

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)[-2]                        # generates number of contiguous "1" pixels


    '''********* Used for testing ***********'''
    #cv2.imshow('mask',mask)
    #cv2.imshow('orig', image)
    #cv2.waitKey(20)
    '''**************************************'''


    if len(cnts) > 0:                                           # begin processing if there are "1" pixels discovered
        c = max(cnts, key=cv2.contourArea)                      # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)            # get properties of circle around shape
        targ = np.array([int(x), int(y),                        # return x, y, radius, of target 
                round(radius, 1)])
        return targ
    else:
        return np.array([None, None, 0])

def getAngle(x):                         # check deviation of target from center
    if x is not None:
        ratio = x / 240                  # divide by pixels in width
        offset = -2*(ratio - 0.5)        # offset.  Now, positive = right, negative = left
        offset_x = round(offset,2)       # perform rounding
        return (offset_x)
    else:
        return None

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:


        '''if yote:
            print(color_range[0][0])
            color_range,yote,cont,prev=autoYeet(color_range,yote,cont,prev)
            #color_range,yote = testing(color_range,yote)'''


        target = colorTarget(color_range) # generate a target
        print(target)
        x = target[0]
        if x is None:
            print("no target located.")
        else:
            x_range = getAngle(x)
            print("Target x location: ", x_range)
        time.sleep(0.1) # short delay