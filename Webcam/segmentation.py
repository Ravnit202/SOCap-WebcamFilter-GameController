import os
import cv2
import numpy as np
import mediapipe as mp

background_images = []
# Store the path to the background images.
background_folder = './images/backgrounds'

class WebcamEffects:

    def __init__(self, bg_img=None, blur=0.95, thresh=0.3, method = None):
        #load mediapipe libraries/solutions
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segment = self.mp_selfie_segmentation.SelfieSegmentation(0)

        self.bg_img = bg_img
        self.blur = blur
        self.thresh = thresh
        self.method = method
        self.prev_choice = None
        
        #Handle multiple bg images
        for img_path in os.listdir(background_folder):

            image = cv2.imread(f"{background_folder}/{img_path}")

            background_images.append(image)

        self.bg_img_index = 1

    def applyFilter(self, image, background_image = 255, blur = 95, threshold = 0.35, method='changeBackground'):

        # Convert the image from BGR to RGB
        RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #Process the image to segment out the user
        result = self.segment.process(RGB_img)
        segmented = result.segmentation_mask
        
        binary_mask_3 = np.stack((segmented,)*3, axis=-1) > threshold
        
        #Replace the background
        if method == 'changeBackground':
            background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
            output_image = np.where(binary_mask_3, image, background_image)

        #Blur the background
        elif method == 'blurBackground':
            blurred_image = cv2.GaussianBlur(image, (blur, blur), 0)
            output_image = np.where(binary_mask_3, image, blurred_image)
        
        #Blur the user and not the background
        elif method == 'boxFilter':
            box_img = cv2.boxFilter(image,-1, (33,33))
            output_image = np.where(binary_mask_3, box_img, image)

        #Remove colour from the background
        elif method == 'desatureBackground':
            
            grayscale = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
            grayscale_3 = np.dstack((grayscale,grayscale,grayscale))

            output_image = np.where(binary_mask_3, image, grayscale_3)
            
        #Create a clone of the user
        elif method == 'cloneUser':
            M = np.float32([[1, 0, -400], [0, 1, -0]])

            shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
            shifted_mask = cv2.warpAffine(segmented, M, (segmented.shape[1], segmented.shape[0]))
            mask_3 = np.stack((shifted_mask,)*3, axis=-1) > threshold

            output_image = np.where(mask_3, shifted, image)
            
        #Return the original image
        else:

            output_image = np.where(image,image,image)

        return output_image, (binary_mask_3 * 255).astype('uint8')

    def updateMethod(self, new_method):
        self.method = new_method 

    def Capture(self, frame, choice):

        # Change the background of the frame.
        output_frame,_ = self.applyFilter(frame, background_image = background_images[self.bg_img_index % len(background_images)],
                                            threshold = 0.30, method=choice)

        self.prev_choice = choice #Store the previous choice

        return output_frame
