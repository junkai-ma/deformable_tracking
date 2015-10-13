class Rect:
    def __init__(self,x_min=0,y_min=0,width=0,height=0):
        self.x_min = x_min
        self.y_min = y_min
        self.width = width
        self.height = height
        self.x_max = x_min+width
        self.y_max = y_min+height

    def SetXMin(self,x):
        self.x_min = x
        self.x_max = self.x_min+self.width

    def SetYMin(self,y):
        self.y_min = y
        self.y_max = self.y_min+self.height

    def SetWidth(self,width):
        self.width = width
        self.x_max = self.x_min+self.width
    
    def SetHeight(self,height):
        self.height = height
        self.y_max = self.y_min+self.height
    
    def Area(self):
        return self.width*self.height

    def TopLeft(self):
        return (self.x_min,self.y_min)

    def BottomRight(self):
        return (self.x_max,self.y_max)

    def Translate(self,xAdd,yAdd):
        self.x_min += xAdd
        self.y_min += yAdd
        self.x_max += xAdd
        self.y_max += yAdd

    def __str__(self):
        return '[%f %f %f %f]'% (self.x_min,self.y_min,self.width,self.height)

if __name__ == '__main__':
    rect1 = Rect(2,4,5,8)
    print rect1
    rect1.SetXMin(1)
    print rect1
    print rect1.TopLeft()
    print rect1.BottomRight()
