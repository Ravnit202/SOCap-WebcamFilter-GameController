import cv2
import mediapipe
import numpy
import pydirectinput

class FingerDetector:


    wScr, hScr = pydirectinput.size() 
    pX, pY = 0, 0 
    cX, cY = 0, 0 

    def __init__(self):
        self.initHand = mediapipe.solutions.hands
        self.mainHand = self.initHand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.draw = mediapipe.solutions.drawing_utils
        self.fingerTips = []
        self.img = None

    def handLandmarks(self, colorImg):

        landmarkList = []  # Default values if no landmarks are tracked

        landmarkPositions = self.mainHand.process(colorImg)  # Object for processing the video input
        landmarkCheck = landmarkPositions.multi_hand_landmarks 

        if landmarkCheck:  # Checks if landmarks are tracked
            for index, hand in enumerate(landmarkCheck):  # Landmarks for each hand
                for index, landmark in enumerate(hand.landmark): 
                    self.draw.draw_landmarks(self.img, hand, self.initHand.HAND_CONNECTIONS)  
                    h, w, c = self.img.shape 
                    centerX, centerY = int(landmark.x * w), int(landmark.y * h) 
                    landmarkList.append([index, centerX, centerY]) 
                    
        return landmarkList

    def fingers(self, landmarks):
        fingerTips = []  # To store 4 sets of 1s or 0s
        tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger
        
        # Check if thumb is up
        if landmarks[tipIds[0]][1] > self.lmList[tipIds[0] - 1][1]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)
        
        # Check if fingers are up except the thumb
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
            x1, y1 = self.lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)
            x2, y2 = self.lmList[12][1:]  # Gets index 12s x and y values (skips index value because it starts from 1)
            finger = self.fingers(self.lmList)  # Calling the fingers function to check which fingers are up
            
            if finger[1] == 1 and finger[2] == 0:  # Checks to see if the pointing finger is up and thumb finger is down
                x3 = numpy.interp(x1, (75, 720 - 75), (75, self.wScr))  # Converts the width of the window relative to the screen width
                y3 = numpy.interp(y1, (75, 560 - 75), (75, self.hScr))  # Converts the height of the window relative to the screen height
                
                cX = self.pX + (x3 - self.pX) / 4  # Stores previous x locations to update current x location
                cY = self.pY + (y3 - self.pY) / 4  # Stores previous y locations to update current y location

                pydirectinput.moveTo(int(cX), int(cY))  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
                self.pX, self.pY = cX, cY  # Stores the current x and y location as previous x and y location for next loop

            if finger[1] == 0 and finger[0] == 1:  # Checks to see if the pointer finger is down and thumb finger is up
                pydirectinput.rightClick()
                
        return
