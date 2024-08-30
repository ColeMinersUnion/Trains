import cv2
import mediapipe as mp
import time

#?This was made at https://lvimuth.medium.com/hand-detection-in-python-using-opencv-and-mediapipe-30c7b54f5ff4
#*Should be a simple hand detection model. 

#TODO: Create a class for hand recognition
#TODO: Try to recognize certain hand shapes. 


class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionCon=0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        img = cv2.flip(img, 1) #*eh
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:   
                '''
                
                    '''
                if draw:
                    self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        return lmlist

    
if(__name__ == '__main__'):
    
    #*I"m just working on adding an fps thingy on my video frame
    old = 0
    curr = 0
    
    hand = handDetector()
    cam = cv2.VideoCapture(0)
    while(True):
        #*Reads the current frames from the webcam
        check, frame = cam.read()
        #*alters the frame by checking the hand
        #*showing the frames as a video
        
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        curr = time.time()
        fps = 1/(curr-old)
        fps = str(int(fps))
         
        old = curr
        
        frame = hand.findHands(frame)
        cv2.putText(frame, fps, (7, 70), font, 3, (0, 0, 0), 3, cv2.LINE_AA)
        
        #cv2.imshow('video', hand.findHands(frame))
        #? averaging about 15 fps with hand in frame
        #? Or about 21 without a hand in frame
        #* Therefore it takes about 1/3 of runtime to run the handtracking model
        #* And 1/6 of frame runtime to draw everything. I hope these scale linearly. 
        #! These are WITHOUT cuda
        
        cv2.imshow('video', frame) 
        #! Baseline FPS bc my computer sucks
        #? About 31 fps, sucks but fine

        #print(fps + "\n")
        key = cv2.waitKey(1)
        if(key == 27):
            break
    print("Video Ended")
    

        
        