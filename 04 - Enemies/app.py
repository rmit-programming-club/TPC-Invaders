import pygame
import time 

WIDTH, HEIGHT = 480, 540
SCALE = 1.5
SCALE_WIDTH, SCALE_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE
FPS = 60


spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.load_sprites()
    self.image = self.player_sprite_n
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.last_shot = pygame.time.get_ticks()
    
  def load_sprites(self):
    #Load the sprite sheet
    self.sprites = pygame.image.load("sprites/Player_ship (16 x 16).png").convert_alpha()
    #Get the individual sprites
    self.player_sprite_n = self.sprites.subsurface((16, 0,16,16))
    self.player_sprite_r = self.sprites.subsurface((32,0,16,16))
    self.player_sprite_l = self.sprites.subsurface((0,0,16,16))
      #scale the sprites
    self.player_sprite_n = pygame.transform.scale(self.player_sprite_n, (32, 32))
    self.player_sprite_r = pygame.transform.scale(self.player_sprite_r, (32, 32))
    self.player_sprite_l = pygame.transform.scale(self.player_sprite_l, (32, 32))

  # Call every game update
  def update(self, dt, time_now):
    #set movement speed
    speed = 250
    #set a cooldown variable
    cooldown = 500 #milliseconds
    dx = 0

    #get key press for movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      dx = -1 #Set the direction delta
      self.image = self.player_sprite_l # Set the Sprite
    elif key[pygame.K_RIGHT] and self.rect.right < WIDTH:
      dx = 1 #Set the direction delta
      self.image = self.player_sprite_r # Set the Sprite
    else:
      dx = 0 #Set the direction delta
      self.image = self.player_sprite_n # Set the Sprite

    # Move the ship
    self.rect.x += dx * speed * dt


class Alien(pygame.sprite.Sprite):
  def __init__(self, x, y, dir=1, speed=5):
    pygame.sprite.Sprite.__init__(self)
    self.load_sprite()
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.speed = speed
    self.dir = dir
    self.timer = 0


  def load_sprite(self):
    self.image_sheet = pygame.image.load("sprites/Alan (16 x 16).png").convert_alpha()
    self.dir = 1
    self.sprites = []
    self.sprites.append(self.image_sheet.subsurface((48,0,16,16)))
    self.sprites.append(self.image_sheet.subsurface((64,0,16,16)))
    self.sprites.append(self.image_sheet.subsurface((80,0,16,16)))

    for i in range(len(self.sprites)):
      self.sprites[i] = pygame.transform.scale(self.sprites[i], (32,32))

    self.image = self.sprites[0]
    self.image_index = 0

  def update(self, dt, time_now):

    if time_now - self.timer >= 300:
      self.image_index += 1
      if self.image_index >= len(self.sprites):
        self.image_index = 0
      self.image = self.sprites[self.image_index]
      self.timer = time_now 


class Level():

  def __init__(self):
    self.background = pygame.image.load("sprites/Space_BG (2 frames) (64 x 64).png").convert_alpha()
    background_a = self.background.subsurface((0,0, 64, 64))
    background_b = self.background.subsurface((64,0, 64, 64))
    self.background_a = self.create_surface(background_a, background_b)
    self.background_b = self.create_surface(background_b, background_a)
    self.timer = 0
    
  def create_aliens(self,rows, cols, alien_group):
    for row in range(rows):
      for item in range(cols):
        alien = Alien(80 + item * 64, 100 + row * 64)
        alien_group.add(alien)
    return alien_group


  def create_surface(self, a, b):
    self.surface = pygame.Surface((WIDTH,HEIGHT))
    for y in range(0, int(HEIGHT/64) + 64):
      for x in range(0, int(WIDTH/64) + 64):
        if x * y % 2 == 0:
          self.surface.blit(pygame.transform.rotate(a, 90 * x), (x * 64, y*64))
        else:
          self.surface.blit(pygame.transform.rotate(b, 90 * x), (x * 64, y*64))

    self.surface.blit(self.background, (0,0))
    return self.surface

  
  def get_surface(self):
    return (self.background_a, (0,0))
  
  def on_loop(self, time_now):
    if time_now - self.timer > 1500:
      self.timer = time_now
      self.background_a, self.background_b = self.background_b, self.background_a



class App:

    def __init__(self):
      # Clock for FPS limiting
      self.clock = pygame.time.Clock()

      # Time for delta time
      self.dt = 0
      self.prev_time = time.time()
      global GAME_OVER
      GAME_OVER = False

      # Pygame varibles
      self.running = True
      self._display_surf = None
      self.size = self.weight, self.height = SCALE_WIDTH, SCALE_HEIGHT


    def on_init(self):
      pygame.init()
      self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
      self._running = True
      # Create the level
      self.level = Level()
      # Create the spaceship
      ship = Spaceship(WIDTH/2, HEIGHT-64)
      self.spaceship_group = spaceship_group
      self.spaceship_group.add(ship)
      # Create the aliens
      self.alien_group = alien_group
      self.alien_group = self.level.create_aliens(6, 6, self.alien_group)
    

      
    def on_event(self, event):
       if event.type == pygame.QUIT:
         self._running = False
    
    def on_loop(self):
      self.clock.tick(FPS)
      self.now = time.time()
      self.dt = self.now - self.prev_time
      self.prev_time = self.now
      self.time_now = pygame.time.get_ticks();

      self.spaceship_group.update(self.dt, self.time_now)
      self.alien_group.update(self.dt, self.time_now)
      self.level.on_loop(self.time_now)


    def on_render(self):
      #create a temp buffer
      temp_buffer = pygame.surface.Surface((WIDTH, HEIGHT))
      temp_buffer.blit(*self.level.get_surface())
      self.spaceship_group.draw(temp_buffer)
      self.alien_group.draw(temp_buffer)
      #Scale the buffer
      temp_buffer = pygame.transform.scale(temp_buffer, (SCALE_WIDTH, SCALE_HEIGHT))
      #blit it to the display surface
      self._display_surf.blit(temp_buffer,(0,0))
      #update the pygame display
      pygame.display.update()
      
    def on_cleanup(self):
       pygame.quit()

    def on_execute(self):
       if self.on_init() == False:
         self._running = False

       while( self._running ):
         for event in pygame.event.get():
            self.on_event(event)
         self.on_loop()
         self.on_render()
       self.on_cleanup()

if __name__ == "__main__" :
  theApp = App()
  theApp.on_execute()
#
