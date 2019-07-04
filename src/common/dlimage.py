import requests
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import data, io, filters
from skimage.measure import compare_ssim as ssim
import skimage


def image_download(image_url, path, suffix):
    response = requests.get(image_url, stream=True)
    with open('{path}/img_{suffix}.jpg'.format(path=path, suffix=suffix), "wb") as image:
        image.write(response.content)


class compareImg:
    def __init__(self):
        pass

    def readImg(self, filepath):
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        # cv2.namedWindow("root", cv2.WINDOW_NORMAL)
        # cv2.imshow("root", img)
        # cv2.waitKey(5000)
        # cv2.destroyAllWindows()
        return img

    def diffImg(self, img1, img2):
        # Initiate SIFT detector
        orb = cv2.ORB_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        # Draw first 10 matches.
        knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
        plt.imshow(knn_image)
        plt.show()

    def run(self):
        # 이미지 파일 경로 설정
        filepath1 = r"C:\BA\python-web-crawling\src\images\1300k\image1.jpg"
        filepath2 = r"C:\BA\python-web-crawling\src\images\1300k\img_4654.jpg"

        # 이미지 객체 가져옴
        img1 = self.readImg(filepath1)
        img2 = self.readImg(filepath2)

        # 2개의 이미지 비교
        self.diffImg(img1, img2)


def compare_imgs(img1, img2):
    return ssim(img1, img2, multichannel=True)


def get_img(path):
    return io.imread(path)


def get_simillarity(img_path1, img_path2):
    img1 = skimage.img_as_float(get_img(img_path1))
    img2 = skimage.img_as_float(get_img(img_path2))

    return compare_imgs(img1, img2)


if __name__ == '__main__':
    s = get_simillarity(r"C:\BA\python-web-crawling\src\images\1300k\image1.jpg", r"C:\BA\python-web-crawling\src\images\1300k\img_4654.jpg")
    print(s)

