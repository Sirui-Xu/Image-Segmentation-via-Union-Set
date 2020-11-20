# we can use chardet to jugde the encoding format of a binary file.
import chardet
import re
with open('./greens.ppm', 'rb') as f:
    image = f.read()
    encodingFormat = chardet.detect(image)['encoding']
    print(encodingFormat)
    with open('./greensppm.txt', 'w') as g:
        g.write(str(image))

# Unfortunately, chardet could not get the true answer.
# outputs: {'encoding': None, 'confidence': 0.0, 'language': None}.

# Hopefully, I got it from website, where it is said that there is a magic number 
# in the head of this file to point out its encoding format.
# For this .ppm file, the magic number is p6(you can check it out in greenspm.txt).
# So the encoding format must be 'Binary'

# We can still evaluate our judgement through chardet
# By using re module
with open('./greens.ppm', 'rb') as f:
    imageStr = str(f.read())
    # print(imageStr[:20])
    # I want to match the head of .ppm file, you can check the structure of .ppm file
    # in my report in detail.
    pattern = re.compile(r'P(\d)\\n(\d+)\s(\d+)\\n(\d+)\\n(.*)')
    # print(pattern)
    m = re.search(pattern, imageStr)
    # print(m)
    print('The magic number is P{}'.format(m[1]))
    print('The size of this image is {}*{}'.format(m[2], m[3]))
    print('The range of value of all pixel is ' + m[4])