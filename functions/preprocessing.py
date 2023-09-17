
import numpy as np
import cv2
def preprocessing(image):
    # load the image as grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg = np.average(gray)
    # Change all pixels to black or white
    gray[gray > 185] = 254
    gray[gray <= 185] = 1
    gray[gray ==1] = 255
    gray[gray ==254] = 0

    # Scale it 10x
    scaled = cv2.resize(gray, (0, 0), fx=20, fy=20, interpolation=cv2.INTER_CUBIC)
    # io.imshow(scaled)

    # Retained your bilateral filter
    filtered = cv2.bilateralFilter(scaled, 11, 17, 17)

    # Thresholded OTSU method
    #thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Erode the image to bulk it up for tesseract
    kernel = np.ones((5, 5), np.uint8)
    final = cv2.erode(filtered, kernel, iterations=2)

    return final
