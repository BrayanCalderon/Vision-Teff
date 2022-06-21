import  cv2
import numpy as np
import time
import socket
import timer_threading as tmth
import trayectoria as trayec


cont_semillas = 0

def selectROI(reset = 0):
    if reset:
        ret, frame = cap.read()
        x,y,w,h = cv2.selectROI(frame)
        return x,y,w,h
    else:
         
        return 616,40,545,1080 #roi perfecto grabación
        #return 254,1,186,462 roi para cuando se conecta camara
        #35 pixeles son alrededor de 2mm
        #17.5 pixeles por tanto son alrededor de 1mm
        #pixel 35 más o menos es el inicio
        

def focusROI(frame,x,y,w,h):
    
    #Creo el rectangulo de ROI para realizar la focalización
    area_pts = np.array([[x,y],[x+w,y],[x+w,y+h],[x,y+h]])
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

def contours(frame,fullframe):
    
    img_gray_b = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    ret,th1 = cv2.threshold(img_gray_b,120,255,cv2.THRESH_BINARY_INV)
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
                cv2.drawContours(frame,[box],0,(0,255,0),1)
                rect = cv2.minAreaRect(outer_contours[i])
                w,h = rect[1]
                x,y = rect[0] #centro
                if w+x > w_max:
                    w_max = w+x
                elif y+h > h_max:
                    h_max = h+y
                rects.append(rect)
                calc_time((x,y))
        return frame
    
    tmth.enviar_pulso(1,0,0,s)
    return frame

def draw_line(frame):
    linea = 35
    while linea < frame.shape[0]:
        start_point = (0,linea)
        end_point = (frame.shape[1],linea)
        frame = cv2.line(frame,start_point,end_point,(0, 255, 255),2)
        linea +=35
    
    ver = 545//3
    while ver < frame.shape[0]:
        start_point = (ver, 0)
        end_point = (ver, frame.shape[0])
        frame = cv2.line(frame,start_point,end_point,(0, 0, 255),2)
        ver += ver
    

   
        
    
    return frame
contador = 0
def calc_time(pos):
    global s, contador
    #Pixel inicio 35
    #2mm -> 35pixeles
    print(f" centro de la semilla es {pos[0]},{pos[1]} ")
    #Divide la sección en 3 partes iguales y me dice que valvula debo activar
    valv = pos[0]//182 #Posición en X
    posy_mm = -((pos[1]*2)/35)
    #print(posy_mm)
    #Mando la señal utilizando la función creada en el otro .py
    time = trayec.trayec_simple(posy_mm, valv )
    tmth.enviar_pulso(2,time,valv+1,s)
    contador += 1
    print(f" tiempo mandado en teoria {time} ")
    global cont_semillas
    cont_semillas += 1


def conexion():
    global s
    try:
        s = socket.socket()
        s.connect(("192.168.4.1",2020))
        print("Conexión Exitosa")
    except:
        print("Intentando conectar de nuevo")
        conexion()    




#Realizo la conexión
conexion()

cap = cv2.VideoCapture("videos/test_4_06.mkv")
cap.set(5, 30)
cap.set(3, 1920)
cap.set(4, 1080)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


x,y,w,h = selectROI(0)
print(x,y,w,h)
prev_time_fps = 0
min_fps = 60
max_fps = 0



#Para grabar video descomentar las dos lineas de abajo
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('outputtest.avi',fourcc, 60.0, (468,174))


while True:
    
    ret, frame = cap.read()

    
    if not ret:break
    cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
    frameaux = focusROI(frame,x,y,w,h)
    frameaux = contours(frameaux,frame)
    frameaux = draw_line(frameaux)
    
    

    
    
    prev_time_fps,fpsframe = fps(prev_time_fps)
    cv2.putText(frame, fpsframe, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow("frame", frame)
    
    frameaux= cv2.resize(frameaux, (471, 649))
    
    #frameaux = cv2.cvtColor(frameaux, cv2.COLOR_GRAY2BGR)


    #for _ in range(20):
    #    out.write(frameaux)

    cv2.imshow("ROI", frameaux)
    
    
    
    if int(fpsframe) < min_fps and (int(fpsframe) > 0):
        min_fps = int(fpsframe)
    elif int(fpsframe)  > max_fps:
        max_fps = int(fpsframe)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
cap.release()
#out.release()


print(f"El minimo FPS fue de {min_fps} y el maximo FPS fue de {max_fps} ")
print(f"Se identificaron {cont_semillas} semillas")
print(f"contador {contador}")
time.sleep(2)
tmth.enviar_pulso(4,0,0,s)

s.close()
 
        