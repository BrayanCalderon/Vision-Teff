import  cv2
import numpy as np
import time

def selectROI(reset = 0):
    if reset:
        ret, frame = cap.read()
        x,y,w,h = cv2.selectROI(frame)
        return x,y,w,h
    else:
        return 514,328,649,471
        #return 631,136,675,676

def focusROI(frame,x,y,w,h):
    
    #Creo el rectangulo de ROI para realizar la focalización
    area_pts = np.array([[x,y],[x+w,y],[x+w,y+w],[x,y+w]])
    #Creo un array auxiliar para posterior AND
    imAux = np.zeros(shape = (frame.shape[:2]),dtype = np.uint8)
    #Dibujo el contorno creado con los puntos anteriores
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    #Realizo el AND entre la imagen auxiliar y el frame original
    image_area = cv2.bitwise_and(frame,frame, mask=imAux)
    return image_area[y:y+h,x:x+w]

def fps(prev_time):
    new_frame_time = time.time()
    fps = 1/(new_frame_time- prev_time)
    prev_time = new_frame_time
    return prev_time,str(int(fps))

def area(box):
    x = box[0,1]
    y = box[0,0]
    dx1 = box[0,1]-box[3,1]
    dy1 = box[0,0]-box[3,0]
    dx2 = box[0,1]-box[1,1]
    dy2 = box[0,0]-box[1,0]
    w   = (dx1**2+dy1**2)**(1/2)
    h   = (dx2**2+dy2**2)**(1/2)
    return x,y,w,h

def contours(frame):
    
    img_gray_b = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    ret,th1 = cv2.threshold(img_gray_b,110,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    outer_contours = []
    src_color = img_gray_b.copy()
    color_copy = frame.copy()
    if contours:
        # Seleccionar solo los contornos que no tienen padres por nivel de jerarquia
        for i in range(len(hierarchy[0])):
            if hierarchy[0,i,3] < 1:
                outer_contours.append(contours[i])
            else:
                continue

        rects = []
        h_max = 0
        w_max = 0

        for i in range(len(outer_contours)):
            
            # Obtengo el centro del contorno, largo y alto, y ángulo
            rect = cv2.minAreaRect(outer_contours[i])
            # obtengo representación en puntos
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            x ,y ,w, h = area(box)
            
            # Selecciona los contornos que cumplen ciertas condiciones
            if (w*h >= src_color.shape[0]*src_color.shape[1]) or w*h < 20 or w*h > 300:
                continue
            else:
                #Dibuja los contornos de los elementos encontrados
                cv2.drawContours(src_color,[box],0,(0,255,0),2)
                rect = cv2.minAreaRect(outer_contours[i])
                w,h = rect[1]
                x,y = rect[0]
                if w+x > w_max:
                    w_max = w+x
                elif y+h > h_max:
                    h_max = h+y
                rects.append(rect)
        return src_color
    return src_color

def draw_line(frame):
    #Shape X = 676, Y = 675
    
    start_point = (0,(frame.shape[0]//2)-120)
    end_point = (frame.shape[0]+200,(frame.shape[0]//2)-120)
    frame = cv2.line(frame,start_point,end_point,(0, 255, 255),2)
    
    start_point = (0,(frame.shape[0]//2)+120)
    end_point = (frame.shape[0]+200,(frame.shape[0]//2)+120)
    frame = cv2.line(frame,start_point,end_point,(0, 255, 255),2)
    return frame
        
    



cap = cv2.VideoCapture("F_8_3000_1.mkv")
x,y,w,h = selectROI(0)
print(x,y,w,h)
prev_time_fps = 0
min_fps = 60
max_fps = 0



fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 60.0, (471,649))

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (471,649))



    
    


while True:
    
    ret, frame = cap.read()
    if not ret:break
    cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
    frameaux = focusROI(frame,x,y,w,h)
    frameaux = contours(frameaux)
    frameaux = draw_line(frameaux)
    
    
    prev_time_fps,fpsframe = fps(prev_time_fps)
    cv2.putText(frame, fpsframe, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow("frame", frame)
    
    frameaux= cv2.resize(frameaux, (471, 649))
    frameaux = cv2.cvtColor(frameaux, cv2.COLOR_GRAY2BGR)


    out.write(frameaux)

    cv2.imshow("ROI", frameaux)
    
    
    
    if int(fpsframe) < min_fps and (int(fpsframe) > 0):
        min_fps = int(fpsframe)
    elif int(fpsframe)  > max_fps:
        max_fps = int(fpsframe)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
cap.release()
out.release()


print(f"El minimo FPS fue de {min_fps} y el maximo FPS fue de {max_fps} ")
 
        