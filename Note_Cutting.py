

import cv2
import numpy as np
import os
import sys
import glob
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patches as patches


# identify the interval of the notes using pixel count and vertical projection
def identify_interval(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3,3), np.uint8)
    img_median1 = cv2.medianBlur(im_bw, 3, 3)
    #img_erosion = cv2.erode(img_median1, kernel, iterations=2)
    #img_erosion1 = cv2.dilate(img_erosion, kernel, iterations=4)
    #img_median = cv2.medianBlur(img_erosion1, 3, 3)

    img_erosion2 = cv2.dilate(img_median1, kernel, iterations=2)
    img_erosion3 = cv2.erode(img_erosion2, kernel, iterations=2)

    cv2.imshow('img',img_erosion3)
    cv2.waitKey(100000)
    # find the peaks
    vertical_projection = np.sum(img_erosion3, axis=0)
    vertical_projection = vertical_projection / 255
    print(vertical_projection)
    peaks = find_peaks(vertical_projection)


    return peaks


# find the peaks
def find_peaks(vertical_projection):

    peaks = []
    for i in range(1, len(vertical_projection) - 1):
     if vertical_projection[i]>0:
         if vertical_projection[i]-vertical_projection[i-1]>1 :
            peaks.append(i)
         elif vertical_projection[i]-vertical_projection[i+1]>1 :
           peaks.append(i)


    return peaks





# After finding the location ( interval ) they should be cropped for further use.
def crop_notes(img, peaks):
    # create a list to store the cropped notes
    cropped_notes = []
    # loop through the intervals
    for i in range(0,len(peaks)-1,2):
        # get the interval

        # get the height and width of the image
        height, width = img.shape[:2]

        # get the start and end points of the interval
        start_point = int(peaks[i])-5
        end_point = int(peaks[i+1])+5
        # get the start and end points of the interval
        start_interval = int(start_point)
        end_interval = int(end_point)


        # crop the note
        cropped_note = img[0:height,start_interval:end_interval]
        # append the cropped note to the list
        cropped_notes.append(cropped_note)


    return cropped_notes


# main function
def main():
    output_path = 'C:\\Users\\user\\OneDrive\\Desktop\\Notes\\'
    # get the current directory
    input_path = 'C:\\Users\\user\\OneDrive\\Desktop\\nn\\'
    # get the images in the current directory
    images = glob.glob(input_path + "/*.png")
    # get the number of images
    no_of_images = len(images)
    # create a list to store the cropped notes
    cropped_notes = []
    # loop through the images and crop the notes
    for i in range(no_of_images):
        img = cv2.imread(images[i])
        intervals = identify_interval(img)

        cropped_notes.append(crop_notes(img, intervals))



    # save the cropped notes


    for i in range(no_of_images):
        for j in range(len(cropped_notes[i])):
            cv2.imwrite(output_path+str(i) + "_" + str(j) + ".jpg", cropped_notes[i][j])
    # close the program
    sys.exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)

