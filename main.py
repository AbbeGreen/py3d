import pygame
import sys
import numpy as np
from pygame.locals import *

GREEN = (50, 170, 70)
BLACK = (0, 0, 0)
PURPLE = (170, 40, 170)
GREY = (40, 40, 40)

pygame.init()

WIDTH, HEIGHT = 800, 800

theta = 1

window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(GREEN)

scale = 20
pos = [WIDTH/2, HEIGHT/2]

projection_matrix = [[1, 0, 0],
					 [0, 1, 0], 
					 [0, 0, 0]]

scale_factor = 1
translation_step_x = 0
translation_step_z = -1
zoom_factor = 1

# Better projection
fnear = 0.1
ffar = 100.0
ffov = 90.0
aspect_ratio = HEIGHT/WIDTH
ffov_rad = 1.0 / np.tan(ffov * 0.5 * np.pi / 180.0)
z_scaling = ffar / (ffar - fnear)
z_offset = -(ffar * fnear) / (ffar - fnear)

proj_mat = [[aspect_ratio * ffov_rad, 0, 0, 0],
			[0, ffov_rad, 0, 0],
			[0, 0, z_scaling, -1],
			[0, 0, z_offset, 0]]



points = [n for n in range(9)]
points[0] = [[-1], [-1], [1], [1]]
points[1] = [[1], [-1], [1], [1]]
points[2] = [[1], [1], [1], [1]]
points[3] = [[-1], [1], [1], [1]]
points[4] = [[-1], [-1], [-1], [1]]
points[5] = [[1], [-1], [-1], [1]]
points[6] = [[1], [1], [-1], [1]]
points[7] = [[-1], [1], [-1], [1]]
points[8] = [[0], [0], [0], [1]]

proj_points = [[0]*len(points[0]) for i in range(len(points))]

while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	if theta < np.pi*2:
		theta +=  np.pi/1080
	elif theta >= np.pi*2:
		theta = 0

	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]:
		translation_step_z -= 0.01
	elif pressed[pygame.K_DOWN]:
		translation_step_z += 0.01 
	elif pressed[pygame.K_RIGHT]:
		translation_step_x -= 0.01
	elif pressed[pygame.K_LEFT]:
		translation_step_x += 0.01

	window.fill(BLACK)

	rotation_matrix_x = [[1, 0, 0, 0],
				     [0, np.cos(theta), -np.sin(theta), 0],
				     [0, np.sin(theta), np.cos(theta), 0],
				     [0, 0, 0, 0]]

	scaling_matrix = [[scale_factor, 0, 0, 0],
					  [0, scale_factor, 0, 0],
					  [0, 0, scale_factor, 0],
					  [0, 0, 0, 0]]

	translate_x = [[1, 0, 0, translation_step_x],
				   [0, 1, 0, 0],
				   [0, 0, 1, 0],
				   [0, 0, 0, 1]]
	translate_z = [[1, 0, 0, 0],
				   [0, 1, 0, 0],
				   [0, 0, 1, translation_step_z],
				   [0, 0, 0, 1]]

	print(translation_step_z)

	for i in range(len(points)):

		sr = np.dot(scaling_matrix, rotation_matrix_x)


		srt_x = np.dot(scaling_matrix, translate_x)
		srt_xz = np.dot(srt_x, translate_z)
		#translation_step_z = -2;

		transformed2d = np.dot(srt_xz, points[i])
		rotated = np.dot(rotation_matrix_x, transformed2d)


		projected2d = np.dot(proj_mat, transformed2d)
		w = projected2d[3][0]
		#zoom_factor = projected2d[2][0]

		if projected2d[3][0] != 1:
			projected2d[0][0] /= (w/2)
			projected2d[1][0] /= (w/2)
			projected2d[2][0] /= (w/2)
		x = projected2d[0][0] * scale + pos[0]
		y = projected2d[1][0] * scale + pos[1]
		proj_points[i][0] = x
		proj_points[i][1] = y
		pygame.draw.circle(window, GREEN, (x, y), 1 / -w)
		#pygame.draw.line(window, BLACK, (proj_points[0][0], proj_points[0][1]), (proj_points[3][1], proj_points[4][1]), 2)
	#zoom_factor = proj_points[8][2]
	for j in range(len(proj_points)):
		for k in range(len(proj_points)):
			pygame.draw.line(window, GREEN, (proj_points[j][0], proj_points[j][1]),
										    (proj_points[k][0], proj_points[k][1]), 3)


	pygame.display.update()