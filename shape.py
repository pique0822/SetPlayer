import cv2
import numpy as np
from CardFinder import CardFinder

def invert(imagem):
    imagem = (255-imagem)
    return imagem
#need the image of the card face
def color_of_image(img):

    lower = np.array([120, 120, 120])
    upper = np.array([255, 255, 255])
    shapeMask = cv2.inRange(img, lower, upper)
    shapeMask = invert(shapeMask)

    (cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

    """
    cv2.imshow("image",shapeMask)
    cv2.waitKey(0)
    """

    for c in cnts:

        drawing = shapeMask.copy()
        cv2.drawContours(drawing,[c],0,(255,255,255),2)
        cv2.imshow("image",drawing)
        cv2.waitKey(0)

        epsilon = 0.01*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)

        print len(approx)
        if len(approx) == 4:
            print "Diamond"
        elif len(approx) == 2:
            print "Squiggle"
        elif len(approx) == 1:
            print "Oval"
        else:
            print "Unidentified Shape"


finder = CardFinder()
""" Works great for these images just make sure to change numCards in CardFinder
diam = cv2.imread('imgs/green_diamond.jpg')
print color_of_image(diam)

sshape = finder.find_cards(cv2.imread('imgs/bbg_s_red.jpg'))[0]
print color_of_image(sshape)

oval = finder.find_cards(cv2.imread('imgs/bbg_purple_oval.jpg'))[0]
print color_of_image(oval)
"""
images = finder.find_cards(cv2.imread('imgs/full_set_bbg2.jpg'))
print len(images)
for img in images:
    print color_of_image(img)
    cv2.imshow("image",img)
    cv2.waitKey(0)
    print ""
