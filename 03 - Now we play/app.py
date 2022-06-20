import pygame
import time 

WIDTH, HEIGHT = 480, 640
SCALE = 1.5
SCALE_WIDTH, SCALE_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE
FPS = 60


class Level():

  def __init__(self):
    self.background = pygame.image.load("sprites/Space_BG (2 frames) (64 x 64).png").convert_alpha()
    background_a = self.background.subsurface((0,0, 64, 64))
    background_b = self.background.subsurface((64,0, 64, 64))
    self.background_a = self.create_surface(background_a, background_b)
    self.background_b = self.create_surface(background_b, background_a)
    self.timer = 0
    

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
    print(time_now - self.timer)
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
    

      
    def on_event(self, event):
       if event.type == pygame.QUIT:
         self._running = False
    
    def on_loop(self):
      self.time_now = pygame.time.get_ticks()

      self.level.on_loop(self.time_now)

    def on_render(self):
      #create a temp buffer
      temp_buffer = pygame.surface.Surface((WIDTH, HEIGHT))
      temp_buffer.blit(*self.level.get_surface())
      
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