import numpy
import ScoreRect

def PixelSample(centerLoc,radius=10,halfsample = False):
    samples = []

    oriX = centerLoc.x_min
    oriY = centerLoc.y_min
    oriWidth = centerLoc.width
    oriHeight = centerLoc.height
    samples.append(ScoreRect.ScoreRect(oriX,oriY,oriWidth,oriHeight,0))

    r2 = radius*radius
    for iy in range(-radius,radius+1):
        for ix in range(-radius,radius+1):
            if ix**2+iy**2 > r2:
                continue
            if ix == 0 and iy == 0:
                continue
            if halfsample and (ix%2 != 0 or iy%2 != 0):
                continue
            overlap = CalOverlap(centerLoc,ix,iy)
            tempSampleRect = ScoreRect.ScoreRect(oriX+ix,oriY+iy,oriWidth,oriHeight,overlap)

            samples.append(tempSampleRect)

    return samples   

def RadialSample(centerLoc,nr,nt,sampleRadius = 20):
    samples = []

    rstep = sampleRadius/nr
    tstep = 2*numpy.pi/nt

    oriX = centerLoc.x_min
    oriY = centerLoc.y_min
    oriWidth = centerLoc.width
    oriHeight = centerLoc.height
    samples.append(ScoreRect.ScoreRect(oriX,oriY,oriWidth,oriHeight,0))

    for ir in range(1,nr+1):
        for it in range(nt):
            phase = (ir%2)*tstep/2
            dx = ir*rstep*numpy.cos(it*tstep+phase)
            dy = ir*rstep*numpy.sin(it*tstep+phase)
            overlap = CalOverlap(centerLoc,dx,dy)
            tempSampleRect = ScoreRect.ScoreRect(int(oriX+dx+0.5),int(oriY+dy+0.5),oriWidth,oriHeight,overlap) 
            samples.append(tempSampleRect)

    return samples


def CalOverlap(rect,dx,dy):
    if abs(dx) >= rect.width or abs(dy) >= rect.height:
        return 0.0
    else:
        overlapArea = (rect.width-abs(dx))*(rect.height-abs(dy))
        if (2*rect.Area()-overlapArea) == 0:
            print 'dx is %f,dy is %f,overlap area is %f,rect.Area is %f' %(dx,dy,overlapArea,rect.Area())
        else:
            overlapRate = float(overlapArea)/(2*rect.Area()-overlapArea)
        return overlapRate


'''
import Rect

aa = Rect.Rect(20,20,24,24)
for ix in range(6,31,6):
    for iy in range(6,31,6):
        print CalOverlap(aa,ix,iy)
'''

'''
aa = Rect.Rect(20,20,24,24)
bb = RadialSample(aa,10,8)
cc = PixelSample(aa,10)
for item in cc:
    print item
'''
