import cv2
import numpy as np

cap = cv2.VideoCapture(0)

rect_blue = (0, 0, 100, 100)
rect_green = (0, 100, 100, 200)

game = False
color_paint = -1
painting = []


def rectContains(rect, pt):
    logic = rect[0] < pt[0] < rect[0] + rect[2] and rect[1] < pt[1] < rect[1] + rect[3]
    return logic


while True:
    tet, frame = cap.read()

    # smoothing filter
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    # flip the frame horizontally
    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (rect_blue[0], rect_blue[1]), (rect_blue[2], rect_blue[3]), (255, 0, 0), 2)
    cv2.rectangle(frame, (rect_green[0], rect_green[1]), (rect_green[2], rect_green[3]), (0, 255, 0), 2)

    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([94, 80, 2])
    higher_blue = np.array([126, 255, 255])

    lower_green = np.array([40, 56, 4])
    higher_green = np.array([90, 255, 255])

    # getting the range of blue color in frame
    blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_range)
    blue_s_gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
    canny_edge_blue = cv2.Canny(blue_s_gray, 50, 240)

    # getting the range of green color in frame
    green_range = cv2.inRange(hsv, lower_green, higher_green)
    res_green = cv2.bitwise_and(frame, frame, mask=green_range)
    green_s_gray = cv2.cvtColor(res_green, cv2.COLOR_BGR2GRAY)
    canny_edge_green = cv2.Canny(green_s_gray, 50, 240)

    # applying HoughCircles
    circles_blue = cv2.HoughCircles(canny_edge_blue, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=10, param2=20,
                                    minRadius=20, maxRadius=40)
    circles_green = cv2.HoughCircles(canny_edge_green, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=10, param2=20,
                                     minRadius=20, maxRadius=40)

    if game == False and circles_blue is not None:
        for i in circles_blue[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

            # center
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

            if game == False and rectContains(rect_blue, (i[0], i[1])):
                game = True
                color_paint = 1
            elif game == False and rectContains(rect_green, (i[0], i[1])):
                game = True
                color_paint = 2
            break

    if game == True and circles_green is not None:
        for i in circles_green[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

            # center
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            painting.append((i[0],i[1]))
            break

    for i in painting:
        if color_paint == 1:
            cv2.circle(frame, (i[0], i[1]), 2, (255, 0, 0), 5)
        if color_paint == 2:
            cv2.circle(frame, (i[0], i[1]), 2, (0, 255, 0), 5)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
