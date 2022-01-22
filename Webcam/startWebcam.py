from webcamHandDetection import HandDetection
from segmentation import WebcamEffects
import keyboard as kb
import cv2


def main():
    #Setup both hand detection and finger detection classes
    hand_detect = HandDetection(joint_list=[[4,8],[4,12],[4,16],[4,20]])
    wb_effect = WebcamEffects()

    #Start video capture
    cap = cv2.VideoCapture(0)
    saved_choice = None
    while not kb.is_pressed('='):
        ret, frame = cap.read() #Read the current frame

        #Checks and skips empty frames
        if not ret:
             continue

        frame = cv2.flip(frame, 1) 

        hand_detect.detect(frame) #Detect the hand movement

        choice = hand_detect.getChoice()

        if(choice != None and choice != saved_choice):
            saved_choice = choice
            
        #Do nothing to freeze the camera
        if choice == 'stopTime': 
            pass
        
        else:
            frame = wb_effect.Capture(frame, saved_choice) #Add then show the applied filter

            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('='):
            break

    cap.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()