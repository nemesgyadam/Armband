import cv2
import numpy as np

from math import atan2, cos, sin, sqrt, pi


def get_green_contour(img, settings):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(
        hsv, settings["green_limit_low"], settings["green_limit_high"]
    )
    #cv2.imshow('green mask', green_mask)

    cnts, hierarchy = cv2.findContours(
        green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if len(cnts) == 0:
        return None
    return max(cnts, key=cv2.contourArea)


def get_black_contour(img, settings):
    """
    Return the contour of the
    biggest black part of the image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lower = np.uint8([0])
    upper = np.uint8([settings["black_upper_limit"]])
    img = cv2.inRange(img, lower, upper)
    cv2.imshow('black', img)
    img = cv2.GaussianBlur(img, (settings["gauss_blur"], settings["gauss_blur"]), 0)
    # cv2.imshow('gauss', img)

    kernel = np.ones((settings["dilate_kernel"], settings["dilate_kernel"]), np.uint8)
    img = cv2.dilate(img, kernel, iterations=settings["dilate_iterations"])
    #cv2.imshow("dilate", img)
    # kernel = np.ones((5,5),np.uint8)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('morpholgy', img)
    cnts, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        return max(cnts, key=cv2.contourArea)
    except:
        #print("No contours found")
        return None


def get_angle_box(cnt, img):
    rect = cv2.minAreaRect(cnt)
    (x, y), (h, w), angle = rect
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    if w < h:
        angle += 180
    else:
        angle += 90

    return angle


def countour2angle(cnt, frame, settings):
    if settings["angle_method"].lower() == "pca":
        angle = get_angle_PCA(cnt, frame)
    elif settings["angle_method"].lower() == "box":
        angle = get_angle_box(cnt, frame)
    else:
        raise Exception("Unknown angle method")
    return angle


def center(cnt):
    """
    Calculate the center of a contour
    """
    moments = cv2.moments(cnt)
    if max(moments.values()) < 0.1:
       # print("No green found")
        return None
    cX = int(moments["m10"] / moments["m00"])
    cY = int(moments["m01"] / moments["m00"])
    return cX, cY


def drawAxis(img, p_, q_, color, scale):
    p = list(p_)
    q = list(q_)

    ## [visualization1]
    angle = atan2(p[1] - q[1], p[0] - q[0])  # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)


def get_angle_PCA(countour, img):
    sz = len(countour)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = countour[i, 0, 0]
        data_pts[i, 1] = countour[i, 0, 1]

    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians

    label = "  Rotation Angle: " + str(-int(np.rad2deg(angle)) - 90) + " degrees"

    # DRAW ANGLE
    cntr = (int(mean[0, 0]), int(mean[0, 1]))
    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    angle_size = 0.2
    p1 = (
        cntr[0] + angle_size * eigenvectors[0, 0] * eigenvalues[0, 0],
        cntr[1] + angle_size * eigenvectors[0, 1] * eigenvalues[0, 0],
    )
    drawAxis(img, cntr, p1, (255, 255, 0), 1)

    return -int(np.rad2deg(angle)) - 90


def draw_center(image, position, color=(0, 255, 0)):
    cv2.circle(image, position, 10, (0, 255, 0), 1)


def draw_center_kalman(image, position, color=(0, 255, 0)):
    cv2.circle(image, position, 5, (0, 255, 0), -1)
