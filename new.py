"""Coded by Suyash Thamake"""
import pygame
import random
import sys
import time
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)  # White background
BORDER_COLOR = (0, 0, 0)  # Black border color
BORDER_THICKNESS = 5  # Thinner border
ENTITY_SIZE = 20
ENTITY_SPEED = 5
FOOD_SIZE = 10
THREAT_SIZE = 20
CHANGE_DIRECTION_PROB = 0.01  # Lower probability to change direction
MAX_THREATS = 6
INITIAL_ENERGY = 5
TIME_PERIOD = 30  # Time period for collision tracking (30 seconds)
AVOIDANCE_RADIUS = 40  # Distance within which entity starts avoiding threats

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Entity Evolution')

def draw_border():
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)

def spawn_food():
    x = random.randint(BORDER_THICKNESS, WIDTH - FOOD_SIZE - BORDER_THICKNESS)
    y = random.randint(BORDER_THICKNESS, HEIGHT - FOOD_SIZE - BORDER_THICKNESS)
    food = pygame.sprite.Sprite()
    food.image = pygame.Surface((FOOD_SIZE, FOOD_SIZE))
    food.image.fill((0, 255, 0))  # Green food
    food.rect = food.image.get_rect()
    food.rect.x = x
    food.rect.y = y
    return food

def spawn_threats():
    threats = pygame.sprite.Group()
    for _ in range(MAX_THREATS):
        x = random.randint(BORDER_THICKNESS, WIDTH - THREAT_SIZE - BORDER_THICKNESS)
        y = random.randint(BORDER_THICKNESS, HEIGHT - THREAT_SIZE - BORDER_THICKNESS)
        threat = pygame.sprite.Sprite()
        threat.image = pygame.Surface((THREAT_SIZE, THREAT_SIZE))
        threat.image.fill((255, 0, 0))  # Red threat
        threat.rect = threat.image.get_rect()
        threat.rect.x = x
        threat.rect.y = y
        threats.add(threat)
    return threats

class Entity(pygame.sprite.Sprite):
    def __init__(self, color, x, y, gender=None):
        super().__init__()
        self.image = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.choice([-ENTITY_SPEED, ENTITY_SPEED])
        self.speed_y = random.choice([-ENTITY_SPEED, ENTITY_SPEED])
        self.energy = INITIAL_ENERGY
        self.gender = gender if gender is not None else random.choice(['male', 'female'])
        self.avoid_threats = {}  # Store threat encounters and their location
        self.collision_count = 0

    def update(self):
        # Randomly change direction
        if random.random() < CHANGE_DIRECTION_PROB:
            self.speed_x = random.choice([-ENTITY_SPEED, ENTITY_SPEED])
            self.speed_y = random.choice([-ENTITY_SPEED, ENTITY_SPEED])

        # Update movement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ensure proper wall bounce after any collision
        self.bounce_off_walls()

        # Check for collision with food
        for food in food_sprites:
            if self.rect.colliderect(food.rect):
                food.kill()  # Remove food
                self.energy += 2  # Increase energy
                food_sprites.add(spawn_food())  # Spawn new food
                break  # Only interact with one food at a time

        # Check for collision with threats
        for threat in threat_sprites:
            if self.rect.colliderect(threat.rect):
                self.energy -= 1  # Decrease energy
                threat_location = (threat.rect.x, threat.rect.y)
                self.avoid_threats[threat_location] = self.avoid_threats.get(threat_location, 0) + 1  # Remember the threat location
                self.collision_count += 1  # Increment the collision count
                self.bounce_from_threat(threat)  # Adjust position to avoid moving inside the threat
                break  # Only interact with one threat at a time

        # Avoid threats
        self.avoid_nearby_threats()

    def avoid_nearby_threats(self):
        for threat in threat_sprites:
            distance = pygame.math.Vector2(self.rect.center).distance_to(threat.rect.center)
            if distance < AVOIDANCE_RADIUS:  # Only avoid threats within a certain distance
                threat_location = (threat.rect.x, threat.rect.y)
                avoidance_strength = self.avoid_threats.get(threat_location, 0)  # How much to avoid based on past encounters

                if avoidance_strength > 0:
                    avoidance_vector = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(threat.rect.center)
                    avoidance_vector.scale_to_length(ENTITY_SPEED + avoidance_strength * 2)  # Increase avoidance speed based on how often they encountered the threat
                    self.speed_x, self.speed_y = avoidance_vector.x, avoidance_vector.y

    def bounce_from_threat(self, threat):
        # Bounce the entity away from the threat after a collision
        if self.rect.right > threat.rect.left and self.speed_x > 0:
            self.rect.right = threat.rect.left  # Move to the left of the threat
            self.speed_x *= -1  # Reverse direction horizontally

        elif self.rect.left < threat.rect.right and self.speed_x < 0:
            self.rect.left = threat.rect.right  # Move to the right of the threat
            self.speed_x *= -1  # Reverse direction horizontally

        if self.rect.bottom > threat.rect.top and self.speed_y > 0:
            self.rect.bottom = threat.rect.top  # Move above the threat
            self.speed_y *= -1  # Reverse direction vertically

        elif self.rect.top < threat.rect.bottom and self.speed_y < 0:
            self.rect.top = threat.rect.bottom  # Move below the threat
            self.speed_y *= -1  # Reverse direction vertically

        # After bouncing off the threat, immediately check for walls
        self.bounce_off_walls()

    def bounce_off_walls(self):
        # Bounce off the walls of the screen
        if self.rect.left < BORDER_THICKNESS:
            self.rect.left = BORDER_THICKNESS
            self.speed_x *= -1  # Reverse direction horizontally
        if self.rect.right > WIDTH - BORDER_THICKNESS:
            self.rect.right = WIDTH - BORDER_THICKNESS
            self.speed_x *= -1  # Reverse direction horizontally
        if self.rect.top < BORDER_THICKNESS:
            self.rect.top = BORDER_THICKNESS
            self.speed_y *= -1  # Reverse direction vertically
        if self.rect.bottom > HEIGHT - BORDER_THICKNESS:
            self.rect.bottom = HEIGHT - BORDER_THICKNESS
            self.speed_y *= -1  # Reverse direction vertically

