import numpy


def LinearKernel_CalPro(x1,x2):
    return numpy.dot(x1, x2)


def LinearKernel_CalNorm(x1):
    return numpy.linalg.norm(x1)
