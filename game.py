import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, new_x, new_y, w, h):
		self.x = new_x
		self.y = new_y
		self.width = w
		self.height = h

class Mario(Sprite):
	def __init__(self, x, y, m):

		super().__init__(x, y , 60, 95)

		self.px = 0
		self.py = 0

		self.numFrames = 0
		self.marioOffset = 100

		self.vert_vel = 0.0

		self.model = m

		self.direction = 1

		self.marioImageNum = 0

		self.imageArray=[]

		self.marioImage1 = pygame.image.load("mario1.png")
		self.imageArray.append(self.marioImage1)
		self.marioImage2 = pygame.image.load("mario2.png")
		self.imageArray.append(self.marioImage2)
		self.marioImage3 = pygame.image.load("mario3.png")
		self.imageArray.append(self.marioImage3)
		self.marioImage4 = pygame.image.load("mario4.png")
		self.imageArray.append(self.marioImage4)
		self.marioImage5 = pygame.image.load("mario5.png")
		self.imageArray.append(self.marioImage5)

		self.image = self.imageArray[0]

	def jump(self):
		if(self.numFrames < 5):
    			self.vert_vel =-15
			
	def update(self):
		self.image = self.imageArray[self.marioImageNum]
		self.numFrames+=1

		self.vert_vel+=0.8
		self.y+=self.vert_vel

		if(self.y >= 400 - self.height):
			self.vert_vel = 0.0
			self.y = 400 - self.height
			self.numFrames = 0

	def updateImage(self):
		self.marioImageNum+=1
		if(self.marioImageNum > 4):
    			self.marioImageNum = 0

	def saveLastCoordinate(self):
		self.px = self.x
		self.py = self.y

	def getOutOfTube(self, t):
		if(self.x + self.width >= t.x and self.px + self.width <= t.x):
			self.x = t.x - self.width
		if(self.x <= t.x + t.width and self.px >= t.x + t.width):
			self.x = t.x + t.width
		if(self.y <= t.height + t.y and self.py >= t.y + t.height):
			self.y = t.y + t.height
		if(self.y + self.height >= t.y and self.py + self.height <= t.y):
			self.numFrames = 0
			self.vert_vel = 0
			self.y = t.y - self.height

class Tube(Sprite):
	def __init__(self, x, y, m):
		
		super().__init__(x, y , 55, 400)

		self.model = m

		self.tubeImage = pygame.image.load("tube.png")
		self.image = self.tubeImage

	def update(self):
		pass	

class Goomba(Sprite):
	def __init__(self, x, y, m):
    		
		super().__init__(x, y , 37, 44)

		self.model = m

		self.px = 0
		self.py = 0

		self.goombaHealth = 42
		self.isOnFire = False

		self.direction = 1

		self.goombaImage = pygame.image.load("goomba.png")
		self.goombaFireImage = pygame.image.load("goomba_fire.png")

		self.image = self.goombaImage

	def saveLastCoordinate(self):
		self.px = self.x
		self.py = self.y
	
	def update(self):	
		self.saveLastCoordinate()

		if(not self.isOnFire):
			self.x+=5*self.direction
		else:
			self.x+=0
		
		for Sprite in self.model.sprites:
			if(type(Sprite) is Tube):
				if(self.collide(Sprite)):
					self.getOutOfTube(Sprite)
		
		if(self.isOnFire):
			self.goombaHealth-=1
			self.image = self.goombaFireImage

	def collide(self, a):
		if(self.x + self.width < a.x):
			return False
		if(self.x > a.x + a.width):
			return False
		if(self.y + self.height < a.y):
			return False
		return True

	def getOutOfTube(self, t):
		if(self.x + self.width >= t.x and self.px + self.width <= t.x):
			self.x = t.x - self.width
			self.direction = self.direction*-1

		if(self.x <= t.x + t.width and self.px >= t.x + t.width):
			self.x = t.x + t.width
			self.direction = self.direction*-1

		if(self.y + self.height >= t.y and self.py + self.height <= t.y):
			self.vert_vel = 0
			self.y = t.y - self.height

	def setOnFire(self):
		self.isOnFire = True

	def getHealth(self):
		return self.goombaHealth

