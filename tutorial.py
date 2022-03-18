from __future__ import print_function
import cv2 as cv
import argparse

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
shift_h = 0
shift_s = 0
shift_v = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
window_result_name = 'result Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
SAdd = "SAdd"
SSub = "SSub"
VAdd = "VAdd"
VSub = "Vsub"

def shift_channel(c, amount):
    if amount > 0:
        c+= amount
        c[c >= 255] = 255
    elif amount < 0:
        c += amount
        c[c<0] = 0
    return c

## [low]
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
## [low]

## [high]
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
## [high]

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

def on_SAdd(val):
    global shift_s
    shift_s = val
    cv.setTrackbarPos(SAdd,window_detection_name,shift_s)

def on_SSub(val):
    pass
def on_VAdd(val):
    pass
def on_VSub(val):
    pass

def hsv_shift(frame_HSV,shift_h,shift_s,shift_v):
    h,s,v = cv.split(frame_HSV)
    shift_h2 = shift_channel(h,shift_h)
    shift_s2 = shift_channel(s,shift_s)
    shift_v2 = shift_channel(v,shift_v)
    shift_hsv = cv.merge([shift_h2,shift_s2,shift_v2])
    return shift_hsv


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()

## [cap]
cap = cv.VideoCapture("Videos/cut.MTS")
## [cap]

## [window]
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.namedWindow(window_result_name)
## [window]

## [trackbar]
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

cv.createTrackbar(SAdd, window_detection_name, 0, 255, on_SAdd)
cv.createTrackbar(SSub, window_detection_name, 0, 255, on_SSub)
cv.createTrackbar(VAdd, window_detection_name, 0, 255, on_VAdd)
cv.createTrackbar(VSub, window_detection_name, 0, 255, on_VSub)



## [trackbar]

while True:
    ## [while]
    ret, frame = cap.read()
    frame = cv.imread("teff.PNG")
    
    if frame is None:
        break

        #Extract ROI
    #roi = frame[160:600,700:1550]

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_shift = hsv_shift(frame_HSV,shift_h,shift_s,shift_v)
    frame_RGB = cv.cvtColor(frame_shift,cv.COLOR_HSV2BGR)
    frame_threshold = cv.inRange(frame_shift, (low_H, low_S, low_V), (high_H, high_S, high_V))
    
    ## [while]

    ## [show]
    cv.imshow(window_capture_name, frame_RGB)
    #cv.imshow(window_detection_name, frame_threshold)
    cv.imshow(window_result_name,frame_threshold)
    ## [show]

    key = cv.waitKey(60)
    if key == ord('q') or key == 27:
        break



