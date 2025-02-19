import pygame
import math

# var
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 50
FOV = math.pi / 3  
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

#Graphics (This can affect preformance alot but makes it look alot better. )
NUM_RAYS = 800  # Number of rays. Affects how full the walls are Max:800 (<=200:Fast, 400: Half full, 800:Full)
STEP_SIZE = 0.05  # Smoothness (<=0.1:Jagged, 0.1:Semi Jagged, 0.02:Semi Smooth, 0.01:Smooth=>)
FOG_DENSITY = 0.5 # Little affect on preformance
#colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

# Create the map
MAP = [
    "2222222444444444444444444444444444444444444444444",
    "2.....2............3........................2...4",
    "2.....2.....................................#.3.3",
    "2.....2....................3................3..25",
    "2.....2............3........................#1..5",
    "2.....2.......536..5353.....................5...5",
    "222..22.......5.......#3#321#..34555#2#1#1#2#..55",
    "4.....#.......5.................................4",
    "#.....3.......3.................................4",
    "4.....3.......3...............................154",
    "5.....3.......5.......1.....................5.2.1",
    "#.....3334#4466.......2.....................#1#.1",
    "5.....................3......................5..2",
    "5.....................4......................2..2",
    "5.....................5......................1..3",
    "666112231456665.......1234......................4",
    "4.............4..........5......................5",
    "#.............3..........1......................4",
    "3.............2.......3..2......................3",
    "#.............1.......2..3.........1..1.........2",
    "3.............54...4351..4.........1..1.........1",
    "#...................2....5.......111..111.......2",
    "3...................154321.......1......1.......2",
    "4................................1......1.......2",
    "5................................11111111.......4",
    "#...................#...........................4",
    "333#3331333323333333333333133333533433333233323333"
]

# Colors for map
WALL_COLORS = {
    "#": GRAY,
    "1": RED,
    "2": BLUE,
    "3": GREEN,
    "4": ORANGE,
    "5": PURPLE,
    "6": CYAN
}


class Raycaster:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("crzy Raycaster")

    def draw_walls(self, player_pos, player_angle):
        x, y = player_pos
        angle = player_angle - FOV / 2
        for ray in range(NUM_RAYS):
            angle += FOV / NUM_RAYS
            distance_to_wall = 0
            hit_wall = False
            eye_x = math.sin(angle)
            eye_y = math.cos(angle)
            while not hit_wall and distance_to_wall < 20:
                distance_to_wall += STEP_SIZE
                test_x = int(x + eye_x * distance_to_wall)
                test_y = int(y + eye_y * distance_to_wall)
                if test_x < 0 or test_x >= len(MAP[0]) or test_y < 0 or test_y >= len(MAP):
                    hit_wall = True
                    distance_to_wall = 20
                else:
                    if MAP[test_y][test_x] in WALL_COLORS:
                        hit_wall = True
            ceiling = HEIGHT // 2 - HEIGHT // distance_to_wall
            floor = HEIGHT - ceiling
            wall_color = WALL_COLORS.get(MAP[test_y][test_x], WHITE)
            fog_color = (
                int(wall_color[0] * (1 - FOG_DENSITY * distance_to_wall / 20)),
                int(wall_color[1] * (1 - FOG_DENSITY * distance_to_wall / 20)),
                int(wall_color[2] * (1 - FOG_DENSITY * distance_to_wall / 20))
            )
            ray_x = int(ray * WIDTH / NUM_RAYS)
            pygame.draw.line(self.screen, fog_color, (ray_x, ceiling), (ray_x, floor))

    def run(self):
        player_pos = [4.5, 4.5]  
        player_angle = 0
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_angle -= 0.1
            if keys[pygame.K_RIGHT]:
                player_angle += 0.1
            if keys[pygame.K_UP]:
                new_pos = (
                    player_pos[0] + math.sin(player_angle) * 0.1,
                    player_pos[1] + math.cos(player_angle) * 0.1
                )
                if not self.check_collision(new_pos):
                    player_pos[0], player_pos[1] = new_pos
            if keys[pygame.K_DOWN]:
                new_pos = (
                    player_pos[0] - math.sin(player_angle) * 0.1,
                    player_pos[1] - math.cos(player_angle) * 0.1
                )
                if not self.check_collision(new_pos):
                    player_pos[0], player_pos[1] = new_pos

            self.screen.fill(BLACK)
            self.draw_walls(player_pos, player_angle)
            pygame.display.flip()
            clock.tick(30)

    def check_collision(self, pos):
        x, y = pos
        grid_x = int(x)
        grid_y = int(y)
        if MAP[grid_y][grid_x] in WALL_COLORS:
            return True  
        return False  


if __name__ == "__main__":
    Raycaster().run()
