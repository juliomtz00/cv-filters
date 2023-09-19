
# Julio Enrique Martinez Robledo
# Number: 578751
# Date: 21.02.2023
# Universidad de Monterrey


# Import libraries
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
    cv2.namedWindow('Output Image ('+str_title+')',cv2.WINDOW_NORMAL)

    #Visualize processed image
    cv2.imshow('Output Image ('+str_title+')',img_proc)

#Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_image',type=str,required=True)
parser.add_argument('--kernel_size',type=int,required=True)
parser.add_argument('--padding',type=str.lower,required=True,choices=["zero","replicate"])
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
    kernel = np.ones((args.kernel_size, args.kernel_size))/ (args.kernel_size**2)

    if args.padding in "zero":
        padded_img = np.pad(gimage, ((int(args.kernel_size)//2, int(args.kernel_size)//2), (int(args.kernel_size)//2, int(args.kernel_size)//2)), mode='constant', constant_values=0)        
        str_title = "Zero"
    elif args.padding in "replicate":
        padded_img = np.pad(gimage, ((int(args.kernel_size)//2, int(args.kernel_size)//2), (int(args.kernel_size)//2, int(args.kernel_size)//2)), mode='edge')
        str_title = "Replicate"

    # apply the filter to
    img_proc = np.zeros_like(img)
    for i in range(args.kernel_size//2,img.shape[0]-args.kernel_size//2):
        for j in range (args.kernel_size//2,img.shape[1]-args.kernel_size//2):
            img_proc[i-args.kernel_size//2,j-args.kernel_size//2] = np.sum(np.multiply(padded_img[i-args.kernel_size//2:i+(args.kernel_size//2 + 1), j-args.kernel_size//2:j+(args.kernel_size//2+1)],kernel))
    
    # save image if selected
    if args.save_output_image:
        #Save output image
        cv2.imwrite("output-image-"+str_title.lower()+".png",img_proc)

    # visualize images if selected
    if args.visualize:
        visualize_image(img,img_proc,str_title)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
