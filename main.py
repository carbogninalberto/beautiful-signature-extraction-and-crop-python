import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import math


def bigger_box_and_alignment(boundRect):
    # (x, y)
    upper_left_point = [int(boundRect[0][0]), int(boundRect[0][1])]
    lower_right_point = [int(boundRect[0][0]+boundRect[0][2]), int(boundRect[0][1]+boundRect[0][3])]

    for bound in boundRect:
        if int(bound[0]) < upper_left_point[0]:
            upper_left_point[0] = int(bound[0])
        elif int(bound[0]+bound[2]) > lower_right_point[0]:
            lower_right_point[0] = int(bound[0]+bound[2])

        if int(bound[1]) < upper_left_point[1]:
            upper_left_point[1] = int(bound[1])
        elif int(bound[1]+bound[3]) > lower_right_point[1]:
            lower_right_point[1] = int(bound[1]+bound[3])

    return upper_left_point, lower_right_point, None



if __name__ == '__main__':

    path = 'dataset/'
    output_path = 'output/'

    images_path = []
    computed_images = []
    computed_images_cropped = []
    # import images
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            images_path.append(os.path.join(path, filename))

    for image_path in images_path:
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        param = int(np.mean(gray_image)/3.94)
        param -= abs(((1/(1 / 2*math.exp(param/100)))**3) * math.log((1/param)))**6 / 100000
        print(np.mean(gray_image)/3.94, "=>", round(param, 3), "delta", round(np.mean(gray_image)/3.94 - param, 3))
        bw_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 37, param)
        bw_image = cv2.blur(bw_image, (2, 2))
        bw_image = cv2.bilateralFilter(bw_image, 6, 50, 50)
        computed_images.append(bw_image)

    for idx, computed_image in enumerate(computed_images):

        computed_image = cv2.blur(computed_image, (3, 3))
        canny_output = cv2.Canny(computed_image, 100, 200)

        # contours
        contours_all, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = []
        for c in contours_all:
            if c.size > 50:
                contours.append(c)
        # Approximate contours to polygons + get bounding rects and circles
        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        centers = [None] * len(contours)
        radius = [None] * len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])

        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

        computed_image_crop = cv2.cvtColor(computed_image, cv2.COLOR_GRAY2BGR)
        computed_image = cv2.cvtColor(computed_image, cv2.COLOR_GRAY2BGR)

        # Draw polygonal contour + bonding rects + circles
        for i in range(len(contours)):
            color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            cv2.rectangle(computed_image, (int(boundRect[i][0]), int(boundRect[i][1])),
                            (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 1)

        upper_left, lower_right, _ = bigger_box_and_alignment(boundRect)
        computed_images_cropped.append(computed_image_crop[upper_left[1]:lower_right[1], upper_left[0]:lower_right[0]])
        print("upperleft {} lower_right {}".format(upper_left, lower_right))
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        cv2.rectangle(computed_image, (upper_left[0], upper_left[1]), (lower_right[0], lower_right[1]),
                      (255, 0, 0), 2)
        computed_images[idx] = computed_image

    for idx, image_path in enumerate(images_path):
        image = cv2.imread(image_path)
        plt.subplot(int(len(images_path) / 2), 2, idx + 1), plt.imshow(image[:,:,::-1])
        plt.title('boxes {}'.format(idx))
        plt.xticks([]), plt.yticks([])
    plt.savefig('original.jpg', dpi=1000)

    plt.clf()

    for idx, computed_image in enumerate(computed_images):
        plt.subplot(int(len(computed_images) / 2), 2, idx + 1), plt.imshow(computed_image, 'gray')
        plt.title('boxes {}'.format(idx))
        plt.xticks([]), plt.yticks([])
    plt.savefig('result_boxes.jpg', dpi=1000)

    plt.clf()

    for idx, computed_image_crop in enumerate(computed_images_cropped):
        plt.subplot(int(len(computed_images_cropped) / 2), 2, idx + 1), plt.imshow(computed_image_crop, 'gray')
        plt.title('result {}'.format(idx))
        plt.xticks([]), plt.yticks([])
    plt.savefig('results.jpg', dpi=1000)
