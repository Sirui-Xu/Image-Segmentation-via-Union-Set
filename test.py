from graph import segment
import numpy as np
import argparse
import cv2
import time
import os
from random import random

# 根据生成的segmentation进行可视化
def generate_color(mask):
    len_nodes = len(set(mask.flatten()))
    print("image segmentation has {} nodes.".format(len_nodes))
    color = [np.array([int(random()*255), int(random()*255), int(random()*255)]) for i in range(len_nodes)]
    mask_color = np.zeros((mask.shape[0], mask.shape[1], 3))
    for y in range(mask_color.shape[0]):
        for x in range(mask_color.shape[1]):
            mask_color[y, x, :] = color[int(mask[y, x])]
    return mask_color

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Segmentation based on Union Find')
    parser.add_argument('--sigma', type=float, default=1.0, 
                        help='var for the Gaussin Filter')
    parser.add_argument('--ksize', type=int, default=5, 
                        help='kernel size for the Gaussin Filter')
    parser.add_argument('--neighbor', type=int, default=8, choices=[4, 8],
                        help='choose the neighborhood format, 4 or 8')
    parser.add_argument('--K', type=float, default=1, 
                        help='a constant to control the threshold function of the predicate')
    parser.add_argument('--phi', type=float, default=0, 
                        help='a constant to balance between values and coordinates')
    parser.add_argument('--min_comp_percent', type=float, default=0.01, 
                        help='a constant to remove all the components with fewer percentage of pixels')
    parser.add_argument('--input_dir', type=str, default="./assets/images/", 
                        help='the file path of the input images')
    parser.add_argument('--output_dir', type=str, default="./assets/segmentations/", 
                        help='the file path of the output images')
    parser.add_argument('--concate_dir', type=str, default="./assets/concate_images/", 
                        help='the file path of the output concated images')
    
    args = parser.parse_args()
    print("##### Parameters settings #####")
    print("Gaussian blur kernel size: " + str(args.ksize))
    print("Gaussian blur kernel variance: " + str(args.sigma))
    print("The number of edges for a pixel: " + str(args.neighbor))
    print("K = " + str(args.K), end=" ")
    print("Phi = " + str(args.phi))
    print("fewerest percentage of one component: " + str(args.min_comp_percent))

    image_paths = os.listdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.concate_dir, exist_ok=True)
    image_paths.remove(".DS_Store")
    for image_path in image_paths:      
        image = cv2.imread(os.path.join(args.input_dir, image_path))
        print("image name: ", image_path)
        
        start_time = time.time()
        segmentation = segment(image, sigma=args.sigma, min_percent=args.min_comp_percent, num_neighbor=args.neighbor, K=args.K, phi=args.phi)
        end_time = time.time()
        print("time passed by: {} s".format(end_time - start_time))
        segmentation_color = generate_color(segmentation)
        
        cv2.imwrite(os.path.join(args.output_dir, image_path), segmentation_color)
        image_concate = np.concatenate([image, segmentation_color], axis=1)
        cv2.imwrite(os.path.join(args.concate_dir, image_path), image_concate)
