from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def show_mat(mat_data):
    w, h = mat_data.shape

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(0, h)
    Y = np.arange(0, w)
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, mat_data)
    # ax.set_zlim(-1.01, 1.01)

    # x.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
