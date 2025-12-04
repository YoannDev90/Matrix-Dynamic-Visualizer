# Programme par S.Roux lycee Follereau Belfort : orion.france@gmail.com
# image de vecteurs de base par une application lineaire 2*2
# Modifie directement la matrice dans le programme.

import pygame
from pygame.locals import *
import numpy as np
import time

class LinearTransformationVisualizer:
    def __init__(self, width=1200, height=800, matrix=None, points=None):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.colors = [(0, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]  # green, orange, blue, purple
        self.offsetx = 400
        self.offsety = 300
        self.scale = 40

        # Default matrix
        if matrix is None:
            self.matrix = np.array([[2, 0], [0, 3]], dtype=float)
        else:
            self.matrix = np.array(matrix, dtype=float)

        # Default points (square)
        if points is None:
            self.points = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]], dtype=float)
        else:
            self.points = np.array(points, dtype=float)

        # Precompute transformed points
        self.transformed_points = self.matrix @ self.points

        # Adjust view to fit
        self.adjust_view()

        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)

        # Pre-render matrix display
        self._render_matrix_texts()

        # Controls text
        self.controls_text = self.font_small.render("Q/W: +/- M[0,0] | E/T: +/- M[0,1] | A/S: +/- M[1,0] | D/F: +/- M[1,1] | R:reset | fleches:deplacer | =/-:zoom | Espace:auto", True, self.black)

    def adjust_view(self):
        all_points = np.concatenate((self.points, self.transformed_points), axis=1)
        min_x = np.min(all_points[0])
        max_x = np.max(all_points[0])
        min_y = np.min(all_points[1])
        max_y = np.max(all_points[1])
        
        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1
        
        scale_x = (self.width * 0.8) / range_x
        scale_y = (self.height * 0.8) / range_y
        self.scale = min(scale_x, scale_y)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        self.offsetx = self.width / 2 - center_x * self.scale
        self.offsety = self.height / 2 - center_y * self.scale

    def _render_matrix_texts(self):
        self.t1 = self.font_medium.render("M=", True, self.black)
        self.t2 = self.font_large.render("(", True, self.black)
        self.t3 = self.font_large.render(")", True, self.black)
        self.texts = [
            self.font_medium.render(str(int(self.matrix[0, 0])), True, self.black),
            self.font_medium.render(str(int(self.matrix[0, 1])), True, self.black),
            self.font_medium.render(str(int(self.matrix[1, 0])), True, self.black),
            self.font_medium.render(str(int(self.matrix[1, 1])), True, self.black)
        ]

    def draw_axes(self):
        # Removed fixed axes, now handled by grid
        pass

    def draw_grid(self):
        # Calculate visible range
        left = -self.offsetx / self.scale
        right = (self.width - self.offsetx) / self.scale
        top = (self.height - self.offsety) / self.scale
        bottom = -self.offsety / self.scale
        
        # Vertical grid lines
        for x_grid in range(int(left), int(right) + 1):
            x_screen = x_grid * self.scale + self.offsetx
            if 0 <= x_screen <= self.width:
                color = (255, 0, 0) if x_grid == 0 else self.black
                width = 5 if x_grid == 0 else 1
                pygame.draw.line(self.screen, color, (x_screen, 0), (x_screen, self.height), width)
                # Add label at top
                label = self.font_small.render(str(x_grid), True, color)
                self.screen.blit(label, (x_screen - label.get_width() // 2, 5))
        
        # Horizontal grid lines
        for y_grid in range(int(bottom), int(top) + 1):
            y_screen = self.height - (y_grid * self.scale + self.offsety)
            if 0 <= y_screen <= self.height:
                color = (255, 0, 0) if y_grid == 0 else self.black  # red for x-axis
                width = 5 if y_grid == 0 else 1
                pygame.draw.line(self.screen, color, (0, y_screen), (self.width, y_screen), width)
                # Add label at left
                label = self.font_small.render(str(y_grid), True, color)
                self.screen.blit(label, (5, y_screen - label.get_height() // 2))

    def draw_original(self):
        for i in range(4):
            x1, y1 = self.points[0, i] * self.scale + self.offsetx, self.height - (self.points[1, i] * self.scale + self.offsety)
            x2, y2 = self.points[0, i+1] * self.scale + self.offsetx, self.height - (self.points[1, i+1] * self.scale + self.offsety)
            pygame.draw.line(self.screen, self.colors[i], (x1, y1), (x2, y2), 4)
            # Add coordinates
            coord_text = self.font_small.render(f"({int(self.points[0, i])},{int(self.points[1, i])})", True, self.colors[i])
            self.screen.blit(coord_text, (x1 + 5, y1 - 15))

    def draw_transformed(self):
        for i in range(4):
            x1, y1 = self.transformed_points[0, i] * self.scale + self.offsetx, self.height - (self.transformed_points[1, i] * self.scale + self.offsety)
            x2, y2 = self.transformed_points[0, i+1] * self.scale + self.offsetx, self.height - (self.transformed_points[1, i+1] * self.scale + self.offsety)
            pygame.draw.line(self.screen, self.colors[i], (x1, y1), (x2, y2), 4)
            # Add coordinates
            coord_text = self.font_small.render(f"({int(self.transformed_points[0, i])},{int(self.transformed_points[1, i])})", True, self.colors[i])
            self.screen.blit(coord_text, (x1 + 5, y1 - 15))

    def draw_matrix(self):
        base_y = self.height - 120
        base_x = self.width - 180
        # White background with padding
        bg_rect = pygame.Rect(base_x, base_y - 5, 170, 60)
        pygame.draw.rect(self.screen, self.white, bg_rect)
        shift_x = 60
        shift_internal = 40
        self.screen.blit(self.t1, (base_x + 10, base_y + 15))
        self.screen.blit(self.t2, (base_x + 50, base_y))
        self.screen.blit(self.texts[0], (base_x + shift_x + 10, base_y))
        self.screen.blit(self.texts[1], (base_x + shift_x + shift_internal + 10, base_y))
        self.screen.blit(self.texts[2], (base_x + shift_x + 10, base_y + 35))
        self.screen.blit(self.texts[3], (base_x + shift_x + shift_internal + 10, base_y + 35))
        self.screen.blit(self.t3, (base_x + shift_x + shift_internal + 40, base_y))

    def draw(self):
        self.screen.fill(self.white)
        self.draw_axes()
        self.draw_grid()
        self.draw_original()
        self.draw_transformed()
        self.draw_matrix()
        # White background for controls
        controls_bg = pygame.Rect(0, self.height - 35, self.width, 35)
        pygame.draw.rect(self.screen, self.white, controls_bg)
        self.screen.blit(self.controls_text, (10, self.height - 30))
        pygame.display.flip()

    def update_matrix(self, row, col, delta):
        self.matrix[row, col] += delta
        self.transformed_points = self.matrix @ self.points
        self.adjust_view()
        self._render_matrix_texts()

    def run(self):
        self.draw()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    world_x = (mx - self.offsetx) / self.scale
                    world_y = (self.height - my - self.offsety) / self.scale
                    if event.button == 4:  # wheel up
                        factor = 1.1
                    elif event.button == 5:  # wheel down
                        factor = 1 / 1.1
                    else:
                        continue
                    new_scale = self.scale * factor
                    self.offsetx = mx - world_x * new_scale
                    self.offsety = self.height - my - world_y * new_scale
                    self.scale = new_scale
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_r:
                        # Reset matrix
                        self.matrix = np.array([[1, 0], [0, 1]], dtype=float)
                        self.transformed_points = self.matrix @ self.points
                        self.adjust_view()
                        self._render_matrix_texts()
                    elif event.key == K_q:
                        self.update_matrix(0, 0, 1)
                    elif event.key == K_w:
                        self.update_matrix(0, 0, -1)
                    elif event.key == K_e:
                        self.update_matrix(0, 1, 1)
                    elif event.key == K_r:
                        pass  # r is already used for reset, maybe change
                    elif event.key == K_t:  # change r to t for [0,1] decrease
                        self.update_matrix(0, 1, -1)
                    elif event.key == K_a:
                        self.update_matrix(1, 0, 1)
                    elif event.key == K_s:
                        self.update_matrix(1, 0, -1)
                    elif event.key == K_d:
                        self.update_matrix(1, 1, 1)
                    elif event.key == K_f:
                        self.update_matrix(1, 1, -1)
                    elif event.key == K_LEFT:
                        self.offsetx += 20
                    elif event.key == K_RIGHT:
                        self.offsetx -= 20
                    elif event.key == K_UP:
                        self.offsety += 20
                    elif event.key == K_DOWN:
                        self.offsety -= 20
                    elif event.key == K_EQUALS or event.key == K_KP_PLUS:
                        self.scale *= 1.1
                    elif event.key == K_MINUS or event.key == K_KP_MINUS:
                        self.scale /= 1.1
                    elif event.key == K_SPACE:
                        self.adjust_view()
            self.draw()
        pygame.quit()

# Usage
if __name__ == "__main__":
    visualizer = LinearTransformationVisualizer()
    visualizer.run()
