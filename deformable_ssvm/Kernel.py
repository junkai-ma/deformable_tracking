import numpy


def LinearKernel_CalPro(x1,x2):
    return numpy.dot(x1, x2)


def LinearKernel_CalNorm(x1):
    return numpy.linalg.norm(x1)


def GaussianKernel_CalPro(x1,x2):
    sigma = 0.2
    return numpy.exp(-sigma*numpy.linalg.norm(x1-x2))


def GaussianKernel_CalNorm(x1):
    return 1.0