# Create groups for entities, food, and threats
entity_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
threat_sprites = spawn_threats()

# Add initial entities
male_entity = Entity((0, 0, 255), 100, 100, 'male')  # Blue male
female_entity = Entity((255, 192, 203), 200, 200, 'female')  # Pink female
entity_sprites.add(male_entity)
entity_sprites.add(female_entity)

# Spawn initial food
for _ in range(10):  # Adjust number as needed
    food_sprites.add(spawn_food())

# Main loop
running = True
clock = pygame.time.Clock()
start_time = time.time()
collision_data = []

while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # Update entities
    entity_sprites.update()

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_border()
    entity_sprites.draw(screen)
    food_sprites.draw(screen)
    threat_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(30)

    # Check if 30 seconds have passed
    if elapsed_time >= TIME_PERIOD:
        # Record collision data
        collision_data.append({
            "period": len(collision_data) + 1,
            "male_collisions": male_entity.collision_count,
            "female_collisions": female_entity.collision_count
        })
        male_entity.collision_count = 0  # Reset collision count for next period
        female_entity.collision_count = 0
        start_time = current_time  # Reset timer for the next period

# After the main loop ends, plot the collision graph
if collision_data:
    periods = [data["period"] for data in collision_data]
    male_collisions = [data["male_collisions"] for data in collision_data]
    female_collisions = [data["female_collisions"] for data in collision_data]

    plt.plot(periods, male_collisions, color='blue', marker='o', linestyle='-', label='Male Collisions')
    plt.plot(periods, female_collisions, color='pink', marker='o', linestyle='-', label='Female Collisions')

    # Adding data labels to key points
    for i, txt in enumerate(male_collisions):
        plt.annotate(txt, (periods[i], male_collisions[i]), textcoords="offset points", xytext=(0, 5), ha='center')
    for i, txt in enumerate(female_collisions):
        plt.annotate(txt, (periods[i], female_collisions[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    plt.xlabel('Time Periods (30s each)')
    plt.ylabel('Number of Collisions')
    plt.title('Collision Data: Male vs Female Entities Over Time')
    plt.legend()
    plt.show()

pygame.quit()