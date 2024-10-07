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
STOP_GAP = 10

# Initialize Pygame
pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, index):
        self.green_time = DEFAULT_TIMERS["green"][index]
        self.yellow_time = DEFAULT_TIMERS["yellow"]
        self.red_time = DEFAULT_TIMERS["red"]
        self.current_time = self.green_time
        self.is_green = True
        self.index = index

    def update(self):
        if self.current_time > 0:
            self.current_time -= 1
        else:
            self.change_signal()

    def change_signal(self):
        if self.is_green:
            self.is_green = False
            self.current_time = self.yellow_time
        elif self.current_time == 0:
            self.is_green = not self.is_green
            self.current_time = self.green_time if self.is_green else self.red_time

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicle_type, direction):
        super().__init__(simulation)
        self.lane = lane
        self.vehicle_type = vehicle_type
        self.speed = SPEEDS[vehicle_type]
        self.direction = direction
        self.image = pygame.image.load(f"images/{direction}/{vehicle_type}.png").convert_alpha()
        self.x, self.y = self.set_position()
        self.crossed_stop_line = False

    def set_position(self):
        if self.direction == 'right':
            return START_COORDS[self.direction][self.lane], 400
        elif self.direction == 'down':
            return 800, START_COORDS[self.direction][self.lane]
        elif self.direction == 'left':
            return START_COORDS[self.direction][self.lane], 400
        elif self.direction == 'up':
            return 800, START_COORDS[self.direction][self.lane]

    def move(self, signal):
        if signal.is_green:
            if self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'down':
                self.y += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'up':
                self.y -= self.speed
        else:
            # Stop the vehicle at the stop line
            if self.direction == 'right' and self.x < STOP_LINES['right']:
                self.x = STOP_LINES['right'] - STOP_GAP
            elif self.direction == 'down' and self.y < STOP_LINES['down']:
                self.y = STOP_LINES['down'] - STOP_GAP
            elif self.direction == 'left' and self.x > STOP_LINES['left']:
                self.x = STOP_LINES['left'] + STOP_GAP
            elif self.direction == 'up' and self.y > STOP_LINES['up']:
                self.y = STOP_LINES['up'] + STOP_GAP

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
        self.current_signal_index = 0

    def run(self):
        screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Traffic Simulation")
        clock = pygame.time.Clock()
        background = pygame.image.load('images/intersection.png').convert()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update signals
            for signal in self.signals:
                signal.update()

            # Draw everything
            screen.blit(background, (0, 0))  # Draw background
            for signal in self.signals:
                if signal.is_green:
                    pygame.draw.circle(screen, (0, 255, 0), (100 + signal.index * 200, 100), 20)  # Green signal
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (100 + signal.index * 200, 100), 20)  # Red signal

            for vehicle in simulation:
                vehicle.move(self.signals[vehicle.lane])
                vehicle.render(screen)

            pygame.display.flip()
            clock.tick(60)  # Maintain 60 FPS

if __name__ == "__main__":
    Simulation().run()


Traceback (most recent call last):
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 149, in <module>
    Simulation().run()
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 142, in run
    vehicle.move(self.signals[vehicle.lane])
  File "/Users/andy/Basic-Traffic-Intersection-Simulation/Basic-Traffic-Intersection-Simulation/simulation.py", line 83, in move
    self.x -= self.speed
AttributeError: 'Vehicle' object has no attribute 'x'
