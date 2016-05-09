import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


class DrawDebug(object):
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()
        self.image_axe = self.fig.add_subplot(121)
        self.data_axe = ImageGrid(self.fig, 122,
                                  axes_pad=0.1,
                                  nrows_ncols=(2, 2),
                                  cbar_mode='single')

    def show_data(self, image_data, other):

        self.image_axe.imshow(image_data)
        for i in range(4):
            im = self.data_axe[i].imshow(other[i])

        self.data_axe.cbar_axes[0].colorbar(im)

        for cax in self.data_axe.cbar_axes:
            cax.toggle_label(False)

        plt.show()

if __name__ == '__main__':
    import cv2
    import numpy as np
    image = cv2.imread('00001.jpg')
    x_r = np.random.rand(10, 10)
    x_r2 = np.random.rand(10, 10)*5
    x_r_list = [x_r, x_r, x_r, x_r2]
    debug_window = DrawDebug()
    debug_window.show_data(image, x_r_list)

    print "abc"
