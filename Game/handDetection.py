import cv2
import mediapipe as mp
import numpy as np
from time import time, sleep
import random
import keyboard as kb

class HandDetection:

    def __init__(self, joint_list=[[4,8]]):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.joint_list = joint_list 
        self.choice = None
    
    def draw_left_hand_values(self, image, results, joint_list):
        landmarks = results.multi_hand_landmarks
        # Loop through hands
        for num, hand in enumerate(landmarks):
            try:
                handed = self.get_label(num, hand, results)
                handed = handed[0].split(' ')[0]
            except:
                handed = None

            j1 = False
            j2 = False
            j3 = False
            j4 = False

            #Loop through joint sets 
            if handed is not None:
                for i in range(len(joint_list)):
                    
                    a = np.array([hand.landmark[joint_list[i][0]].x, hand.landmark[joint_list[i][0]].y]) # First coord
                    b = np.array([hand.landmark[joint_list[i][1]].x, hand.landmark[joint_list[i][1]].y]) # Second coord
                    #c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord
                    
                    dist = np.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2)
                    if(dist < 0.025):
                        if(i == 0):
                            #print(dist, 'j1')
                            j1 = True
                        elif(i == 1):
                            #print(dist, 'j2')
                            j2 = True
                        elif (i == 2):
                            #print(dist, 'j3')
                            j3 = True
                        elif (i == 3):
                            #print(dist, 'j4')
                            j4 = True

                    cv2.putText(image, str(round(dist, 4)), tuple(np.multiply(b, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        return [j1, j2, j3, j4]

    def rightHandMouse(self, image, results):
        index_joints = [[8,7]]
        landmarks = results.multi_hand_landmarks
        for num, hand in enumerate(landmarks):
            try:
                handed = self.get_label(num, hand, results)
                handed = handed[0].split(' ')[0]
            except:
                handed = None
            if handed != 'Left':
                for i in range(len(index_joints)):
                    a = np.array([hand.landmark[index_joints[i][0]].x, hand.landmark[index_joints[i][0]].y]) # First coord
                    b = np.array([hand.landmark[index_joints[i][1]].x, hand.landmark[index_joints[i][1]].y]) # Second coord

    def get_label(self, index, hand, results):
        output = None
        for _, classification in enumerate(results.multi_handedness):
            if classification.classification[0].index == index:
                
                # Process results
                label = classification.classification[0].label
                score = classification.classification[0].score
                text = '{} {}'.format(label, round(score, 2))
                
                # Extract Coordinates
                coords = tuple(np.multiply(
                    np.array((hand.landmark[self.mp_hands.HandLandmark.WRIST].x, hand.landmark[self.mp_hands.HandLandmark.WRIST].y)),
                [640,480]).astype(int))
                
                output = text, coords
                
        return output

    def updateChoice(self, choice):
        self.choice = choice
 
    def getChoice(self):
        return self.choice

    def detect(self, frame):
        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
                frame = cv2.flip(frame, 1)
                # BGR 2 RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Flip on horizontal
                image = cv2.flip(image, 1)
                
                # Set flag
                image.flags.writeable = False
                
                # Detections
                results = hands.process(image)
                
                # Set flag to true
                image.flags.writeable = True
                
                # RGB 2 BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Detections
                #print(results)
                l_hand = False
                r_hand = False
                vals = [False, False, False, False]
                # Rendering results
                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS, 
                                                self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                                self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                                )
                        # Render left or right detection
                        if self.get_label(num, hand, results):
                            text, coord = self.get_label(num, hand, results)
                            h = text.split(' ')
                            if h[0] == "Left":
                                l_hand = True
                            #print(h[0])
                            if h[0] == "Right" or h[0] == None:
                                r_hand = True
                            cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # Draw angles to image from joint list
                    vals = self.draw_left_hand_values(image, results, self.joint_list)
                    #self.get_position(results)
                if l_hand is True:
                    if vals[0] is True and vals[1] is True:
                        self.updateChoice('d')
                    if vals[2] is True and vals[3] is True:
                        self.updateChoice('f')
                    elif vals[0] is True:
                        self.updateChoice('q')
                    elif vals[1] is True:
                        self.updateChoice('w')
                    elif vals[2] is True:
                        self.updateChoice('e')
                    elif vals[3] is True:
                        self.updateChoice('r')
                    else:
                        self.updateChoice('No Key')
                else:
                    self.updateChoice('No Key')
