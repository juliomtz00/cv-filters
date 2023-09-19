#Import libraries
import numpy as np
import cv2
import sys
import argparse

#Create function to visualize images
def visualize_image(img,img_proc,str_title):

    #Create a new window for visualization purposes
    cv2.namedWindow('Input Image', cv2.WINDOW_NORMAL)

    #Visualize input image
    cv2.imshow('Input Image',img)

    #Create a new window for visualization purposes
    cv2.namedWindow('Output Image ('+str_title+')',cv2.WINDOW_NORMAL)

    #Visualize processed image
    cv2.imshow('Output Image ('+str_title+')',img_proc)

#Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_image',type=str,required=True)
parser.add_argument('--transformation',type=str.lower,required=True,choices=["negative","log","gamma"])
parser.add_argument('--save_output_image',type=int,default=0, required=False)
parser.add_argument('--visualize',type=int,default=1, required=False)
args = parser.parse_args()

#Read input image
img = cv2.imread(args.input_image)

if img is None: 
    print("Sorry, image could not be read.")
    sys.exit(-1)
    
else:
    #Process input image
    if args.transformation.lower() in "negative":
        #Negative
        img_negative = 255 - img
        img_proc = img_negative
        str_title = 'Negative'

    elif args.transformation.lower() in "log": 
        #Log
        c = 100
        rm = img/255
        img_log = c*np.log(1+rm)
        img_proc = np.uint8((255/(np.max(img_log)-np.min(img_log)))*(img_log-np.min(img_log)))
        str_title = 'Log'

    elif args.transformation.lower() in "gamma":
        #Gamma
        c = 1
        gamma_value = 0.4
        rn = img/255
        img_gamma = c*(rn**gamma_value)
        img_proc = np.uint8((255/(np.max(img_gamma)-np.min(img_gamma)))*(img_gamma-np.min(img_gamma)))
        str_title = 'Gamma'

    if args.save_output_image:
        #Save output image
        cv2.imwrite("output-image-"+str_title.lower()+".png",img_proc)

    if args.visualize:
        visualize_image(img,img_proc,str_title)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
