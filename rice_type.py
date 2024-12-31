import cv2
import time
import numpy as np

prev_time_frame = 0
new_time_frame = 0
video = cv2.VideoCapture('priya.avi')


def contour(img, orig_img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # calculate contour area and perimeter

        # calculate aspect ratio and roundness
        x, y, w, h = cv2.boundingRect(cnt)
        rect = cv2.minAreaRect(cnt)
        length = rect[1][0]
        width = rect[1][1]
        length1 = max(length, width)
        width1 = min(length, width)

        if x > 50 and x < 600 and y > 20 and y < 600:
            # classify based on shape and size
            if length1 < 122 and length1 > 82 and width1 < 26 and width1 > 20:
                cv2.drawContours(orig_img, [cnt], 0, (0, 255, 0), 2)
                cv2.putText(orig_img, "basmathi  grain", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif length1 < 68 and length1 > 48 and width1 < 35 and width1 > 31:
                cv2.drawContours(orig_img, [cnt], 0, (0, 0, 255), 2)
                cv2.putText(orig_img, " indian rice", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            else:
                cv2.drawContours(orig_img, [cnt], 0, (255, 0, 0), 2)
                cv2.putText(orig_img, "brown rice", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


while True:
    # Reading of the Video
    ret, img = video.read()
    img = cv2.resize(img, (700, 500))

    # Converting to GrayScale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    retval, threshold = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    threshold = cv2.filter2D(threshold, -1, kernel_sharpening)

    # Apply erosion and dilation to remove noise and fill in gaps
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(threshold, kernel, iterations=2)
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    contour(thresh, img)
    cv2.imshow("Live", img)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and destroy all windows
video.release()
cv2.destroyAllWindows()
