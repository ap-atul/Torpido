import time

import cv2
import numpy as np

from lib.util.videoReader import VideoGet

MIN_CONFIDENCE = 0.5
WIDTH = 320
HEIGHT = 320

layerNames = ["feature_fusion/Conv_7/Sigmoid",
              "feature_fusion/concat_3"]

# imageFile = '/home/atul/Projects/Torpido/examples/text_sample1.jpeg'
# if os.path.isfile(imageFile):
#     print("File exists")

# video = cv2.VideoCapture("../examples/example1.mp4")
videoGetter = VideoGet("../examples/example4.mp4").start()
count = 0
while True:
    if videoGetter.stopped:
        videoGetter.stop()
        break

    image = videoGetter.frame

    if image is None:
        break

    count += 1
    # image = cv2.imread(imageFile)
    (H, W) = image.shape[:2]

    (newW, newH) = 320, 320
    rW = W / float(newW)
    rH = H / float(newH)

    image = cv2.resize(image, (newW, newH))
    orig = image
    (H, W) = image.shape[:2]

    if count % 200 == 0:

        net = cv2.dnn.readNet("/home/atul/Projects/Torpido/model/frozen_east_text_detection.pb")

        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94),
                                     swapRB=True, crop=False)
        start = time.time()
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        end = time.time()

        print(f"Shape of score {scores.shape}")
        print(f"[DATA] Average score :: {np.mean(scores)}")
        print(f"[INFO] Text detection took :: {end - start} s")

        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            for x in range(0, numCols):
                if scoresData[x] < MIN_CONFIDENCE:
                    continue
                confidences.append(scoresData[x])

        if np.mean(confidences) > 0.5:
            print("YES")

        print(f"Average confidence :: {np.mean(confidences)}")

    cv2.imshow("Text Detection", orig)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break

    # cv2.waitKey(0)
