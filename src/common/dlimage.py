import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from skimage import data, io, filters, color
from skimage.measure import compare_ssim as ssim
from skimage.transform import rescale, resize, downscale_local_mean
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
    return ssim(img1, img2, multichannel=True, data_range=img1.max() - img2.min())


def get_img(path):
    return io.imread(path)


def get_simillarity(img_path1, img_path2):
    imgA = get_img(img_path1)
    imgB = resize(get_img(img_path2), imgA.shape)

    imgA = skimage.img_as_float(get_img(img_path1))
    imgB = skimage.img_as_float(resize(get_img(img_path2), imgA.shape))

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    ax = axes.ravel()

    ax[0].imshow(imgA)
    ax[1].imshow(imgB)
    ax[1].set_xlabel(compare_imgs(imgA, imgB))

    fig.tight_layout()
    plt.show()


    # skimage.img_as_float()

    return compare_imgs(imgA, imgB)


if __name__ == '__main__':
    img_path1 = r"C:\BA\python-web-crawling\src\images\1300k\img_전체_215024702984.jpg"
    img_path2 = r"C:\BA\python-web-crawling\src\images\10x10\img_전체_215024702984_2339102_2.jpg"
    # img_path2 = r"C:\BA\python-web-crawling\src\images\10x10\img_전체_215024397505_2056826_2.jpg"
    s = get_simillarity(img_path1=img_path1, img_path2=img_path2)

    print(s)