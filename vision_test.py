import cv2
import numpy as np


def pre_process(frame):
    frame_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    src_filter = gaussian(frame_processed)
    #Closing
    kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(src_filter, cv2.MORPH_CLOSE, kernel, iterations = 1)
   
    #Binary Treshold 
    ret,thresh1 = cv2.threshold(closing,190,255,cv2.THRESH_BINARY)
    for i in range(len(thresh1)):
        for j in range(5):
            thresh1[i,j] = 255
    for i in range(-1,-9,-1):
        for j in range(len(thresh1)):
            thresh1[i,j] = 255

    #erode
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh1,kernel,iterations = 1)
    return erosion

def gaussian(img):
    img = cv2.medianBlur(img,7)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    return th2

def hsv_pre(frame):

    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    umbral_bajo = (0,0,0)
    umbral_alto = (28,190,34)
    #mascara
    mask = cv2.inRange(img_hsv,umbral_bajo,umbral_alto)
    
    #frame[mask==255] = (0,255,0)
    res = cv2.bitwise_and(img_hsv,img_hsv,mask = mask)
    res[mask==255] = (255,0,0)
    res[mask==0] = (mask)
    
    return res



def increase_sat(frame):
    val = 20
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(frame_hsv)
    
    #hago una suma vectorizada de que a cada pixel le sumo val
    s += val
    #Hago una condicion de que si el valor del pixel es mayor a 255, valga 255, de lo contrario quedará igual
    s[s>255] = 255
    merge = cv2.merge([h,s,v])
    frame = cv2.cvtColor(merge,cv2.COLOR_HSV2BGR)
    return frame



# g = alpha*pixel+beta, funcion lineal donde alpha es el brillo y beta es el contraste
# podemos vectorizar para obtener una mejor calidad

def lineal_img(frame,alpha,beta):
    print(f"El tamaño del frame original {frame.shape}")
    
    print(f"El tamaño de new_img {new_img.shape}")
    print(new_img)
    #new_img[new_img > 255] = 255
    return new_img

def nothing(x):
    pass

def convertToJpeg(img):
    result, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
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

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width,frame_height)
fourcc = cv2.VideoWriter_fourcc(*'RGBA')
result = cv2.VideoWriter("cut.avi",
                          fourcc,
                          30,(850,440))

frame_cont = 0
while True:
    filename = f"{frame_cont}.bmp"
    frame_cont += 1
    ret,frame = cap.read()
    if frame is None:
        break

    #converting jpeg
    #frame = convertToJpeg(frame)
    
    #Extract ROI
    roi = frame[:,:]
    #roi = frame[160:600,700:1550]
    #roi = increase_sat(roi)
    #3 de brillo
    #6 de contraste
    #result.write(roi)
    alpha = int(cv2.getTrackbarPos("alpha","Trackbar"))
    beta = int(cv2.getTrackbarPos("beta","Trackbar"))
    roi = cv2.convertScaleAbs(roi, alpha=3, beta=6)
    #cv2.imwrite(filename,frame)

    
    
    roi = hsv_pre(roi)

    #Draw Lines
    cv2.line(frame,(700,160),(700,600),(0,0,255),2) #Vertical izquierda
    cv2.line(frame,(700,160),(1550,160),(0,0,255),2) #Horizontal Superior
    cv2.line(frame,(700,600),(1550,600),(0,0,255),2) #Horizontal inferior
    cv2.line(frame,(1550,160),(1550,600),(0,0,255),2) #Vertical derecha

    cv2.imshow("Original",frame)
    cv2.imshow("Sección",roi)

    key = cv2.waitKey(1)
    if key ==27:
        break


cap.release()
result.release()
cv2.destroyAllWindows()