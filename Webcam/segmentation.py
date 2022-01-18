import os
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
from threading import Thread, Lock
background_images = []
        # Specify the path of the folder which contains the background images.
background_folder = './Webcam/backgrounds'
class WebcamEffects:

    def __init__(self, bg_img=None, blur=0.95, thresh=0.3, display = False, method = None, path_to_imgs = './backgrounds'):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segment = self.mp_selfie_segmentation.SelfieSegmentation(0)
        self.bg_img = bg_img
        self.blur = blur
        self.thresh = thresh
        self.display = display
        self.method = method

    def modifyBackground(self, image, background_image = 255, blur = 95, threshold = 0.3, display = True, method='changeBackground'):
        '''
        '''
        # Convert the input image from BGR to RGB format.
        RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # Perform the segmentation.
        result = self.segment.process(RGB_img)
        
        # Get a binary mask having pixel value 1 for the object and 0 for the background.
        # Pixel values greater than the threshold value will become 1 and the remainings will become 0.
        binary_mask = result.segmentation_mask > threshold
        
        # Stack the same mask three times to make it a three channel image.
        binary_mask_3 = np.stack((result.segmentation_mask,)*3, axis=-1) > threshold
        if method == 'changeBackground':
        
            # Resize the background image to become equal to the size of the input image.
            background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
    
            # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
            # value 1 and replace the other pixel values (where mask have zero) with the new background image.
            output_image = np.where(binary_mask_3, image, background_image)
            
        elif method == 'blurBackground':
            
            # Create a blurred copy of the input image.
            blurred_image = cv2.GaussianBlur(image, (blur, blur), 0)
    
            # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
            # value 1 and replace the other pixel values (where mask have zero) with the new background image.
            output_image = np.where(binary_mask_3, image, blurred_image)
        
        elif method == 'medianBlur':
            blurred_image = cv2.medianBlur(image, 33)
            output_image = np.where(binary_mask_3, blurred_image, image)

        elif method == 'boxFilter':
            box_img = cv2.boxFilter(image,-1, (33,33))
            output_image = np.where(binary_mask_3, box_img, image)

        elif method == 'desatureBackground' or method == 'stopTime':
            
            # Create a gray-scale copy of the input image.
            grayscale = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
    
            # Stack the same grayscale image three times to make it a three channel image.
            grayscale_3 = np.dstack((grayscale,grayscale,grayscale))
    
            # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
            # value 1 and replace the other pixel values (where mask have zero) with the new background image.
            output_image = np.where(binary_mask_3, image, grayscale_3)
            
        elif method == 'transparentBackground':
            
            # Stack the input image and the mask image to get a four channel image. 
            # Here the mask image will act as an alpha channel. 
            # Also multiply the mask with 255 to convert all the 1s into 255.  
            output_image = np.dstack((image, binary_mask * 255))
            
        else:
            # Display the error message.
            # Return
            output_image = np.where(image,image,image)
        
        # Check if the original input image and the resultant image are specified to be displayed.
        if display:
        
            # Display the original input image and the resultant image.
            plt.figure(figsize=[22,22])
            plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off')
            plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off')
        
        # Otherwise
        else:
            
            # Return the output image and the binary mask.
            # Also convert all the 1s in the mask into 255 and the 0s will remain the same.
            # The mask is returned in case you want to troubleshoot.
            return output_image, (binary_mask_3 * 255).astype('uint8')

    def updateMethod(self, new_method):
        self.method = new_method

    def Capture(self, frame, choice):
        # Initialize a list to store the background images.
        
        # Iterate over the images in the background folder.
        for img_path in os.listdir(background_folder):
            
            # Read a image.
            image = cv2.imread(f"{background_folder}/{img_path}")
            
            # Append the image into the list.
            background_images.append(image)
        
        # Initialize a variable to store the index of the background image.
        bg_img_index = 0
        
        if self.method == 'stopTime':
            pass
        
        else:# Check if frame is not read properly.
            
                # Flip the frame horizontally for natural (selfie-view) visualization.

                # Change the background of the frame.
            output_frame,_ = self.modifyBackground(frame, background_image = background_images[bg_img_index % len(background_images)],
                                                threshold = 0.3, display = False, method=choice)
                
            return output_frame
