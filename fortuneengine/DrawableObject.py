import pygame

class DrawableObject(pygame.sprite.Sprite):

    def __init__(self, images, textfileName, transparent = False, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        
        self._images = []
        self._origImages = []
        for i in range(len(images)):
            self._images.append(images[i].convert_alpha())
            self._origImages.append(images[i].convert_alpha())
            
        blank = pygame.Surface((0,0))
        
        if(transparent):
            for i in range(len(images)):
                self._images[i] = blank

        self._start = pygame.time.get_ticks()
        self.image = self._images[0]
        self._last_update = 0
        self._frame = 0
        self.animations = {}
        self._current_anim = ""
        self.rect = self.image.get_rect()
        self.xPos = x
        self.yPos = y
        self.myAngle = 0
        self.xSize = self.image.get_width()
        self.ySize = self.image.get_height()
        self.rect.topleft = (x,y)

        if textfileName != '':

           f = open(textfileName, 'r')
           currentLine = f.readline()
           while currentLine != '':

             animValues = currentLine.split(",")
             self.animations[animValues[0]] =  [int(animValues[1]), int(animValues[2])]
             currentLine = f.readline()

        else:
        
            self.animations["anim1"] = [0, len(self._images)]
            self.goToAnim("anim1")

        self.makeTransparent(transparent)

    def repopulateImages(self, newImages):
    
        self._images = []
        self._origImages = []
        for i in range(len(newImages)):
            self._images.append(newImages[i].convert_alpha())
            self._origImages.append(newImages[i].convert_alpha())
        
        self.image = self._images[0]
        self._frame = 0
        self.xSize = self.image.get_width()
        self.ySize = self.image.get_height()

    def addImages(self, images):
        self._images.extend(images)
        self._origImages.extend(images)

    def goToAnim(self, animName):
      if self.animations.get(animName, 0) != 0:
         self._current_anim = animName
         self._frame = self.animations[animName][0]
         self.image = self._images[self._frame]
         
    def goToFrame(self, frame):

        if frame <= len(self._images):
           self._frame = frame
           self.image = self._images[self._frame]

    def nudge(self, x, y):
        self.xPos += x
        self.yPos += y
        self.rect.right += x
        self.rect.top += y

    def scale(self, x=None, y=None):
        if type(x).__name__=='int': self.xSize = x
        if type(y).__name__=='int': self.ySize = y
            
        for i in range(len(self._images)):
            self._origImages[i] = pygame.transform.scale(self._origImages[i], (self.xSize, self.ySize))
            self._images[i] = self._origImages[i]

    def fill(self, color):
        for i in range(len(self._images)):
            #print "filling with ", color
            self._origImages[i].fill(color)
            self._images[i].fill(color)
            
    def getXSize(self):
       return self.xSize

    def getYSize(self):
       return self.ySize

    def rotate(self,angle):
        self.myAngle += angle
        for i in range(len(self._images)):
            self._images[i] = pygame.transform.rotate(self._origImages[i], self.myAngle)

    def getRotation(self):
       return self.myAngle

    def setPosition(self, x = None, y = None):
        if type(x).__name__=='int': self.xPos = x
        if type(y).__name__=='int': self.yPos = y
        self.rect.topleft = (self.xPos, self.yPos)

    def getXPos(self):
       return self.xPos

    def getYPos(self):
       return self.yPos

    def calcColorKey(self, x=0, y=0):
       myColorKey = images[0].get_at((x,y))
       setColorKey(myColorKey)
       
    def makeTransparent(self, bool = True):
       if bool == True:
            surf = pygame.Surface((0,0))
            for i in range(len(self._images)):
                self._images[i] = surf
       else:
            for i in range(len(self._images)):
                self._images[i] = self._origImages[i]
            self.image = self._images[self._frame]

    def setColorKey(self, aColor):
       for i in range(len(self._images)):
          self._images[i].set_colorkey(aColor)

    def update(self, t=None):
        timePassed = t + self._last_update

        if (timePassed) > 200:

            self.image = self._images[self._frame]
            self._last_update = timePassed%1000
        else:   
            self._last_update = timePassed

    def nextFrame(self):
       pass

    def nextCurrentAnimFrame(self):
       pass
