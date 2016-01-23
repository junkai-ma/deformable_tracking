import Rect
import cv2
import Displacement


def AddPartRegionOnImage(img, parts):
    img_new = img
    for each_part in parts:
        cv2.rectangle(img_new, each_part.TopLeft(), each_part.BottomRight(), (255, 255, 0))
    return img_new


def TwoPointRegion2Rect(regions):
    return [Rect.Rect(x[0], x[1], x[2]-x[0], x[3]-x[1]) for x in regions]


def CalDistanceFromRect(parts):
    distances = []
    for i in range(1, len(parts)):
        dis = Displacement.Displacement(parts[i].x_min-parts[0].x_min, parts[i].y_min-parts[0].y_min)
        distances.append(dis)

    return distances
