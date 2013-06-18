import pygame
from pygame.sprite import RenderUpdates

class Scene(pygame.sprite.RenderUpdates):

    def __init__(self, sprites):

       self._spritelist = [[sprites, sprites.getXPos(), sprites.getYPos()]]
       #self._spritelist.append([sprites, sprites.getXPos(), sprites.getYPos()])
       RenderUpdates.__init__(self, sprites)

       self.xPos = 0
       self.yPos = 0
       self.xSize = 0
       self.ySize = 0
       
       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def calcPosition(self):
    
       lowestX = 9000
       lowestY = 9000

       for i in range(len(self._spritelist)):
           if self._spritelist[i][0].getXPos() < lowestX: lowestX = self._spritelist[i][0].getXPos()
           if self._spritelist[i][0].getYPos() < lowestY: lowestY = self._spritelist[i][0].getYPos()

       self.xPos = lowestX
       self.yPos = lowestY

    def calcSize(self):
    
       highestX = 0
       highestY = 0
       
       for i in range(len(self._spritelist)):
           if (self._spritelist[i][0].getXPos() + self._spritelist[i][0].getXSize()) > highestX: highestX = self._spritelist[i][0].getXPos() + self._spritelist[i][0].getXSize()
           if (self._spritelist[i][0].getYPos() + self._spritelist[i][0].getYSize()) > highestY: highestY = self._spritelist[i][0].getYPos() + self._spritelist[i][0].getYSize()

       self.xSize = highestX - self.xPos
       self.ySize = highestY - self.yPos

    def addObject(self, newDrawableObject):
        RenderUpdates.add_internal(self, newDrawableObject)
        self._spritelist.insert(len(self._spritelist) - 1, [newDrawableObject, newDrawableObject.getXPos(), newDrawableObject.getYPos()])

    def addObjects(self, newDrawableObjects):
        for sprite in newDrawableObjects:
           RenderUpdates.add_internal(self, sprite)
           self._spritelist.insert(len(self._spritelist) - 1, [sprite, sprite.getXPos(), sprite.getYPos()])

    def setRelativePositions(self):

       for i in range(len(self._spritelist)):
           self._spritelist[i][1] = self._spritelist[i][0].getXPos() - self.xPos
           self._spritelist[i][2] = self._spritelist[i][0].getYPos() - self.yPos

    def removeObject(self, sprite):

       for i in self._spritelist:
           if i[0] == sprite:
               self._spritelist.remove(i)
               break
       RenderUpdates.remove_internal(self, sprite)

    def getObject(self, index):

       if index < len(self._spritelist):
          return  self._spritelist[index][0]

    def getListSize(self):

       return len(self._spritelist)

    def getList(self):

       return list(self._spritelist)

    def moveObjects(self):

       for i in range(len(self._spritelist)):
          self._spritelist[i][0].move()

       self.calcPosition()
       self.calcSize()
       self.setRelativePositions()

    def moveScene(self, xNudge = 0, yNudge = 0):

       
       for i in range(len(self._spritelist)):

          self._spritelist[i][0].nudge(xNudge, yNudge)
          

       self.calcPosition()

    def setPosition(self, newXPos = None, newYPos = None):

       if newXPos != None: self.xPos = newXPos
       if newYPos != None: self.yPos = newYPos

       for i in range(len(self._spritelist)):

          self._spritelist[i][0].setPosition(self.xPos + self._spritelist[i][1], self.yPos + self._spritelist[i][2])

    def getXPos(self):
       return self.xPos

    def getYPos(self):
       return self.yPos

    def getXSize(self):
       return self.xSize

    def getYSize(self):
       return self.ySize

    def scaleObjects(self, newXSize = None, newYSize = None):

       
       for i in range(len(self._spritelist)):
           self._spritelist[i][0].scale(newXSize, newYSize)

    def scaleScene(self, newXSize = None, newYSize = None):

       self.calcPosition()
       self.calcSize()

       xScale = 1
       yScale = 1

       if newXSize != None: xScale = (newXSize * 1.0)/self.xSize
       if newYSize != None: yScale = (newYSize * 1.0)/self.ySize
       
       for i in range(len(self._spritelist)):
           self._spritelist[i][0].scale(xScale * self._spritelist[iaw][0].getXSize(), yScale * self._spritelist[i][0].getYSize())
           self._spritelist[i][1] = xScale * self._spritelist[i][1]
           self._spritelist[i][2] = yScale * self._spritelist[i][2]

       self.calcPosition()
       self.calcSize()
       self.setPosition()

    def update(self, t):
    
       for s in self._spritelist: s[0].update(t);

    def draw(self, surface):
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append
       for s in self._spritelist:
           r = spritedict[s[0]]
           newrect = surface_blit(s[0].image, s[0].rect)
           if r is 0:
               dirty_append(newrect)
           else:
               if newrect.colliderect(r):
                   dirty_append(newrect.union(r))
               else:
                   dirty_append(newrect)
                   dirty_append(r)
           spritedict[s[0]] = newrect
       return dirty
       
    def drawEntireScene(self, surface):
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append
       for s in self._spritelist:
           dirty_append(spritedict[s[0]])
           dirty_append(surface_blit(s[0].image, s[0].rect))
       return dirty

    def nextFrame(self):

       for i in range(len(self._spritelist)):

          self._spritelist[i][0].nextFrame()
