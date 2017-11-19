import math
import cv2
import numpy as np
from histgram import Histgram
from logging import getLogger
logger = getLogger(__name__)

def cvt_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def straighten(image):
    logger.debug('straighten...')
    gray = cvt_gray(image)
    # Gaussian , threshold, contours
    sigma_x = 65
    average_square = (sigma_x, sigma_x)
    img_gauss = cv2.GaussianBlur(image, average_square, sigma_x)
    ret, thres = cv2.threshold(img_gauss, 240, 255, cv2.THRESH_BINARY_INV)
    thres = cvt_gray(thres)
    _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 最大の矩形の傾きを取得
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    position, size, angle = rect

    # 傾きのずれを画像の回転で補正する
    while angle <= -45:
        angle += 90
    while angle >= 45:
        angle -= 90
    logger.debug('Largest contour angle: {}'.format(angle))

    rows, cols, _ = image.shape
    rotationMat = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    res_image = cv2.warpAffine(image, rotationMat, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
    return res_image

def shadow_y(image):
    logger.debug('shadow_y...')
    # gaussian_y
    sigma_x = 1
    sigma_y = 127
    average_square = (sigma_x, sigma_y)
    img_gauss = cv2.GaussianBlur(image, average_square, sigma_x, None, sigma_y)

    # threshold inverse
    gray = cv2.cvtColor(img_gauss, cv2.COLOR_RGB2GRAY)
    ret, thres = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    return thres

def detect_rubies(shadow_image):
    logger.debug('detect_rubies...')
    # 連結成分を取得する
    nlabels, labelimg, contours, CoGs = cv2.connectedComponentsWithStats(shadow_image)

    # 連結成分の width に関するヒストグラム
    get_width = lambda contour: contour[2]
    max_width = get_width(max(contours, key=get_width))
    widths = [get_width(c) for c in contours if get_width(c) != max_width]
    w_hist = Histgram(widths)
    logger.debug('histgram {}'.format(w_hist))

    # ヒストグラムの中点以下をルビと考える
    # 小さすぎるものはノイズ
    half_size = math.floor(w_hist.size / 2)
    ruby_contours = [c for c in contours if w_hist.get_index(get_width(c)) < half_size and w_hist.get_index(get_width(c)) > 0]
    logger.debug('Detect {} rubies contours'.format(len(ruby_contours)))
    return ruby_contours

def remove_rubies_by_contours(image, ruby_contours, color=(255,255,255)):
    image_h = image.shape[0]
    for c in ruby_contours:
        x,y,w,h,_ = c
        cv2.rectangle(image, (x,0), (x+w,image_h), color, -1)

def remove_rubies(image):
    straight_image = straighten(image)
    shadow_image = shadow_y(straight_image)
    rubies = detect_rubies(shadow_image)
    remove_rubies_by_contours(straight_image, rubies)
    return straight_image
