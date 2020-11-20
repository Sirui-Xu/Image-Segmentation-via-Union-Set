import cv2
import re
import numpy as np
# In this code, I use cv2 to convert .pgm to .jpg instead of PIL.Image which could also be used.
def myImread_pgm(filename):
    with open(filename, 'rb') as f:
        image = f.read()
    # print(image[:2])

    # The magic number must match. 
    assert b'P5' == image[:2], "The image inputted (%s) doesn't have the right magic!" % filename
    
    # Find the basic information in the head of .pgm through regular expression.
    HeadPattern = re.compile(b'P(\d)\\n(\d+)\s(\d+)\\n(\d+)\\n')
    m = re.search(HeadPattern, image)
    image_width, image_height, max_color = int(m[2]), int(m[3]), int(m[4])
    # print(image_width, image_height, max_color)

    # Discard the head of .pgm through regular expression.
    HeadPattern = re.compile(b'(P\d\\n\d+\s\d+\\n\d+\\n)')
    head = re.match(HeadPattern, image)
    image = image.replace(head[0], b"")

    # create a matrix(numpy) to save the image
    # cv2 require image height in first dimension, width in second dimension.
    image_matrix = np.zeros((image_height, image_width))
    for i in range(image_height):
        for j in range(image_width):
            value = image[0]
            # calculate the value of the pixel
            image_matrix[i, j] = value
            image = image[1:]
    return image_matrix

if __name__ == "__main__":
    
    image = myImread_pgm('./greens.pgm')
    cv2.imwrite('./greens_pgm2jpg.jpg', image)