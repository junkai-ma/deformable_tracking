import matplotlib.pyplot as plt


def show_inf(img1, img2, img3):
    plt.figure()

    plt.subplot(131)
    plt.imshow(img1)
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(img2)
    plt.colorbar()

    plt.subplot(133)
    plt.imshow(img3)
    plt.colorbar()
