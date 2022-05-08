import cv2
vidcap = cv2.VideoCapture('vid2.MTS')
success,image = vidcap.read()
count = 0
while success:
  print("entre")
  cv2.imwrite("frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
print("finish")