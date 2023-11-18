import pygame
import pymunk
import pymunk.pygame_util
import math

pymunk.pygame_util.positive_y_is_up=False
pygame.init()

screen=pygame.display.set_mode([490,490])
pygame.display.set_caption("carrom")
clock=pygame.time.Clock()
draw_options=pymunk.pygame_util.DrawOptions(screen)

bg=pygame.image.load("bg.png")
bg=pygame.transform.scale(bg, (490,490))

space = pymunk.Space()
space.gravity=0,0
static=space.static_body

font=pygame.font.SysFont("Arial", 15)
f=0

def seg(pos1,pos2):
	body=pymunk.Segment(space.static_body,pos1,pos2, 16)
	body.elasticity=0.8
	body.friction=0.2
	space.add(body)

seg((0,0),(490,0))
seg((0,0),(0,490))
seg((490,0),(490,490))
seg((0,490),(490,490))

class coin:
	c=[]
	def __init__(self,r,m,f,e,p,c,s=False,a=False):
		self.body=pymunk.Body()
		self.body.position=p
		self.shape=pymunk.Circle(self.body, r)
		self.shape.mass,self.shape.elasticity,self.shape.friction=m,e,f
		self.pivot=pymunk.PivotJoint(static,self.body,(0,0),(0,0))
		self.pivot.max_bias,self.pivot.max_force=0,100
		space.add(self.body,self.shape,self.pivot)
		self.c,self.r,self.s,self.a=c,r,s,a
		self.status="in"
		coin.c.append(self)

arr=[[(245,209),"white"],[(245,227),"black"],[(245,245),"red"],[(245,263),"white"],[(245,281),"white"],
     [(227,272),"black"],[(227,254),"black"],[(227,236),"white"],[(227,218),"black"],
     [(209,227),"white"],[(209,245),"black"],[(209,263),"white"],
     [(263,272),"black"],[(263,254),"black"],[(263,236),"white"],[(263,218),"black"],
     [(281,227),"white"],[(281,245),"black"],[(281,263),"white"]]

for i in arr:
	r=coin(11, 1, 0.2, 0.8,i[0],i[1])
	
striker = coin(11, 1.1, 0, 0.8, (245,400), "green",True)

def check():
	r=10
	for i in coin.c:
		if (math.dist(i.body.position, (30,30))<=r) or (math.dist(i.body.position, (30,460))<=r) or (math.dist(i.body.position, (460,30))<=r) or (math.dist(i.body.position, (460,460))<=r):
		   i.body.velocity=(0,0)
		   i.body.position=(500,500)
		   i.status="out"

def map_range(old_val, old_min, old_max, new_min, new_max):
    new_val = float(((old_val - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min)
    if new_val>new_max:
    	return new_max
    else:
    	return new_val

def draw(bts=False):
	screen.fill("white")
	if bts:
		space.debug_draw(draw_options)
		pygame.draw.circle(screen,"red",(30,30),10)
		pygame.draw.circle(screen,"red",(30,460),10)
		pygame.draw.circle(screen,"red",(460,30),10)
		pygame.draw.circle(screen,"red",(460,460),10)
	else:
		screen.blit(bg,(0,0))
		for i in coin.c:
			pygame.draw.circle(screen,i.c,i.body.position,i.r)
			if i.c!="black" and i.s==False:
				pygame.draw.circle(screen,"black",i.body.position,i.r-2,2)
				pygame.draw.circle(screen,"black",i.body.position,i.r-7,1)
			elif i.s==True:
				continue
			else:
				pygame.draw.circle(screen,"white",i.body.position,i.r-2,2)
				pygame.draw.circle(screen,"white",i.body.position,i.r-7,1)
	if striker.a:
		x,y=pygame.mouse.get_pos()
		p=striker.body.position
		pygame.draw.line(screen,"black",striker.body.position,(x,y))
		pygame.draw.line(screen,"black",striker.body.position,(3*p[0]-2*x,3*p[1]-2*y))
		txt=font.render("force:"+str(int(f)), True, (255,255,255))
		screen.blit(txt, (10,0))
	else:
		ins=font.render("left click to aim and right click to move",True,"white")
		screen.blit(ins, (10,0))

def count():
	r,w,b=0,0,0
	for i in coin.c:
		if i.c=="red" and i.status=="in":
			r+=1
		if i.c=="white" and i.status=="in":
			w+=1
		if i.c=="black" and i.status=="in":
			b+=1
	coins=font.render("r:%i  w:%i  b:%i"%(r,w,b), True, "white")
	ins=font.render("press r,w,b to invoke coins to board",True,"white")
	sta="foul"if striker.status=="out" else "in"
	s=font.render("striker status: "+sta,True,"white")
	screen.blit(coins,(400,0))
	screen.blit(ins,(10,472))
	screen.blit(s,(390,472))

run=True
while run:
	d = math.dist(striker.body.position, pygame.mouse.get_pos())
	f = map_range(d, 0, 100, 0, 1500)
	for event in pygame.event.get():
		if event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()==(1,0,0):
			striker.a=True
		if event.type==pygame.MOUSEBUTTONUP:
			striker.a=False
			if event.button==1:
				x,y=(striker.body.position[0]-event.pos[0]),(striker.body.position[1]-event.pos[1])
				a=math.atan2(y, x)
				striker.body.apply_impulse_at_local_point((f*math.cos(a),f*math.sin(a)),(0,0))
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_r:
				for i in coin.c:
					if i.status=="out"and i.c=="red":
						i.body.position=(245,245)
						i.status="in"
			if event.key==pygame.K_w:
				for i in coin.c:
					if i.status=="out"and i.c=="white":
						i.body.position=(245,245)
						i.status="in"
						break
			if event.key==pygame.K_b:
				for i in coin.c:
					if i.status=="out"and i.c=="black":
						i.body.position=(245,245)
						i.status="in"
						break
		if event.type==pygame.QUIT:
			run=False
	if pygame.mouse.get_pressed()==(0,0,1) and striker.body.velocity==(0,0):
		striker.body.position=pygame.mouse.get_pos()
		striker.status="in"
	draw(bts=False)
	check()
	count()
	pygame.display.update()
	space.step(1/60)
	clock.tick(60)
pygame.quit()