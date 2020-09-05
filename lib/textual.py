import os
import time

import cv2
import numpy as np

MIN_CONFIDENCE = 0.005
WIDTH = 320
HEIGHT = 320

imageFile = '/home/atul/Projects/Torpido/examples/sample.png'
if os.path.isfile(imageFile):
    print("File exists")

# video = cv2.VideoCapture(0)
# while True:
#     _, image = video.read()
#
#     if image is None:
#         break

image = cv2.imread(imageFile)
orig = image
(H, W) = image.shape[:2]

(newW, newH) = 320, 320
rW = W / float(newW)
rH = H / float(newH)

image = cv2.resize(image, (newW, newH))
(H, W) = image.shape[:2]

layerNames = ["feature_fusion/Conv_7/Sigmoid",
              "feature_fusion/concat_3"]
net = cv2.dnn.readNet("/home/atul/Projects/Torpido/model/frozen_east_text_detection.pb")

blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94),
                             swapRB=True, crop=False)
start = time.time()
net.setInput(blob)
(scores, geometry) = net.forward(layerNames)
end = time.time()

print(f"[INFO] Text detection took :: {end - start} s")

(numRows, numCols) = scores.shape[2:4]
rects = []
confidences = []

for y in range(0, numRows):
    scoresData = scores[0, 0, y]
    # xData0 = geometry[0, 0, y]
    # xData1 = geometry[0, 1, y]
    # xData2 = geometry[0, 2, y]
    # xData3 = geometry[0, 3, y]
    # anglesData = geometry[0, 4, y]

    for x in range(0, numCols):
        # if scoresData[x] < MIN_CONFIDENCE:
        #     continue

        # (offsetX, offsetY) = (x * 4.0, y * 4.0)
        #
        # angle = anglesData[x]
        # cos = np.cos(angle)
        # sin = np.sin(angle)
        #
        # h = xData0[x] + xData2[x]
        # w = xData1[x] + xData3[x]
        #
        # endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
        # endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
        # startX = int(endY - w)
        # startY = int(endX - h)
        #
        # rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])

    # boxes = non_max_suppression(np.array(rects), probs=confidences)

    # for(startX, startY, endX, endY) in boxes:
        # startX = int(startX * rW)
        # startY = int(startY * rH)
        # endX = int(endX * rW)
        # endY = int(endY * rH)
        #
        # cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

print(np.mean(confidences))
# cv2.imshow("Text Detection", orig)
# key = cv2.waitKey(1) & 0xFF


