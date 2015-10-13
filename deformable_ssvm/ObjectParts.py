import Rect

class ObjectParts:
    def __init__(self,RootLoc,PartsList):
        self.partsNum = len(PartsList)
        self.rootLoc = RootLoc
        self.partsList = PartsList

    def TranslatePart(self,partIndex,dx,dy):
        self.partsList[partIndex].Translate(dx,dy)
    
    def TranslateRoot(self,dx,dy):
        self.rootLoc.Translate(dx,dy)

    def __str__(self):
        outstring = 'The parts of a object contains:\n'
        outstring += 'Root Location is:\n'
        outstring += '[%f %f %f %f]\n' % (self.rootLoc.x_min,
                                          self.rootLoc.y_min,
                                          self.rootLoc.width,
                                          self.rootLoc.height)
        
        outstring += '%d parts be detected:\n' % self.partsNum
        for each in self.partsList:
            outstring += '[%f %f %f %f]\n' % (each.x_min,
                                              each.y_min,
                                              each.width,
                                              each.height)

        return outstring


if __name__ == '__main__':
    root1 = Rect.Rect(2.0,2.0,4.0,5.0)
    parts = []
    for i in range(5):
        parts.append(Rect.Rect(i,i,i,i))

    Object = ObjectParts(root1,parts)

    print Object

