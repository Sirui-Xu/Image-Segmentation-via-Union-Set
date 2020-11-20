import cv2
import re
import numpy as np
# In this code, I use cv2 to convert .ppm to .jpg instead of PIL.Image which could also be used.
def myImread_ppm(filename):
    with open(filename, 'rb') as f:
        image = f.read()
    # print(image[:2])

    # The magic number must match. 
    assert b'P6' == image[:2], "The image inputted (%s) doesn't have the right magic!" % filename
    
    # Find the basic information in the head of .ppm through regular expression.
    HeadPattern = re.compile(b'P(\d)\\n(\d+)\s(\d+)\\n(\d+)\\n')
    m = re.search(HeadPattern, image)
    image_width, image_height, max_color = int(m[2]), int(m[3]), int(m[4])
    # print(image_width, image_height, max_color)

    # Discard the head of .ppm through regular expression.
    HeadPattern = re.compile(b'(P\d\\n\d+\s\d+\\n\d+\\n)')
    head = re.match(HeadPattern, image)
    image = image.replace(head[0], b"")

    # create a matrix(numpy) to save the image
    # cv2 require image height in first dimension, width in second dimension.
    image_matrix = np.zeros((image_height, image_width, 3))
    for i in range(image_height):
        for j in range(image_width):
            r,g,b = image[:3]
            # It is worth mentioning that BGR channel arrangement is used in cv2, not RGB.
            image_matrix[i, j, :] = [int(b), int(g), int(r)]
            image = image[3:]
    return image_matrix

if __name__ == "__main__":
    image = myImread_ppm('./greens.ppm')
    cv2.imwrite('./greens_ppm2jpg.jpg', image)