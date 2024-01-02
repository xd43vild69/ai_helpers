import cv2
import numpy as np
import os
import sys
from glob import glob
from tkinter import filedialog

class Normalizer:

    output_dir = ""

    def __init__(self, name):
        # Ask user to select input directory
        print("Please select the source directory...")
        
        input_dir = filedialog.askdirectory(title="Select source directory")
        self.output_dir = input_dir + '_n_' + name

        # If output directory does not exist, create it
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.process(input_dir)

    def process(self, input_dir):

        # Process images in input directory
        image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
        image_paths = []
        for format in image_formats:
            image_paths.extend(glob(os.path.join(input_dir, format)))
        
        print("Processing images...")
        try:
            # Loop through all image files in the input directory
            for image_path in image_paths:
                print(f"Processing image: {image_path}")
                image = cv2.imread(image_path)
                self.square_image_768(image, image_path)

            print("Data normalization completed.")

        except KeyboardInterrupt:
            print("Data normalization interrupted by the user.")
            sys.exit(0)

    def square_image_768(self, img, image_path, size=(768,768)):

        original_image_path = os.path.join(self.output_dir, f"orig_{os.path.splitext(os.path.basename(image_path))[0]}.png")    
        h, w = img.shape[:2]
        c = img.shape[2] if len(img.shape)>2 else 1

        if h == w: 
            resized =cv2.resize(img, size, cv2.INTER_AREA)
            cv2.imwrite(original_image_path, resized)
            return

        dif = h if h > w else w

        interpolation = cv2.INTER_AREA if dif > (size[0]+size[1])//2 else cv2.INTER_CUBIC

        x_pos = (dif - w)//2
        y_pos = (dif - h)//2

        if len(img.shape) == 2:
            mask = np.zeros((dif, dif), dtype=img.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
        else:
            mask = np.zeros((dif, dif, c), dtype=img.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
        
        width = 768
        height = 768
        dim = (width, height)

        resized = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA)

        cv2.imwrite(original_image_path, resized)


    
    
        
