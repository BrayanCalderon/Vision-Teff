import cv2
import numpy as np

cap = cv2.VideoCapture(0)
j = 0
frames = []
while j<30:
    _,frame = cap.read()
    frames.append(frame)
    j+=1 
    print(j)
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1)
    if key ==27:
        break
print(frame.shape)
cap.release()
cv2.destroyAllWindows()

for fram in frames:
    cv2.imshow("Frames",fram[:,:])

cap.release()
cv2.destroyAllWindows()
