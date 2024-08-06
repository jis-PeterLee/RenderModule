import turtle as trt
import math
import time

width = 715
height = 495
color = "white"

objdict = {}

trt.screensize(width, height, color)

axis = trt.Turtle()
pen1 = trt.Turtle()
pen2 = trt.Turtle()
pen3 = trt.Turtle()
hitbox = trt.Turtle()

axis.speed(1000)
axis.width(2)
axis.penup()
axis.hideturtle()

pen1.speed(1000)
pen1.width(2)
pen1.penup()
pen1.hideturtle()

pen2.speed(1000)
pen2.width(2)
pen2.penup()
pen2.hideturtle()

pen3.speed(1000)
pen3.width(2)
pen3.penup()
pen3.hideturtle()

hitbox.speed(1000)
hitbox.width(1.5)
hitbox.penup()
hitbox.color("blue")
hitbox.hideturtle()



class NoIndexError(Exception):
    # Error for GetObj() function
    pass

class obj:

    def __init__(self, DotPos, color, xpos, ypos):

        # fundamental variables
        self.DotPos = DotPos
        self.DotAm = int(len(DotPos) / 2)
        self.color = color
        self.xpos = xpos
        self.ypos = ypos

        # lists of positions seperated by axes
        self.DotX = []
        self.DotY = []
        # existence and nonexistence of collision
        self.collision = 0

        for i in range(self.DotAm):
            self.DotX.append(self.DotPos[i * 2])
            self.DotY.append(self.DotPos[i * 2 + 1])

        # required for collision detections
        
        self.width = max(self.DotX) - min(self.DotX)
        self.height = max(self.DotY) - min(self.DotY)
        
        self.DistX = min(self.DotX)
        self.DistY = min(self.DotY)

        self.MinX = min(self.DotX) + self.xpos
        self.MaxX = max(self.DotX) + self.xpos
        self.MinY = min(self.DotY) + self.ypos
        self.MaxY = max(self.DotY) + self.ypos

        # list of Vector2 positions converted to Trigometric positions
        self.TrigoPos = VectorToTrigo(self.DotPos)
    
    def render(self, pen):

        DotPos = TrigoToVector(self.TrigoPos)

        # using different pens to create layers

        if pen == 1:
            
            pen1.color(self.color)

            for i in range(self.DotAm):
                pen1.setposition(DotPos[i * 2] + self.xpos, DotPos[i * 2 + 1] + self.ypos)
                pen1.pendown()

            pen1.penup()
        
        elif pen == 2:
            
            pen2.color(self.color)

            for i in range(self.DotAm):
                pen2.setposition(DotPos[i * 2] + self.xpos, DotPos[i * 2 + 1] + self.ypos)
                pen2.pendown()

            pen2.penup()

        elif pen == 3:
            
            pen3.color(self.color)

            for i in range(self.DotAm):
                pen3.setposition(DotPos[i * 2] + self.xpos, DotPos[i * 2 + 1] + self.ypos)
                pen3.pendown()

            pen3.penup()
    
    def rotate(self, RotAng):

        for i in range(self.DotAm):
            angle = self.TrigoPos[i * 2 + 1]

            # convert RotAng into radian unit

            angle += RotAng / 180 * math.pi

            # replace the original radian angle in TrigoPos into a new one

            self.TrigoPos.pop(i * 2 + 1)

            self.TrigoPos.insert(i * 2 + 1, angle)

            # updating the with, height, DistX, DistY, Min/Max X/Y to update the hitbox of the object

            self.DotPos = TrigoToVector(self.TrigoPos)

            self.DotX = []
            self.DotY = []

            for i in range(self.DotAm):
                self.DotX.append(self.DotPos[i * 2])
                self.DotY.append(self.DotPos[i * 2 + 1])

            self.width = max(self.DotX) - min(self.DotX)
            self.height = max(self.DotY) - min(self.DotY)
   
            self.DistX = min(self.DotX)
            self.DistY = min(self.DotY)

            self.MinX = min(self.DotX) + self.xpos
            self.MaxX = max(self.DotX) + self.xpos
            self.MinY = min(self.DotY) + self.ypos
            self.MaxY = max(self.DotY) + self.ypos
        
    def move(self, Tox, Toy):
        self.xpos += Tox
        self.ypos += Toy

        # update Min/Max X/Y

        self.MinX = min(self.DotX) + self.xpos
        self.MaxX = max(self.DotX) + self.xpos
        self.MinY = min(self.DotY) + self.ypos
        self.MaxY = max(self.DotY) + self.ypos

    def setposition(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

        # update Min/Max X/Y
        
        self.MinX = min(self.DotX) + self.xpos
        self.MaxX = max(self.DotX) + self.xpos
        self.MinY = min(self.DotY) + self.ypos
        self.MaxY = max(self.DotY) + self.ypos

    def CheckCollisions(self, target):

        collided = 0

        if target == False:

            for i in objdict:
                
                obj = objdict[i]

                objMinX = min(obj.DotX) + obj.xpos
                objMaxX = max(obj.DotX) + obj.xpos
                objMinY = min(obj.DotY) + obj.ypos
                objMaxY = max(obj.DotY) + obj.ypos

                if (objMinX <= self.MaxX and objMaxX >= self.MinX) and (objMinY <= self.MaxY and objMaxY >= self.MinY):
                    collided += 1
            collided += -1

        elif target == "x-axis":

            if self.MaxX >= width:
                return 1
            elif self.MinX <= 0 - width:
                return -1
            else:
                return 0
        elif target == "y-axis":

            if self.MaxY >= height or self.MinY <= 0 - height:
                return 1
            elif self.MinY <= 0 - height:
                return -1
            else:
                return 0

        else:

            target = GetObj("sprite2")
            targetMinX = min(target.DotX) + target.xpos
            targetMaxX = max(target.DotX) + target.xpos
            targetMinY = min(target.DotY) + target.ypos
            targetMaxY = max(target.DotY) + target.ypos

            if (targetMinX <= self.MaxX and targetMaxX >= self.MinX) and (targetMinY <= self.MaxY and targetMaxY >= self.MinY):
                collided += 1
        
        return collided

    def ShowHitBox(self):
        
        # tracing the rectangle hitbox

        hitbox.color("blue")
        hitbox.setposition(self.MinX,self.MinY)
        hitbox.pendown()
        hitbox.setposition(self.MaxX, self.MinY)
        hitbox.setposition(self.MaxX, self.MaxY)
        hitbox.setposition(self.MinX, self.MaxY)
        hitbox.setposition(self.MinX, self.MinY)
        hitbox.penup()

def VectorToTrigo(DotPos:list):

    TrigoPos = []

    DotAm = int(len(DotPos) / 2)
    
    for i in range(DotAm):
        
        xpos = DotPos[i * 2]
        ypos = DotPos[i * 2 + 1]

        radius = math.sqrt(abs(xpos) ** 2 + abs(ypos) ** 2)

        if radius == 0:
            angle = 0
        else:
            angle = math.asin(abs(ypos) / radius)

        TrigoPos.append(radius)
        TrigoPos.append(angle)

        # print("xpos : {0} , ypos : {1} , radius : {2} , angle : {3}".format(xpos, ypos, radius, angle))
    
    return TrigoPos

def TrigoToVector(TrigoPos:list):

    VectorPos = []

    DotAm = int(len(TrigoPos) / 2)

    for i in range(DotAm):

        radius = TrigoPos[i * 2]

        angle = TrigoPos[i * 2 + 1]

        xpos = math.cos(angle) * radius
        ypos = math.sin(angle) * radius

        VectorPos.append(xpos)
        VectorPos.append(ypos)

    return VectorPos

def NewSprite(DotPos:list, color, xpos, ypos, name):
    objdict[name] = obj(DotPos, color, xpos, ypos)

def DrawAxis():
    axis.setposition(0 - width, 0)
    axis.pendown()
    axis.setposition(width, 0)
    axis.penup()
    axis.setposition(0, 0 - height)
    axis.pendown()
    axis.setposition(0, height)
    axis.penup()

def wait(sec):
    time.sleep(sec)

def GetObj(name):
    if name not in objdict.keys():
        raise NoIndexError
    else:
        return objdict[name]

def clear(pen):
    if pen == 1:
        pen1.clear()
    elif pen == 2:
        pen2.clear()
    elif pen == 3:
        pen3.clear()
    elif pen == "hitbox":
        hitbox.clear()

def RenderAll(pen):
    
    # render all objects in objdict

    for i in objdict:
        obj = objdict[i]
        obj.render(pen)

def ShowAllHitBox():

    for i in objdict:
        obj = objdict[i]
        obj.ShowHitBox()
    
