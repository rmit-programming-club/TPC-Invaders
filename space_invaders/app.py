import pygame, time



# Constants

## FPS
FPS = 144

## Window dimensions
WIDTH, HEIGHT = 480, 640
SCALE = 1.3
SCALE_WIDTH, SCALE_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE

# Main Application class
class App():

  # Initialize varibles for Application Class
  def __init__(self):
    # Clock for FPS limiting
    self.clock = pygame.time.Clock()

    # Time for delta time
    self.dt = 0
    self.prev_time = time.time()
    
    # Pygame varibles
    self.running = True
    self._display_surf = None
    self.size = self.weight, self.height = SCALE_WIDTH, SCALE_HEIGHT


  def on_init(self):

    #Pygame Surface initialisation
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self._running = True

    #Game Logic
    self.level = Level()
    self.player = Player()

  # Handle events
  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False



  def on_loop(self):
    self.clock.tick(FPS)
    print(self.clock.get_fps())
    self.now = time.time()
    self.dt = self.now - self.prev_time
    self.prev_time = self.now

    ## GAME LOGIC GOES HERE
    self.player.on_input(self.dt, pygame.key.get_pressed())

    self.player.on_loop(self.dt)
    self.level.on_loop(self.dt)

  # blit render layers to screen surface
  def on_render(self):
    self._display_surf.blit(*self.level.get_surface())
    self._display_surf.blit(*self.player.get_surface())
    #update display
    pygame.display.update()


  def on_cleanup(self):
    del self.player
    del self.background
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    while ( self._running ):
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()
  
class Level():

  def __init__(self):
    self.background = pygame.image.load("sprites/Space_BG (2 frames) (64 x 64).png").convert()
    self.background_a = self.background.subsurface((0,0, 64, 64))
    self.background_b = self.background.subsurface((64,0, 64, 64))
    self.timer = 0
    #self.background = pygame.transform.scale(self.background, (480, 640))


  def get_surface(self):
    self.surface = pygame.Surface((WIDTH,HEIGHT))
    for y in range(0, int(HEIGHT/64)):
      for x in range(0, int(WIDTH/64) + 64):
        if x * y % 2 == 0:
          self.surface.blit(pygame.transform.rotate(self.background_a, 90 * x), (x * 64, y*64))
        else:
          self.surface.blit(pygame.transform.rotate(self.background_b, 90 * y), (x * 64, y*64))

    self.surface = pygame.transform.scale(self.surface, (SCALE_WIDTH, SCALE_HEIGHT))
    self.surface.blit(self.background, (0,0))
    return self.surface, (0,0)

  def on_loop(self, dt):
    if time.time():
      self.timer = self.timer + 1
      if self.timer == 200:
        self.background_a, self.background_b = self.background_b, self.background_a
        self.timer = 0


class Player():
  
  def __init__(self):
    self.x, self.y = (SCALE_WIDTH/2) - 32,(4/5) * SCALE_HEIGHT
    
    #Load the sprite sheet
    self.sprite = pygame.image.load("sprites/Player_ship (16 x 16).png").convert()
    #Get the individual sprites
    self.player_sprite_n = self.sprite.subsurface((16, 0,16,16))
    self.player_sprite_r = self.sprite.subsurface((32,0,16,16))
    self.player_sprite_l = self.sprite.subsurface((0,0,16,16))
    #scale the sprites
    self.player_sprite_n = pygame.transform.scale(self.player_sprite_n, (64 * SCALE, 64 * SCALE))
    self.player_sprite_r = pygame.transform.scale(self.player_sprite_r, (64 * SCALE, 64 * SCALE))
    self.player_sprite_l = pygame.transform.scale(self.player_sprite_l, (64 * SCALE, 64 * SCALE))
    #set the current sprite
    self.player_sprite_current = self.player_sprite_n
    self.velocity = 0
    self.speed = 200 * SCALE

  def get_surface(self):
    return self.player_sprite_current, (self.x, self.y)

  def on_input(self, dt, input):
    if input[pygame.K_RIGHT]:
      self.velocity = 1
      self.player_sprite_current = self.player_sprite_r
    elif input[pygame.K_LEFT]:
      self.velocity = -1
      self.player_sprite_current = self.player_sprite_l
    else:
      self.player_sprite_current = self.player_sprite_n
      self.velocity = 0
    

  def on_loop(self, dt):
    dx = self.speed * self.velocity * dt
    if (self.velocity == -1 and self.x > 0) or (self.velocity == 1 and self.x < WIDTH-64):
      self.x += dx


if __name__ == "__main__":
  app = App()
  app.on_execute()