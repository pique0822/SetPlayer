import cv2
import numpy as np
import CardFinder

error = 2

def invert(imagem):
    imagem = (255-imagem)
    return imagem
#need the image of the card face
def shape_of_image(img):

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

    contours = []
    for c in cnts:

        """drawing = shapeMask.copy()
        cv2.drawContours(drawing,[c],0,(255,255,255),2)
        cv2.imshow("image",drawing)
        cv2.waitKey(0)"""

        epsilon = 0.005*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)

        contours.append(len(approx))

    contours = sorted(contours)

    actual_contours = []
    for i in range(len(contours)-1):
        if not abs(contours[i]-contours[i+1]) >= error:
            actual_contours.append(contours[i])
    actual_contours.append(contours[len(contours)-1])
    contour_avg = sum(actual_contours)/len(actual_contours)

    if contour_avg == 4:
        return "Diamond"
    elif 4 < contour_avg < 15:
        return "Oval"
    elif 15 <= contour_avg <= 22:
        return "Squiggle"
    else:
        return "Unidentified Shape"



""" Works great for these images just make sure to change numCards in CardFinder
diam = cv2.imread('imgs/green_diamond.jpg')
print color_of_image(diam)

sshape = finder.find_cards(cv2.imread('imgs/bbg_s_red.jpg'))[0]
print color_of_image(sshape)

oval = finder.find_cards(cv2.imread('imgs/bbg_purple_oval.jpg'))[0]
print color_of_image(oval)
"""
images = CardFinder.find_cards(cv2.imread('imgs/twelve_set_wood2.jpg'))# doesnt work for wood1 for wood 2 it only misses 2
for img in images:
    print shape_of_image(img)
    cv2.imshow("image",img)
    cv2.waitKey(0)
