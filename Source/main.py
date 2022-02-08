
# coding: utf-8

# In[1]:

import cv2
import numpy as np
import pyglet


MEASUREMENTS = 10
THRESHOLD = 10

eye_status = {'detections': [2]*MEASUREMENTS, 'closed_eyes': False}

def check(found_eyes):
    eye_status['detections'].append(found_eyes)
    eye_status['detections'].pop(0)
    eyes_num = sum(eye_status['detections'])
    
    if eyes_num > THRESHOLD:
        eye_status['closed_eyes'] = False
    else:
        eye_status['closed_eyes'] = True
        
        
def change_color(img, pixels, B, G, R):
    for (w,k) in pixels:
        img[w][k] = [B, G, R]
        
        
def draw(img1, img2, i, j):          # i = coordinata verticale, j = orizzontale
    h,w, _ = img2.shape
    img1[i:i+h, j:j+w] = img2[:h, :w]
    
    
def main_face(faces):                # restituisce i parametri della faccia più estesa rilevata nell'immagine
    fx = faces[0][0]
    fy = faces[0][1]
    fw = faces[0][2]
    fh = faces[0][3]
    
    for [x, y, w, h] in faces:
        if w*h > fw*fh:
            fx = x
            fy = y
            fw = w
            fh = h
    return fx, fy, fw, fh

        
face_cascade = cv2.CascadeClassifier('../Assets/lib/face.xml')
eye_cascade = cv2.CascadeClassifier('../Assets/lib/glasses.xml')
        
cv2.VideoCapture(0)
cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

box = cv2.imread('../Assets/Img/quadro.png')
start = cv2.imread('../Assets/Img/start.png')
safe_drive = cv2.imread('../Assets/Img/guida_sicura.png')
distracted_guide = cv2.imread('../Assets/Img/distrazione.png')
danger = cv2.imread('../Assets/Img/Pericolo.png')
triangles = cv2.imread('../Assets/Img/Allarme_sonno.png')
yellow_triangle = cv2.imread('../Assets/Img/attenzione_giallo.png')
open_eyes = cv2.imread('../Assets/Img/occhi_aperti.png')
sound = pyglet.media.load('../Assets/audio/alarm.mp3')
sound2 = pyglet.media.load('../Assets/audio/alarm2.mp3')
pixels = np.loadtxt('../Assets/files/pixels_quadro.txt', dtype = 'int')


draw(box, start, 100, 370)

looper = pyglet.media.SourceGroup(sound.audio_format, None)          #crea looper audio (occhi chiusi)
looper.loop = True
looper.queue(sound)
warning = pyglet.media.Player()
warning.queue(looper)

looper2 = pyglet.media.SourceGroup(sound2.audio_format, None)          #crea looper audio 2 (distrazione)
looper2.loop = True
looper2.queue(sound2)
warning2 = pyglet.media.Player()
warning2.queue(looper2)


while cv2.waitKey(30) != ord('s'):
    cv2.imshow('C.C.A.S.A.: Car Concentration And Security Assistant', box)
else:
    draw(box, safe_drive, 100, 370)
    change_color(box, pixels, 150, 210, 190)
    
while cv2.waitKey(30) != ord('q'):
    ret, camera = cap.read()
        
    gray = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    if len(face) != 0:
        fx, fy, fw, fh = main_face(face)
        
        cv2.rectangle(camera,(fx,fy),(fx+fw,fy+fh),(150,210,190), 1)   
        
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        roi_color = camera[fy:fy+fh, fx:fx+fw]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, maxSize=(int(fw/5),int(fh/5)), minSize=(int(fw/7),int(fh/7)))
        
        check(len(eyes))
        
        for [ex,ey,ew,eh] in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh), (150,210,190), 1)
        
        warning2.pause()
        draw(box, safe_drive, 100, 370)
        draw(box, open_eyes, 500, 455)
        
    else:
        draw(box, distracted_guide, 100, 370)
        draw(box, yellow_triangle, 500, 455)
        warning2.play()
        
    if eye_status['closed_eyes']:
        warning.play()
        draw(box, danger, 100, 370)
        draw(box, triangles, 500, 455)
    else:
        warning.pause()
        
        
    draw(box, camera, 235, 375)
    cv2.imshow('C.C.A.S.A.: Car Concentration And Security Assistant', box)

warning.pause()
warning2.pause()
        
cap.release()
cv2.destroyAllWindows()
