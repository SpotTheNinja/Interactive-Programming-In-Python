# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False



class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return list(self.center)

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def rotate(self,angle_vel):
        self.angle_vel = angle_vel
    
    def thrust_on(self,thrust):
        self.thrust = thrust
        if thrust:
            self.image_center[0]=135
            ship_thrust_sound.play()
            
        else:
            self.image_center[0] =45 #based on tiled image location
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    #dummy value from dictionary
    def shoot(self, dummy):
        
        
        
        missile_pos = angle_to_vector(self.angle)
        missile_pos[0] *= self.image_size[0]
        missile_pos[1]  *= self.image_size[1]
        missile_pos[0] += self.pos[0]
        missile_pos[1] += self.pos[1]
        
        missile_vel = [5,5]  #initial missile velocity, this could use some cleaning up
        missile_dir = angle_to_vector(self.angle)
        
        missile_vel[0] += math.sqrt(self.vel[0]**2 + self.vel[1]**2) 
        missile_vel[1] += math.sqrt(self.vel[0]**2 + self.vel[1]**2)                
        missile_vel[0] *= missile_dir[0]
        missile_vel[1] *= missile_dir[1]
        
        a_missile = Sprite( missile_pos,missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

        
    def update(self):
        self.pos[0] +=self.vel[0]
        self.pos[1] +=self.vel[1]
        self.angle  +=self.angle_vel
        
        c=.01
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)
        
        forward_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward_vector[0]*.1
            self.vel[1] += forward_vector[1]*.1
        
       
        
        if self.pos[0] > WIDTH:
            self.pos[0] =  0
            self.pos[1] = HEIGHT - self.pos[1] % HEIGHT 
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
            self.pos[1] = HEIGHT - self.pos[1] % HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0  
            self.pos[0] = WIDTH - self.pos[0] % WIDTH 
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
            self.pos[0] = WIDTH - self.pos[0] % WIDTH 
            
            
        

    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        #animated at 24 fps
        if self.animated:
            
         
                       
            print self.age
            self.image_center[0] += self.image_size[0]
            print self.image_center
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
                
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size, self.angle)
    
    def collide(self, another_sprite):
        pos_two = another_sprite.get_pos()
        distance = math.sqrt((self.pos[0]-pos_two[0])**2+(self.pos[1]-pos_two[1])**2)
        
        if distance < self.radius + another_sprite.get_radius():
            print "collision!"
            return True
            
        else:
            return False
    
    def update(self):
        
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[0] > WIDTH:
            self.pos[0] =  0
            self.pos[1] = HEIGHT - self.pos[1] % HEIGHT 
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
            self.pos[1] = HEIGHT - self.pos[1] % HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0  
            self.pos[0] = WIDTH - self.pos[0] % WIDTH 
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
            self.pos[0] = WIDTH - self.pos[0] % WIDTH 
            
        self.age +=1
        return self.age > self.lifespan #False if None value is present -> because float("inf")
         
def keydown(key):
    global a_missile
    inputs = {"left": my_ship.rotate,"right": my_ship.rotate,"up": my_ship.thrust_on, "space":my_ship.shoot}
    values = {"left":-.1,"right":.1,"up":True,"space":""}
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            inputs[i](values[i])
            

def keyup(key):
    inputs = {"left": my_ship.rotate,"right": my_ship.rotate, "up": my_ship.thrust_on}
    values = {"left":0,"right":0,"up":False}
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            inputs[i](values[i])

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, soundtrack, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True 
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()
            
def draw(canvas):
    global time, angle, lives, score, started, soundtrack
    
    
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, explosion_group)
    if group_collide(rock_group, my_ship):
        lives -=1
        if lives == 0:
            for i in range(len(rock_group)):
                rock_group.pop() #no set.clear() in this version
            
            soundtrack.pause()
            started = False
    
    score += group_group_collide(rock_group, missile_group)
    
    # update ship and sprites
    my_ship.update()   

    
    
    #draw score
    canvas.draw_text("Lives: " +str(lives), (2,18), 18, "White")
    canvas.draw_text("Score: " +str(score), (WIDTH -120,18),18,"White")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())    
            
# timer handler that spawns a rock    
def rock_spawner():
    global score
    x = 1+ score/1000 #work on this speed buff
    if started and len(rock_group) < 12:
        spawn_pos = [random.randrange(0,WIDTH),random.randrange(0,HEIGHT)]
        spawn_vel = [random.randrange(-10,10)*.1*x,random.randrange(-10,10)*.1*x]
        spawn_ang_vel =random.randrange(-10,11)*.01
        
        if math.sqrt((spawn_pos[0]-my_ship.get_pos()[0])**2 + (spawn_pos[1]-my_ship.get_pos()[1])**2)  > my_ship.get_radius() + asteroid_info.get_radius():
        
            a_rock = Sprite(spawn_pos, spawn_vel, 0, spawn_ang_vel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)

def process_sprite_group(canvas, sprite_group):
    
    for sprite in set(sprite_group):      
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)
            print explosion_info.get_center()

def group_collide(group, another_object):
    global explosion_group
    for sprite in set(group):
        if sprite.collide(another_object):
            group.remove(sprite)
            # need to create a new list to prevent messing with value inside class
            explosion = Sprite(sprite.get_pos(),[0,0],0,0,explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            return True

def group_group_collide(group, another_group):
    collisions = 0
    
    for sprite in set(another_group):
        if group_collide(group, sprite):
            collisions +=1
            another_group.discard(sprite) #because missiles have lifespan, discard is better
            
    collisions *= 100
    return collisions
            
        
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, rocks and missiles
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_keyup_handler(keyup)


timer = simplegui.create_timer(2000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()