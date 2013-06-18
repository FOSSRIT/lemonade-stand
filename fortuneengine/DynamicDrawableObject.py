import pygame
from DrawableObject import DrawableObject

class DynamicDrawableObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,images,textfileName,fps = 10, x = 0, y = 0, xVelocity = 0, yVelocity = 0):

        self._delay = 1000/fps
        DrawableObject.__init__(self, images, textfileName, x, y)

    def addImages(self, images):

        self._images.extend(images)

    def setSpeed(self, xVelocity = None, yVelocity = None):

       if xVelocity != None:  self.xSpeed = xVelocity
       if yVelocity != None:  self.ySpeed = yVelocity

    def getXSpeed(self):

       return self.xSpeed

    def getYSpeed(self):

       return self.ySpeed

    def move(self):
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed
        self.rect.right += self.xSpeed
        self.rect.top += self.ySpeed

    def update(self, t):

        timePassed = t + self._last_update

        if (timePassed) > self._delay:
            if self._frame < self.animations.get(self._current_anim)[0] or self._frame > self.animations.get(self._current_anim)[1]:
                self._frame = self.animations.get(self._current_anim)[0] - 1

            self._frame += timePassed/self._delay
            
            if self._frame >= self.animations.get(self._current_anim)[1]:
                self._frame = self._frame%(self.animations.get(self._current_anim)[1])
            
            self.image = self._images[self._frame]
            self._last_update = timePassed%self._delay
        else:   
            self._last_update = timePassed

    def nextFrame(self):
        self._frame += 1
        if self._frame >= len(self._images):
            framesPast = self._frame - len(self._images)
            self._frame = framesPast

        self.image = self._images[self._frame]

    def nextCurrentAnimFrame(self):

        for cnt in range(len(animations)):

            if animations[cnt] == self._current_anim:
                if self._frame < self.animations[self._current_anim][0] or self._frame > self.animations[self._current_anim][1]:
                    self._frame = self.animations[self._current_anim][0]

                else: self._frame += 1

                if self._frame > self.animations[self._current_anim][1]:
                    framesPast = self._frame - self.animations[self._current_anim][1]
                    self._frame = framesPast - 1 + self.animations[self._current_anim][0]
                  
                self.image = self._images[self._frame]
