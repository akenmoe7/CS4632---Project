import random
import time
import threading
import pygame
import sys

# Constants
DEFAULT_TIMERS = {
    "green": [10, 10, 10, 10],
    "yellow": 5,
    "red": 150,
}
SPEEDS = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}
VEHICLE_TYPES = list(SPEEDS.keys())
DIRECTIONS = ['right', 'down', 'left', 'up']

# Vehicle starting coordinates
START_COORDS = {
    'right': (0, 0, 0),
    'down': (755, 727, 697),
    'left': (1400, 1400, 1400),
    'up': (602, 627, 657),
}

STOP_LINES = {'right': 590, 'down': 330, 'left': 800, 'up': 535}

# Initialize Pygame
pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, index):
        self.green = DEFAULT_TIMERS["green"][index]
        self.yellow = DEFAULT_TIMERS["yellow"]
        self.red = DEFAULT_TIMERS["red"]
        self.is_yellow = False

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicle_type, direction):
        super().__init__(simulation)  # Add the vehicle to the simulation group
        self.lane = lane
        self.vehicle_type = vehicle_type
        self.speed = SPEEDS[vehicle_type]
        self.direction = direction
        self.image = pygame.image.load(f"images/{direction}/{vehicle_type}.png").convert_alpha()
        self.x, self.y = self.set_position()

    def set_position(self):
        if self.direction == 'right':
            return START_COORDS[self.direction][self.lane], 400
        elif self.direction == 'down':
            return 800, START_COORDS[self.direction][self.lane]
        elif self.direction == 'left':
            return START_COORDS[self.direction][self.lane], 400
        elif self.direction == 'up':
            return 800, START_COORDS[self.direction][self.lane]

    def move(self):
        if self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'up':
            self.y -= self.speed

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

def initialize_signals():
    return [TrafficSignal(i) for i in range(len(DIRECTIONS))]

def generate_vehicles():
    while True:
        vehicle_type = random.choice(VEHICLE_TYPES)
        lane = random.randint(0, 2)
        direction = random.choice(DIRECTIONS)
        Vehicle(lane, vehicle_type, direction)
        time.sleep(1)

class Simulation:
    def __init__(self):
        self.signals = initialize_signals()
        threading.Thread(target=generate_vehicles, daemon=True).start()

    def run(self):
        screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Traffic Simulation")
        clock = pygame.time.Clock()

        # Load background image
        background = pygame.image.load('images/intersection.png').convert()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(background, (0, 0))  # Draw background
            simulation.update()  # Update vehicle positions
            for vehicle in simulation:
                vehicle.move()
                vehicle.render(screen)

            pygame.display.flip()
            clock.tick(60)  # Maintain 60 FPS

if __name__ == "__main__":
    Simulation().run()


Traceback (most recent call last):
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 111, in <module>
    Simulation().run()
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 104, in run
    vehicle.move()
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 64, in move
    self.x -= self.speed
AttributeError: 'Vehicle' object has no attribute 'x'

