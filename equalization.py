#Entered command example must be python3 equalization.py --input_image city.tif --equalization global --save_output_image 0  --visualize 1

#Import libraries
import numpy as np
import cv2
import sys
import argparse

def visualize_image(img,img_proc,str_title):

    #Create a new window for visualization purposes
    cv2.namedWindow('Input Image', cv2.WINDOW_NORMAL)

    #Visualize input image
    cv2.imshow('Input Image',img)

    #Create a new window for visualization purposes
    cv2.namedWindow('Equalized Image ('+str_title+')',cv2.WINDOW_NORMAL)

    #Visualize processed image
    cv2.imshow('Equalized Image ('+str_title+')',img_proc)

#Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_image',type=str,required=True)
parser.add_argument('--equalization',type=str.lower,required=True,choices=["local","global"])
parser.add_argument('--save_output_image',type=int,default=0, required=False)
parser.add_argument('--visualize',type=int,default=1, required=False)
args = parser.parse_args()

#Read input image
img = cv2.imread(args.input_image)

if img is None: 
    print("Sorry, image could not be read.")
    sys.exit(-1)

else:

    #Image in grayscale
    gimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if args.equalization in "local":
        #Size of neighborhood
        s = 32

        #process of local histogram equalization
        cl = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(s,s))
        img_local = cl.apply(gimage)
        img_proc = img_local.copy()
        str_title = "Local"
    
    elif args.equalization in "global":
        #Calculate histogram 
        histo, bins = np.histogram(gimage.flatten(),256,[0,256])

        #Cumulative distribution function
        cdf = histo.cumsum()

        #Intensity values to new values using Cumulative distribution function
        cdfMap = np.ma.masked_equal(cdf,0)
        cdfMap = (cdfMap - cdfMap.min())*255/(cdfMap.max()-cdfMap.min())
        cdf = np.ma.filled(cdfMap,0).astype('uint8')
        img_global = cdf[gimage]
        img_proc = img_global.copy()
        str_title = "Global"

    if args.save_output_image:
        #Save output image
        cv2.imwrite("equalized-image-"+str_title.lower()+".png",img_proc)

    if args.visualize:
        visualize_image(img,img_proc,str_title)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

