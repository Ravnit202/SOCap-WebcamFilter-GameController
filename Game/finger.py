import cv2
import mediapipe
import numpy
import pydirectinput
class FingerDetector:


    wScr, hScr = pydirectinput.size() #Get the current screen resolution
    pX, pY = 0, 0 
    cX, cY = 0, 0 

    def __init__(self):
        #Load the mediapipe libraries/solutions
        self.initHand = mediapipe.solutions.hands
        self.mainHand = self.initHand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.draw = mediapipe.solutions.drawing_utils

        self.fingerTips = []
        self.img = None

    def handLandmarks(self, colorImg):
        landmarkList = []

        landmarkPositions = self.mainHand.process(colorImg)  # Process the given image
        landmarkCheck = landmarkPositions.multi_hand_landmarks 

        if landmarkCheck:  # Checks if landmarks exist
            for index, hand in enumerate(landmarkCheck):  # differentiate by hand
                for index, landmark in enumerate(hand.landmark): 
                    self.draw.draw_landmarks(self.img, hand, self.initHand.HAND_CONNECTIONS)  
                    h, w, c = self.img.shape 
                    centerX, centerY = int(landmark.x * w), int(landmark.y * h) 
                    landmarkList.append([index, centerX, centerY]) 
                    
        return landmarkList

    def fingers(self, landmarks):
        fingerTips = []
        tipIds = [4, 8, 12, 16, 20]  #Values for each fingertip
        
        #Check if the thumb is up
        if landmarks[tipIds[0]][1] > self.lmList[tipIds[0] - 1][1]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)
        
        #Check if fingers are up and the thumb is down
        for id in range(1, 5):
            if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
                fingerTips.append(1)
            else:
                fingerTips.append(0)

        return fingerTips


    def fingerDetection(self, frame):
        frame = cv2.flip(frame, 1)
        self.img = frame
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB
        
        self.lmList = self.handLandmarks(imgRGB)

        if len(self.lmList) > 12:
            x1, y1 = self.lmList[8][1:]  
            finger = self.fingers(self.lmList)  
            if finger[1] == 1 and finger[2] == 0:  
                x3 = numpy.interp(x1, (75, 720 - 75), (75, self.wScr))  # Converts the width of the window relative to the screen width
                y3 = numpy.interp(y1, (75, 560 - 75), (75, self.hScr))  # Converts the height of the window relative to the screen height
                
                cX = self.pX + (x3 - self.pX) /2 # Smooth out the mouse x movement
                cY = self.pY + (y3 - self.pY) /2 # Smooth out the mouse y movement

                pydirectinput.moveTo(int(cX), int(cY))  #Move the mouse using pydirectinput
                self.pX, self.pY = cX, cY  # Save the current x and y values

            if finger[1] == 0 and finger[0] == 1:  # Check if the pointer finger is down and the thumb finger is up
                pydirectinput.rightClick()
                
        return
