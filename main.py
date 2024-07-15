import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0) #"Resources/Videos/1.mp4"
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
print(listShirts)
fixedRatio = 270/190 #widthOfShirt/widthOfPoint11to12
shirtRatioWidthHeight = 581/440 #height/width
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findPose(img)

    lmList, bbox = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0]-lm12[0])*fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioWidthHeight)))
        currentScale = (lm11[0]-lm12[0])/190
        offset = int(44*currentScale), int(48*currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0], lm12[1]-offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight,(1725, 450))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 450))

        if lmList[15][0] > 1500:
            counterRight += 1
            cv2.ellipse(img, (1790, 510), (66, 66), 0, 0,
                        counterRight*selectionSpeed, (0, 255, 0), 20)    #135, 510
            if counterRight*selectionSpeed > 360:
                counterRight = 0
                if(imageNumber < len(listShirts)-1):
                    imageNumber += 1
        elif lmList[16][0] < 400:
            counterLeft +=1
            cv2.ellipse(img, (135, 510), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)  # 135, 510
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if (imageNumber > 0):
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    imgShirt = cv2.flip(imgShirt, 1)
    cv2.waitKey(1)