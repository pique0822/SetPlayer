import cv2
import numpy as np

def find_cards(img):
    numcards = 9

    img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # define range of color that defines the background to filter out
    lower_table = np.array([8,20,10])
    upper_table = np.array([22,255,255])
    # threshold the HSV image to indentify which pixels are table
    mask = cv2.inRange(hsv, lower_table, upper_table)
    mask_inv = cv2.bitwise_not(mask)
    # use the mask to black out any pixel that is the table
    res = cv2.bitwise_and(img,img, mask= mask_inv)

    # useful when testing new background filters
    # cv2.imshow("s",res)
    # cv2.waitKey(0)

    thresh = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

    # Next we look at the actual shape of the objects in the cards.
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]

    ret = []

    # Next we try to add a rectangle around the cards to recognize the cards
    for i in range(numcards):
        card = contours[i]
        peri = cv2.arcLength(card,True)
        approx = cv2.approxPolyDP(card,0.02*peri,True)
        rect = cv2.minAreaRect(contours[i])
        r = cv2.cv.BoxPoints(rect)

        ap = []
        for l in approx[0:4]:
            ap.append(l[0])
        dl = np.array(ap,np.float32)

        # This will ensure that any card that is not perfectly rectangular will be made rectangular
        h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
        transform = cv2.getPerspectiveTransform(dl,h)
        warp = cv2.warpPerspective(img,transform,(450,450))

        ret.append(warp)
    return ret

# example usage
if __name__ == "__main__":
    # img = cv2.imread('imgs/full_set_bbg2.jpg') # doesn't work with this cardfinder filtering out table
    img = cv2.imread('imgs/full_set.jpg')
    for im in find_cards(img):
        cv2.imshow('image',im)
        cv2.waitKey(0)
