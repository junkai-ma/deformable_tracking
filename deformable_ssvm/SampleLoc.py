import numpy
import Rect


def PixelSample(centerLoc, radius=20, halfsample=False):
    samples = []

    oriX = centerLoc.x_min
    oriY = centerLoc.y_min
    oriWidth = centerLoc.width
    oriHeight = centerLoc.height
    samples.append(Rect.Rect(oriX, oriY, oriWidth, oriHeight))

    r2 = radius*radius
    for iy in range(-radius,radius+1):
        for ix in range(-radius,radius+1):
            if ix**2+iy**2 > r2:
                continue
            if ix == 0 and iy == 0:
                continue
            if halfsample and (ix%2 != 0 or iy%2 != 0):
                continue
            # overlap = CalOverlap(centerLoc,ix,iy)
            tempSampleRect = Rect.Rect(oriX+ix, oriY+iy, oriWidth, oriHeight)

            samples.append(tempSampleRect)

    return samples   


def RadialSample(centerLoc, nr, nt, sampleRadius=20):
    samples = []

    rstep = sampleRadius/nr
    tstep = 2*numpy.pi/nt

    oriX = centerLoc.x_min
    oriY = centerLoc.y_min
    oriWidth = centerLoc.width
    oriHeight = centerLoc.height
    samples.append(Rect.Rect(oriX, oriY, oriWidth, oriHeight))

    for ir in range(1,nr+1):
        for it in range(nt):
            phase = (ir%2)*tstep/2
            dx = ir*rstep*numpy.cos(it*tstep+phase)
            dy = ir*rstep*numpy.sin(it*tstep+phase)
            # overlap = CalOverlap(centerLoc, dx, dy)
            tempSampleRect = Rect.Rect(int(oriX+dx+0.5), int(oriY+dy+0.5), oriWidth, oriHeight)
            samples.append(tempSampleRect)

    return samples

'''
def CalOverlap(rect,dx,dy):
    if abs(dx) >= rect.width or abs(dy) >= rect.height:
        return 0.0
    else:
        overlapArea = (rect.width-abs(dx))*(rect.height-abs(dy))
        if (2*rect.Area()-overlapArea) == 0:
            print 'dx is %f,dy is %f,overlap area is %f,rect.Area is %f' % (dx, dy, overlapArea, rect.Area())
        else:
            overlapRate = float(overlapArea)/(2*rect.Area()-overlapArea)
        return overlapRate
'''


def RegionSample(root_rect, original_rect, step_x, step_y, expand_h, expand_w):
    """

    :rtype : object
    """
    height = root_rect.height+2*expand_h-original_rect.height
    width = root_rect.width+2*expand_w-original_rect.width
    n_width = int(width/step_x)+1
    n_height = int(height/step_y)+1
    new_tl_x = root_rect.x_min-expand_w
    new_tl_y = root_rect.y_min-expand_h
    samples = []
    samples.append(original_rect)
    for i in range(n_width):
        for j in range(n_height):
            dx = i*step_x
            dy = j*step_y
            tempRect = Rect.Rect(new_tl_x+dx, new_tl_y+dy, original_rect.width, original_rect.height)
            samples.append(tempRect)

    return samples

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


def PartsSample(parts, expand_x, expand_y):

    samples = []

    for part_num in range(len(parts)):
        temp_group = []
        original_rect = parts[part_num]
        height = original_rect.height
        width = original_rect.width
        for dy in range(-expand_x, expand_x+1):
            temp_list_h = []
            new_y = original_rect.y_min+dy
            for dx in range(-expand_y, expand_y+1):
                new_x = original_rect.x_min+dx
                rect = Rect.Rect(new_x, new_y, width, height)
                temp_list_h.append(rect)

            temp_group.append(temp_list_h)

        samples.append(temp_group)

    return samples


if __name__ == '__main__':
    center_example = Rect.Rect(10, 10, 4, 4)
    part1 = Rect.Rect(8, 8, 8, 8)
    part2 = Rect.Rect(14, 25, 10, 10)
    roots = [center_example, part1, part2]
    sample_example = PartsSample(roots, 4, 4)

    print ('ok')
