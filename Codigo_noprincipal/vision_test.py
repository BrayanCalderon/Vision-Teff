import cv2
import numpy as np



def hsv_pre(frame):

    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    #Umbrales de color
    umbral_bajo = (0,0,0)
    umbral_alto = (28,190,34)
    
    #mascara
    mask = cv2.inRange(img_hsv,umbral_bajo,umbral_alto)
    frame[mask==255] = (0,255,0)
    res = cv2.bitwise_and(img_hsv,img_hsv,mask = mask)
    res[mask==255] = (255,0,0)    
    return res


def nothing(x):
    pass

def convertToJpeg(img):
    result, encoded = cv2.imencode('.png', img, [cv2.IMWRITE_PNG_STRATEGY, 100])
    return cv2.imdecode(encoded, 1)

cv2.namedWindow("Trackbar")
cv2.createTrackbar("alpha","Trackbar",3,100,nothing)
cv2.createTrackbar("beta","Trackbar",6,100,nothing)



#Video
#Detalles video ejemplo
#Resolución 1920x1080
#Frames: 30 fps
#duración: 26 segundos, total 780 frames
#digicamcontrol

try:
    cap = cv2.VideoCapture("test.mkv")
except:
    print("No pude entrar a esta monda")

#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))

#size = (frame_width,frame_height)

#fourcc = cv2.VideoWriter_fourcc(*'RGBA')
#result = cv2.VideoWriter("cut.avi",
#                          fourcc,
#                          30,(850,440))

frame_cont = 0
while True:
    filename = f"{frame_cont}.png"
    frame_cont += 1
    ret,frame = cap.read()
    if frame is None:
        break

    #converting jpeg
    #frame = convertToJpeg(frame)
 
    #ret,frame = cap.read()

    
    #Extract ROI
    #roi = frame[160:600,300:900]
    #Resolución para camara
    #roi = frame[160:600,700:1550]
    #3 de brillo
    #6 de contraste
    #result.write(roi)
    #alpha = int(cv2.getTrackbarPos("alpha","Trackbar"))
    #beta = int(cv2.getTrackbarPos("beta","Trackbar"))
    #roi = cv2.convertScaleAbs(roi, alpha=3, beta=6)
    try:
        cv2.imwrite(filename,frame)
    except:
        print("Me cagué")
    
    
    #roi = hsv_pre(roi)

    #Draw Lines
    #cv2.line(frame,(700,160),(700,600),(0,0,255),2) #Vertical izquierda
    #cv2.line(frame,(700,160),(1550,160),(0,0,255),2) #Horizontal Superior
    #cv2.line(frame,(700,600),(1550,600),(0,0,255),2) #Horizontal inferior
    #cv2.line(frame,(1550,160),(1550,600),(0,0,255),2) #Vertical derecha

    #cv2.imshow("Original",frame)
    #cv2.imshow("Sección",roi)

    key = cv2.waitKey(1)
    if key ==27:
        break


cap.release()
#result.release()
cv2.destroyAllWindows()