import cv2
import re
import numpy as np
# In this code, I use cv2 to convert .pbm to .jpg instead of PIL.Image which could also be used.
def myImread_pbm(filename):
    with open(filename, 'rb') as f:
        image = f.read()
    # print(image[:2])

    # The magic number must match. 
    assert b'P4' == image[:2], "The image inputted (%s) doesn't have the right magic!" % filename
    
    # Find the basic information in the head of .pbm through regular expression.
    HeadPattern = re.compile(b'P(\d)\s+(\d+)\s(\d+)\\n')
    m = re.search(HeadPattern, image)
    image_width, image_height = int(m[2]), int(m[3])
    # print(image_width, image_height)

    # Discard the head of .pbm through regular expression.
    HeadPattern = re.compile(b'(P\d\s+\d+\s\d+\\n)')
    head = re.match(HeadPattern, image)
    image = image.replace(head[0], b"")
    # create a matrix(numpy) to save the image
    # cv2 require image height in first dimension, width in second dimension.
    image_matrix = np.zeros((image_height, image_width))
    for i in range(image_height):
        for j in range(image_width):
            # Calculate the bit
            value = (image[((image_width+7) // 8) * i + j // 8] >> (7 - (j % 8))) % 2
            image_matrix[i, j] = (value ^ 1) * 255
    return image_matrix

if __name__ == "__main__":
    image = myImread_pbm('./greens.pbm')
    cv2.imwrite('./greens_pbm2jpg.jpg', image)

    # pbm from matlab
    image = myImread_pbm('./greens_.pbm')
    cv2.imwrite('./greens_pbm2jpg_.jpg', image)