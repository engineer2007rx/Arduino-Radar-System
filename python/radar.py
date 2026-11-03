

import pygame
import serial
import math
import time



PORT = "COM4"       # Change to your Arduino COM port
BAUD_RATE = 9600

MAX_DISTANCE = 100  # Radar range in cm
DETECTION_LIMIT = 30

WIDTH = 1000
HEIGHT = 700

SERVO_OFFSET = 0    # Adjust after physical calibration



# Connect to Arduino
arduino = serial.Serial(PORT, BAUD_RATE, timeout=0.05)
time.sleep(2)
arduino.reset_input_buffer()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Arduino Radar")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 65, 0)
RED = (255, 40, 40)
WHITE = (230, 230, 230)
GRAY = (100, 100, 100)

# Radar geometry
CX = WIDTH // 2
CY = 590
RADIUS = 420

font = pygame.font.SysFont("consolas", 22)
small_font = pygame.font.SysFont("consolas", 16)

# Live sensor data
angle = 90
distance = 0
detected = False

# Recent object detections
blips = []

# Smoothed readings per angle
filtered = [None] * 181

running = True


# Convert angle and distance into screen coordinates
def radar_coordinates(a, d):

    a = max(0, min(180, a + SERVO_OFFSET))

    radians = math.radians(a)

    radius = (d / MAX_DISTANCE) * RADIUS

    x = CX - radius * math.cos(radians)
    y = CY - radius * math.sin(radians)

    return int(x), int(y)


# Draw smooth semicircular rings
def draw_radar():

    for d in [20, 40, 60, 80, 100]:

        radius = (d / MAX_DISTANCE) * RADIUS

        points = []

        for a in range(181):

            x, y = radar_coordinates(a, d)
            points.append((x, y))

        pygame.draw.lines(
            screen, DARK_GREEN, False, points, 2
        )

        label = small_font.render(
            f"{d} cm", True, GREEN
        )

        screen.blit(
            label,
            (CX + 8, CY - radius - 20)
        )

    # Angle lines
    for a in range(0, 181, 30):

        x, y = radar_coordinates(a, MAX_DISTANCE)

        pygame.draw.line(
            screen,
            DARK_GREEN,
            (CX, CY),
            (x, y),
            1
        )

        label = small_font.render(
            f"{a} deg", True, GREEN
        )

        screen.blit(
            label,
            (x - 20, y - 20)
        )


# Draw fading scanning line
def draw_scan(a):

    x, y = radar_coordinates(a, MAX_DISTANCE)

    # Outer glow
    pygame.draw.line(
        screen, (0, 90, 0), (CX, CY), (x, y), 9
    )

    # Main scanning line
    pygame.draw.line(
        screen, GREEN, (CX, CY), (x, y), 2
    )


# Read Arduino serial data
def read_arduino():

    global angle, distance, detected

    try:

        # Process incoming data
        while arduino.in_waiting:

            data = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            values = data.split(",")

            if len(values) != 2:
                continue

            try:
                new_angle = int(values[0])
                new_distance = int(values[1])
            except ValueError:
                continue

            if not 0 <= new_angle <= 180:
                continue

            if not 0 <= new_distance <= 500:
                continue

            angle = new_angle
            distance = new_distance

            detected = (
                distance > 0 and
                distance <= DETECTION_LIMIT
            )

            # Ignore invalid or out-of-range readings
            if distance == 0 or distance > MAX_DISTANCE:
                continue

            # Smooth distance readings over time
            previous = filtered[angle]

            if previous is None:
                filtered[angle] = float(distance)
            else:
                filtered[angle] = (
                    0.65 * previous + 0.35 * distance
                )

            smooth_distance = filtered[angle]

            x, y = radar_coordinates(
                angle, smooth_distance
            )

            # Update nearby detection
            blips.append((
                x, y, time.time()
            ))

    except (serial.SerialException, OSError) as e:
        print("Serial error:", e)


# Main program
try:

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Receive data
        read_arduino()

        screen.fill(BLACK)

        # Draw radar
        draw_radar()

        # Draw scanning line
        draw_scan(angle)

        # Remove old detections
        now = time.time()

        blips = [
            b for b in blips
            if now - b[2] < 1.5
        ]

        # Draw detected objects with fading effect
        for x, y, timestamp in blips:

            age = now - timestamp

            brightness = max(
                30, int(255 * (1 - age / 1.5))
            )

            pygame.draw.circle(
                screen,
                (brightness, 0, 0),
                (x, y),
                6
            )

        # Information panel
        pygame.draw.rect(
            screen, (0, 25, 0),
            (15, 15, 300, 155)
        )

        pygame.draw.rect(
            screen, DARK_GREEN,
            (15, 15, 300, 155), 2
        )

        title = font.render(
            "ARDUINO RADAR", True, GREEN
        )

        angle_text = font.render(
            f"Angle: {angle} degrees", True, WHITE
        )

        distance_text = font.render(
            f"Distance: {distance} cm", True, WHITE
        )

        status = (
            "OBJECT DETECTED"
            if detected else "NO OBJECT"
        )

        status_color = RED if detected else GREEN

        status_text = font.render(
            status, True, status_color
        )

        screen.blit(title, (30, 25))
        screen.blit(angle_text, (30, 60))
        screen.blit(distance_text, (30, 95))
        screen.blit(status_text, (30, 130))

        pygame.display.flip()

        clock.tick(60)

finally:

    arduino.close()
    pygame.quit()
