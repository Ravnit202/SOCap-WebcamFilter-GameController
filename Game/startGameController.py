from gameHandDetection import HandDetection
from finger import FingerDetector
import keyboard as kb
import pydirectinput as inp
import cv2
import sys


def main():
    if len(sys.argv) >= 1:
        keys = []
        for i in sys.argv[1:]:
            keys.append(i)
        hand_detect = HandDetection(joint_list=[[4,8],[4,12],[4,16],[4,20]], keys=keys)
    else:
        hand_detect = HandDetection(joint_list=[[4,8],[4,12],[4,16],[4,20]])

    finger = FingerDetector()
    cap = cv2.VideoCapture(0)
    while not kb.is_pressed('='):
        
        choice = None
        _, frame = cap.read()

        #frame = cv2.flip(frame, 1)
        
        hand_detect.detect(frame)
        finger.fingerDetection(frame)
        choice = hand_detect.getChoice()
    
        if choice != 'No Key':
            inp.press(choice)

        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('='):
            break

    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()