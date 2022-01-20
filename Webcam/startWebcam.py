from webcamHandDetection import HandDetection
from segmentation import WebcamEffects
import keyboard as kb
import cv2


def main():
    hand_detect = HandDetection(joint_list=[[4,8],[4,12],[4,16],[4,20]])
    wb_effect = WebcamEffects()

    cap = cv2.VideoCapture(0)
    saved_choice = None
    while not kb.is_pressed('='):
        _, frame = cap.read()

        frame = cv2.flip(frame, 1)

        hand_detect.detect(frame)

        choice = hand_detect.getChoice()

        if(choice != None and choice != saved_choice):
            saved_choice = choice
            
        if choice == 'stopTime':
            pass
        else:
            frame = wb_effect.Capture(frame, saved_choice)

            
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()