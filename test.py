import CardFinder
import cv2
import numpy as np

#cf = CardFinder()
#img = cv2.imread('imgs/full_set.jpg')
img = cv2.imread('imgs/twelve_set_wood1.jpg')
for im in CardFinder.find_cards(img):
    cv2.imshow('image',im)
    cv2.waitKey(0)
