import random
import time
import threading
import pygame
import sys

# Default values of signal timers
defaultGreen = {0:10, 1:10, 2:10, 3:10}
defaultRed = 150
defaultYellow = 5

signals = []
noOfSignals = 4
currentGreen = 0
nextGreen = (currentGreen+1)%noOfSignals
currentYellow = 0

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':3.0}  # Increased bike speed from 2.5 to 3.0

# Coordinates of vehicles' start
x = {'right':[0]*3, 'down':[755,727,697], 'left':[1400]*3, 'up':[602,627,657]}    
y = {'right':[348,370,398], 'down':[0]*3, 'left':[498,466,436], 'up':[800]*3}

vehicles = {direction: {lane: [] for lane in range(3)} | {'crossed': 0} for direction in ['right', 'down', 'left', 'up']}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Gap between vehicles
stoppingGap = movingGap = 15

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        super().__init__()
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        
        
        
        # Create a 4x4 pixel surface for the vehicle
        self.image = pygame.Surface(10, 10)
        if vehicleClass == 'bike':
            self.image.fill(0, 0, 255)  # Blue for bike
        elif vehicleClass == 'bus':
            self.image.fill(255, 255, 0)  # Yellow for bus
        elif vehicleClass == 'car':
            self.image.fill(255, 0, 0)  # Red for car
        else:  # truck
            self.image.fill(0, 255, 0)  # Green for truck

            
        # Set new starting coordinate
        if direction in ['right', 'left']:
            x[direction][lane] += (-1 if direction == 'right' else 1) * stoppingGap
        else:
            y[direction][lane] += (-1 if direction == 'down' else 1) * stoppingGap
        simulation.add(self)


    def move(self):
        if not self.crossed and (self.direction == 'right' and self.x > stopLines[self.direction] or
                                 self.direction == 'down' and self.y > stopLines[self.direction] or
                                 self.direction == 'left' and self.x < stopLines[self.direction] or
                                 self.direction == 'up' and self.y < stopLines[self.direction]):
            self.crossed = 1
        
        if ((self.crossed == 1 or 
             (self.direction in ['right', 'down'] and getattr(self, 'x' if self.direction == 'right' else 'y') <= self.stop) or
             (self.direction in ['left', 'up'] and getattr(self, 'x' if self.direction == 'left' else 'y') >= self.stop) or
             (currentGreen == self.direction_number and currentYellow == 0)) and 
            (self.index == 0 or self.check_distance())):
            setattr(self, 'x' if self.direction in ['right', 'left'] else 'y', 
                    getattr(self, 'x' if self.direction in ['right', 'left'] else 'y') + self.speed * (1 if self.direction in ['right', 'down'] else -1))


def initialize():
    for i in range(noOfSignals):
        signals.append(TrafficSignal(defaultRed, defaultYellow, defaultGreen[i]))
        if i == 0:
            signals[i].red = 0
        elif i == 1:
            signals[i].red = defaultGreen[0] + defaultYellow
    repeat()

def repeat():
    global currentGreen, currentYellow, nextGreen
    while signals[currentGreen].green > 0:
        updateValues()
        time.sleep(1)
    currentYellow = 1
    for lane in range(3):
        for vehicle in vehicles[directionNumbers[currentGreen]][lane]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]] #stop based on direction and if green
    while signals[currentGreen].yellow > 0: 
        updateValues()
        time.sleep(1) #count
    currentYellow = 0
    
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed
       
    currentGreen = nextGreen
    nextGreen = (currentGreen+1)%noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green
    repeat()

def updateValues():
    for i in range(noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1

def generateVehicles():
    while True:
        vehicle_type = random.randint(0,3)
        lane_number = random.randint(1,2)
        direction_number = random.choices(range(4), weights=[25,25,25,25])[0]
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)

class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, daemon=True)
    thread1.start()

    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, daemon=True)
    thread2.start()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0)) #background of intersection
        for i in range(noOfSignals):
            if i == currentGreen:
                screen.blit(yellowSignal if currentYellow else greenSignal, signalCoods[i])
                signals[i].signalText = signals[i].yellow if currentYellow else signals[i].green
            else:
                screen.blit(redSignal, signalCoods[i])
                signals[i].signalText = signals[i].red if signals[i].red <= 10 else "---"
            
            signalText = font.render(str(signals[i].signalText), True, (255,255,255), (0,0,0))
            screen.blit(signalText, signalTimerCoods[i])

        for vehicle in simulation:  
            vehicle.render(screen)
            vehicle.move()

        pygame.display.update()
        clock.tick(60)  # 60 FPS

Main()
