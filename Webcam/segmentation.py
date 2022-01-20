import os
import cv2
import numpy as np
import mediapipe as mp

background_images = []
        # Specify the path of the folder which contains the background images.
background_folder = './images/backgrounds'

class WebcamEffects:

    def __init__(self, bg_img=None, blur=0.95, thresh=0.3, method = None):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segment = self.mp_selfie_segmentation.SelfieSegmentation(0)
        self.bg_img = bg_img
        self.blur = blur
        self.thresh = thresh
        self.method = method
        self.prev_choice = None
        
        for img_path in os.listdir(background_folder):

            image = cv2.imread(f"{background_folder}/{img_path}")

            background_images.append(image)

        self.bg_img_index = 1

    def modifyBackground(self, image, background_image = 255, blur = 95, threshold = 0.3, method='changeBackground'):

        # Convert the image from BGR to RGB
        RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        result = self.segment.process(RGB_img)

        binary_mask = result.segmentation_mask > threshold
        
        binary_mask_3 = np.stack((result.segmentation_mask,)*3, axis=-1) > threshold
        if method == 'changeBackground':
        
            background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
            output_image = np.where(binary_mask_3, image, background_image)
            
        elif method == 'blurBackground':
            
            blurred_image = cv2.GaussianBlur(image, (blur, blur), 0)
            output_image = np.where(binary_mask_3, image, blurred_image)
        
        elif method == 'medianBlur':
            blurred_image = cv2.medianBlur(image, 33)
            output_image = np.where(binary_mask_3, blurred_image, image)

        elif method == 'boxFilter':
            box_img = cv2.boxFilter(image,-1, (33,33))
            output_image = np.where(binary_mask_3, box_img, image)

        elif method == 'desatureBackground' or method == 'stopTime':
            
            grayscale = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
            grayscale_3 = np.dstack((grayscale,grayscale,grayscale))

            output_image = np.where(binary_mask_3, image, grayscale_3)
            
        elif method == 'transparentBackground':
             
            output_image = np.dstack((image, binary_mask * 255))
            
        else:

            output_image = np.where(image,image,image)

        return output_image, (binary_mask_3 * 255).astype('uint8')

    def updateMethod(self, new_method):
        self.method = new_method

    def Capture(self, frame, choice):
        if self.method == 'stopTime':  ### We simply pass to skip the frame
            pass
        
        else:

            # Change the background of the frame.
            output_frame,_ = self.modifyBackground(frame, background_image = background_images[self.bg_img_index % len(background_images)],
                                                threshold = 0.3, method=choice)

            self.prev_choice = choice

            return output_frame
