import cv2
import time 
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import osascript


target_volume = 30
vol = "set volume output volume " + str(target_volume)
osascript.osascript(vol)

cap = cv2.VideoCapture(0)
preTime = 0

detector = htm.HandDector(detectionConfidence=0.8)
volume_bar = 0




while True:

    success, img = cap.read()
    img = detector.FindHand(img)
    lmlist = detector.FindPosition(img,draw=False)


    if len(lmlist) != 0 :
        detector.Highlight(img,position=[8,4])
        volumeControl = detector.DrawLineBetween(img,points=(0,1))

        scaled_volume  = np.interp(int(volumeControl),[35,250],[0,100 ])
        volume_bar = np.interp(int(volumeControl),[35,250],[400,150 ])

        if scaled_volume <=0:
            scaled_volume = 0
        elif scaled_volume >= 100:
            scaled_volume = 100
        else:
            scaled_volume = scaled_volume
        
        vol = "set volume output volume " + str(scaled_volume)
        osascript.osascript(vol)
        cv2.rectangle(img,(50,int(volume_bar)),(85,400),(0,0,255),cv2.FILLED)

        

    cv2.rectangle(img,(50,150),(85,400),(0,0,255),3)
    


    currTime = time.time()
    fps = 1/(currTime-preTime) 
    preTime = currTime

    if not success:
        break

    cv2.putText(img,f'FPS:{int(fps)}',(10,30),(cv2.FONT_HERSHEY_SIMPLEX),1,(0,0,0),2)
    cv2.imshow ("Image",img)

 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()   