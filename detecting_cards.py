#!/usr/bin/env python2

import cv2
import numpy as np

#in set there are 9 cards at a time
numcards = 9

#This at first removes all the unimportant details to focus on the cards.
#full_set_bbg2 is the better image with the whole set
img = cv2.imread('imgs/full_set_bbg2.jpg')
img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

#Next we look at the actual shape of the objects in the cards.
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]

#Next we try to add a rectangle around the cards to recognize the cards
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

    #This will ensure that any card that is not perfectly rectangular will be made rectangular
    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
    transform = cv2.getPerspectiveTransform(dl,h)
    warp = cv2.warpPerspective(img,transform,(450,450))

    cv2.imshow('image',warp)
    cv2.waitKey(0)
