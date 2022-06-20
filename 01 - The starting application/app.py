import pygame
import time 

WIDTH, HEIGHT = 480, 640
SCALE = 2
SCALE_WIDTH, SCALE_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE
FPS = 60


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

		def on_event(self, event):
			 if event.type == pygame.QUIT:
				 self._running = False
		def on_loop(self):
			 pass
		def on_render(self):
			 pass
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