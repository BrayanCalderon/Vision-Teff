import cv2
vidcap = cv2.VideoCapture('test_4_06.mkv')
success,image = vidcap.read()
count = 0
while success:
  #print("entre")
  cv2.imwrite("ftest/frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
print("finish")