class Fireball(Sprite):
	def __init__(self, x, y, m):
    		
		super().__init__(x, y , 37, 37)

		self.model = m

		self.px = 0
		self.py = 0

		self.vert_vel = -40.0
		self.fireballSpeed = 15
		self.direction = 1

		self.fireballImage = pygame.image.load("fireball.png")
		self.image = self.fireballImage
	
	def saveLastCoordinate(self):
		self.px = self.x
		self.py = self.y
	
	def update(self):
		self.x += self.fireballSpeed * self.direction
		self.vert_vel += 8.0
		self.y += self.vert_vel

		self.saveLastCoordinate()

		#some number on the map for ground
		if(self.y > 395):
			self.vert_vel =- 30.3
			self.y = 350 - self.height

		for Sprite in self.model.sprites:
			if(type(Sprite) is Goomba):
				if(self.collide(Sprite)):
					Sprite.setOnFire()
					self.model.sprites.remove(self)

	def collide(self, a):
		if(self.x + self.width < a.x):
			return False
		if(self.x > a.x + a.width):
			return False
		if(self.y + self.height < a.y):
			return False
		return True
   
class Model():
	def __init__(self):
		self.sprites = []

		self.mario = Mario(100, 206, self)
		self.sprites.append(self.mario)

		self.tube = Tube(111, 350, self)
		self.sprites.append(self.tube)

		self.tube = Tube(294, 308, self)
		self.sprites.append(self.tube)
		
		self.tube = Tube(645, 290, self)
		self.sprites.append(self.tube)

		self.sprites.append(Goomba(500, 357, self))

		self.sprites.append(Goomba(255, 357, self))


		self.fireballCount = 0

	def update(self):
		for Sprite in self.sprites:
			Sprite.update()

			if(type(Sprite) is Tube):
				if(self.collide(self.mario, Sprite)):
					self.mario.getOutOfTube(Sprite)
			if(type(Sprite) is Goomba):
				if(Sprite.goombaHealth == 0):
					self.sprites.remove(Sprite)


		self.fireballCount+=1

	def collide(self, a, b):
		if(a.x + a.width < b.x):
			return False
		if(a.x > b.x + b.width):
			return False
		if(a.y > b.y + b.height):
			return False
		if(a.y + a.height < b.y):
			return False
		return True
	
	def addFireball(self):
		if(self.fireballCount > 5):
			self.fireball = Fireball(self.mario.x + self.mario.width, self.mario.y, self)
			self.sprites.append(self.fireball)

			self.fireballCount = 0

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):   
		self.screen.fill([135,206,250])
		pygame.draw.rect(self.screen, (0,200,0), (0,400,100000,500), 0)

		for Sprite in self.model.sprites:
			if(type(Sprite) is Mario):
				if(Sprite.direction == 1):
					#draw image
					self.screen.blit(self.model.mario.image, (self.model.mario.marioOffset, Sprite.y))
				else:
					#draw image flip (not done yet)
					self.screen.blit(self.model.mario.image, (self.model.mario.marioOffset, Sprite.y))
			else:
    				self.screen.blit(Sprite.image, (Sprite.x - self.model.mario.x + self.model.mario.marioOffset, Sprite.y))
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_LCTRL:
					self.model.addFireball()
    					
		keys = pygame.key.get_pressed()

		self.model.mario.saveLastCoordinate()

		if keys[K_LEFT]:
			self.model.mario.x-=6
			self.model.mario.updateImage()
			# self.model.mario.direction = 1
		if keys[K_RIGHT]:
			self.model.mario.x+=6
			self.model.mario.updateImage()
			# self.model.mario.direction = 1
		if keys[K_UP]:
			self.model.mario.jump()
		if keys[K_SPACE]:
			self.model.mario.jump()

print("Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")