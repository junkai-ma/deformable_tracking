import cv2
import numpy as np


bin_n = 16
SZ = 20
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR


def hog(img):
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)

    # quantizing binvalues in (0...16)
    bins = np.int32(bin_n*ang/(2*np.pi))

    # Divide to 4 sub-squares
    bin_cells = bins[:10, :10], bins[10:, :10], bins[:10, 10:], bins[10:, 10:]
    mag_cells = mag[:10, :10], mag[10:, :10], mag[:10, 10:], mag[10:, 10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    return hist


def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 2:
        return img.copy()

    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img, M, (SZ, SZ), flags=affine_flags)
    return img


def get_hog(img):
    normal_image = cv2.resize(image, (SZ, SZ))
    return hog(normal_image)

if __name__ == '__main__':
    image = cv2.imread('00001.jpg')
    cv2.imshow('target1', image)
    cv2.waitKey(0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('target2', gray_image)
    cv2.waitKey(0)
    image2 = deskew(gray_image)
    print image2.shape
    cv2.imshow('target3', image2)
    cv2.waitKey(0)
    hog_feature = hog(image2)
    print hog_feature
