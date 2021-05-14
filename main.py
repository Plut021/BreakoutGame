import pygame
import os
import random
import time

pygame.font.init()


WIDTH, HEIGHT = 2560, 1440
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Breakout")

# load images
BALL = pygame.image.load(os.path.join("assets", "ball.png"))
PLAYER = pygame.image.load(os.path.join("assets", "player.png"))
TOP_WALL = pygame.image.load(os.path.join("assets", "top_wall.png"))
WALL = pygame.image.load(os.path.join("assets", "wall.png"))
TILE = pygame.image.load(os.path.join("assets", "tile.png"))


# colors
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)


def main():
	starting = True
	run = True
	FPS = 60
	level = 1
	main_font = pygame.font.SysFont("comocsans", 100)
	clock = pygame.time.Clock()

	
	class TopWall:
		def __init__(self, x=50, y=50, img=TOP_WALL):
			self.x = x
			self.y = y
			self.img = img
			self.mask = pygame.mask.from_surface(self.img)

		def draw(self, window=WIN):
			self.pos = (self.x, self.y)
			window.blit(self.img, self.pos)


	class Wall:
		def __init__(self, x, y, img=WALL):
			self.x = x
			self.y = y
			self.img = img
			self.mask = pygame.mask.from_surface(self.img)

		def draw(self, window=WIN):
			self.pos = (self.x, self.y)
			window.blit(self.img, self.pos)



	class Tile:
		def __init__(self, x, y, img=TILE):
			self.x = x
			self.y = y
			self.img = img
			self.mask = pygame.mask.from_surface(self.img)


		def draw(self, window=WIN):
			self.pos = (self.x, self.y)
			window.blit(self.img, self.pos)

	class Ball:
		def __init__(self, x=(WIDTH-BALL.get_width())/2, y=HEIGHT-160, y_vel=-10, angles=(-20,20), img=BALL):
			self.x = x
			self.y = y
			self.x_vel = random.randint(angles[0],angles[1])
			self.y_vel = y_vel
			self.img = img
			self.mask = pygame.mask.from_surface(self.img)

		def draw(self,window=WIN):
			self.pos = (self.x,self.y)
			window.blit(self.img,self.pos)

		def move(self):
			self.x += self.x_vel
			self.y += self.y_vel

	class Player:
		def __init__(self, x=(WIDTH-PLAYER.get_width())/2, y=HEIGHT-100, speed=20, img=PLAYER, lives=3):
			self.x = x
			self.y = y
			self.speed = speed
			self.img = img
			self.mask = pygame.mask.from_surface(self.img)
			self.lives = lives

		def draw(self, window=WIN):
			self.pos = (self.x,self.y)
			window.blit(self.img, self.pos)
			self.lives_label = main_font.render(f"LIVES: {self.lives}", 1, WHITE)
			window.blit(self.lives_label, (WIDTH-100-self.lives_label.get_width(), HEIGHT-200))

		def lose_live(self):
			self.lives -= 1

	
	ball = Ball()
	player = Player()
	top_wall = TopWall()
	wall_r = Wall((WIDTH-WALL.get_width()-50), 50)
	wall_l = Wall(50,50)

	def ball_side_wall_colision(ball=ball, walls=[wall_l, wall_r]):
	 	for wall in walls:
	 		offset_x = int(wall.x - ball.x)
	 		offset_y = int(wall.y - ball.y)
	 		if ball.mask.overlap(wall.mask, (offset_x, offset_y)) != None:
	 			ball.x_vel = ball.x_vel * -1


	def ball_top_wall_colision(ball=ball, wall=top_wall):
		offset_x = int(wall.x - ball.x)
		offset_y = int(wall.y - ball.y)
		if ball.mask.overlap(wall.mask, (offset_x, offset_y)) != None:
	 		ball.y_vel = ball.y_vel * -1


	def player_colision(ball=ball, player=player):
	 	offset_x = int(ball.x - player.x)
	 	offset_y = int(ball.y - player.y)
	 	if player.mask.overlap(ball.mask, (offset_x, offset_y)) != None:
	 		ball.y_vel = ball.y_vel * -1


	def tile_colision(tiles, ball=ball):
		tile_remove_list = []
		for tile in tiles:
			offset_x = int(tile.x - ball.x)
			offset_y = int(tile.y - ball.y)
			if ball.mask.overlap(tile.mask, (offset_x, offset_y)) != None:
				ball.y_vel = ball.y_vel * -1
				tile_remove_list.append(tile)
		for tile in tile_remove_list:
			tiles.remove(tile)

	def generate_tiles():
		difficulty = 10 + 5 * level
		tile_list = [] 
		cords_list = []
		for i in range(difficulty):
			tile_generated = False
			while not tile_generated:
				x_cord = random.randint(1,19)
				y_cord = random.randint(1,25)
				pos_tuple = (x_cord, y_cord)
				if pos_tuple not in cords_list:
					cords_list.append(pos_tuple)
					tile = Tile(120*x_cord, 30*y_cord + 80)
					tile_generated = True
					tile_list.append(tile)
		return tile_list


	tile_list = generate_tiles()

	def draw_tiles(tile_list):
		for tile in tile_list:
			tile.draw()

	def display_label():
		level_label = main_font.render(f"LEVEL: {level}", 1, WHITE)
		WIN.blit(level_label, (100, HEIGHT-200))


	def draw_start_screen():
		pygame.draw.rect(WIN, BLACK,(0,0,WIDTH, HEIGHT))
		message = main_font.render("PRESS SPACE TO START", 1, BLUE)
		WIN.blit(message,(int((WIDTH-message.get_width())/2), int((HEIGHT-message.get_height())/2)))
		pygame.display.update()


	def redraw_window():
		pygame.draw.rect(WIN,BLACK,(0,0, WIDTH, HEIGHT))
		draw_tiles(tile_list)
		#collisoin check
		ball_side_wall_colision()
		ball_top_wall_colision()
		player_colision()
		tile_colision(tile_list)
		#ball update
		ball.move()
		ball.draw()
		#player update
		player.draw()
		if ball.y > player.y:
			player.lose_live()
			ball.x = (WIDTH-BALL.get_width())/2
			ball.y = HEIGHT-160
			ball.y_vel = ball.y_vel * -1
		#label update
		display_label()
		#draw bg
		top_wall.draw()
		wall_l.draw()
		wall_r.draw()

		pygame.display.update()


	while starting:
		clock.tick(int(FPS/2))
		draw_start_screen()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				starting = False
				run = False

		keys = pygame.key.get_pressed()
		for key in keys:
			if keys[pygame.K_SPACE]:
				starting = False



	while run:
		clock.tick(FPS)
		redraw_window()

		if player.lives == 0:
			pygame.draw.rect(WIN,BLACK,(0,0, WIDTH, HEIGHT))
			message = main_font.render("GAME OVER", 1, RED)
			WIN.blit(message, (int((WIDTH-message.get_width())/2),int((HEIGHT-message.get_height())/2)))
			pygame.display.update()
			time.sleep(5)
			run = False

		if len(tile_list) == 0:
			pygame.draw.rect(WIN,BLACK,(0,0, WIDTH, HEIGHT))
			level += 1
			message = main_font.render(f"YOU RECHED LEVEL {level}", 1, WHITE)
			WIN.blit(message, (int((WIDTH-message.get_width())/2),int((HEIGHT-message.get_height())/2)))
			pygame.display.update()
			time.sleep(5)
			tile_list = generate_tiles()

		

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_d] and player.x < WIDTH - 80 - player.img.get_width():
			player.x += player.speed

		if keys[pygame.K_a] and player.x > 80:
			player.x -= player.speed
main()