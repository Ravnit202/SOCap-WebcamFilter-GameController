import cv2
import mediapipe as mp
import numpy as np


class HandDetection:

    def __init__(self, joint_list=[[4,8]]):
        """
        Initialize all objects
        """
        #Load mediapipe libraries/solutions
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.joint_list = joint_list 
        self.choice = None

    def draw_hand_values(self, image, results, joint_list):
        """
        Go through and draw the hand values
        """
        landmarks = results.multi_hand_landmarks
        #Loop through each hand
        for num, hand in enumerate(landmarks):

            j1 = False
            j2 = False
            j3 = False
            j4 = False

            for i in range(len(joint_list)):
                
                a = np.array([hand.landmark[joint_list[i][0]].x, hand.landmark[joint_list[i][0]].y]) # First coord
                b = np.array([hand.landmark[joint_list[i][1]].x, hand.landmark[joint_list[i][1]].y]) # Second coord

                dist = np.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2) # Calculate the distance between a fingertip and the thumb
                if(dist < 0.028):
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

    def get_label(self, index, hand, results):
        """
        Check which hand is being detected, and label the hand
        """
        output = None
        #Determine which hand is being seen 
        for _, classification in enumerate(results.multi_handedness):
            if classification.classification[0].index == index:
                
                label = classification.classification[0].label
                score = classification.classification[0].score
                text = '{} {}'.format(label, round(score, 2))
                
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
        Detect the hand motion and process the image, then updating the choice of filter
        """
        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
                # BGR 2 RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                image.flags.writeable = False
                
                results = hands.process(image)

                image.flags.writeable = True
                
                # RGB 2 BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Detections

                vals = [False, False, False, False]

                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS, 
                                                self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                                self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                                )

                    #Store the fingers pressed
                    vals = self.draw_hand_values(image, results, self.joint_list)

                #Update the chosen filter
                if vals[0] is True and vals[1] is True:
                    self.updateChoice('stopTime')
                elif vals[2] is True and vals[3] is True:
                    self.updateChoice('cloneUser')
                elif vals[0] is True:
                    self.updateChoice('blurBackground')
                elif vals[1] is True:
                    self.updateChoice('changeBackground')
                elif vals[2] is True:
                    self.updateChoice('boxFilter')
                elif vals[3] is True:
                    self.updateChoice('desatureBackground')
