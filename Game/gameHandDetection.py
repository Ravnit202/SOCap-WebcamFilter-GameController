import cv2
import mediapipe as mp
import numpy as np

class HandDetection:

    def __init__(self, joint_list=[[4,8]], keys = ['q','w','e','r','f','d']):
        """
        Initialize all objects
        """
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.joint_list = joint_list 
        self.choice = None
        self.keys = keys


    def draw_left_hand_values(self, image, hand, joint_list):
        """
        Draws values onto Left hand
        """
        j1 = False
        j2 = False
        j3 = False
        j4 = False

        for i in range(len(joint_list)):
                
                a = np.array([hand.landmark[joint_list[i][0]].x, hand.landmark[joint_list[i][0]].y]) # First coord
                b = np.array([hand.landmark[joint_list[i][1]].x, hand.landmark[joint_list[i][1]].y]) # Second coord

                dist = np.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2) #Calculate the distance between a fingertip and the thumb

                if(dist < 0.028): #If the distance between a fingertip and thumb is below 0.028, we know the action has been performed
                    if(i == 0):
                        j1 = True
                    elif(i == 1):
                        j2 = True
                    elif (i == 2):
                        j3 = True
                    elif (i == 3):
                        j4 = True

                cv2.putText(image, str(round(dist, 4)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        return [j1, j2, j3, j4]


    def label_hand(self, index, hand, results):
        """
        Label the hand with all landmarks
        """
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
        """
        Update the current choice
        """
        self.choice = choice
 
    def getChoice(self):
        """
        Get the current choice
        """
        return self.choice

    def detect(self, frame):
        """
        Detect the hand motion and process the image
        """
        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
                # BGR 2 RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Flip Horizontally
                image = cv2.flip(image, 1)
                
                image.flags.writeable = False
                
                # Detections
                results = hands.process(image)
                
                image.flags.writeable = True
                
                # RGB 2 BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Detections
                l_hand = None
                r_hand = None
                vals = [False, False, False, False]
                # Rendering results
                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS, 
                                                self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                                self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                                )
                        # Differentiate between left and right hands
                        if self.label_hand(num, hand, results):
                            text, coord = self.label_hand(num, hand, results)
                            h = text.split(' ')
                            if h[0] == "Left":
                                l_hand = hand
                                
                            if h[0] == "Right" or h[0] == None:
                                r_hand = hand
                            
                            cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Draw angles to image from joint list if the left hand is up
                if(l_hand):
                    vals = self.draw_left_hand_values(image, l_hand, self.joint_list)

                    if vals[0] is True and vals[1] is True:
                        self.updateChoice(self.keys[5])
                    elif vals[2] is True and vals[3] is True:
                        self.updateChoice(self.keys[4])
                    elif vals[0] is True:
                        self.updateChoice(self.keys[0])
                    elif vals[1] is True:
                        self.updateChoice(self.keys[1])
                    elif vals[2] is True:
                        self.updateChoice(self.keys[2])
                    elif vals[3] is True:
                        self.updateChoice(self.keys[3])
                    else:
                        self.updateChoice('No Key')
                else:
                    self.updateChoice('No Key')
        return image
