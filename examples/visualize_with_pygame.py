""" A script that rotates a square in 3D space using
    quaternions and displays it in a Pygame window."""

import numpy as np
import pygame

import robolie as rl

# Set up pygame window
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Quaternion Rotation")


# Define the cube
cube = np.array(
    [
        [-1, -1, -1],
        [-1, -1, 1],
        [-1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1],
        [1, -1, 1],
        [1, 1, -1],
        [1, 1, 1],
    ]
)


# Rotate cube with quaternions
def rotate_qube(theta, axis, cube):
    return np.array([rl.rotate_by_quaternion(v, theta, axis) for v in cube])


# project cube to 2D
def project_cube(cube):
    return np.array([v[:2] for v in cube])


# Project and display cube
def display_cube(cube):
    for edge in [
        (0, 1),
        (1, 3),
        (3, 2),
        (2, 0),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 5),
        (5, 7),
        (7, 6),
        (6, 4),
    ]:
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (
                width / 2 + 100 * project_cube(cube)[edge[0]][0],
                height / 2 + 100 * project_cube(cube)[edge[0]][1],
            ),
            (
                width / 2 + 100 * project_cube(cube)[edge[1]][0],
                height / 2 + 100 * project_cube(cube)[edge[1]][1],
            ),
        )


# Define rotation axis
axis = np.array([1, 1, 0])
axis = axis / np.linalg.norm(axis)

# Functionality for drawing the rotation axis
def draw_axis_arrow():
    arrow_length = 200
    arrow_color = (120, 144, 250)
    start_point = (width / 2 - arrow_length * axis[0], height / 2 - arrow_length * axis[1])
    end_point = (width / 2 + arrow_length * axis[0], height / 2 + arrow_length * axis[1])
    pygame.draw.line(
        screen,
        arrow_color,
        start_point,
        end_point,
        5,
    )
    angle = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
    head_length = 20
    arrowhead1 = (end_point[0] - head_length * np.cos(angle - np.pi/6),
              end_point[1] - head_length * np.sin(angle - np.pi/6))
    arrowhead2 = (end_point[0] - head_length * np.cos(angle + np.pi/6),
              end_point[1] - head_length * np.sin(angle + np.pi/6))
    pygame.draw.polygon(screen, arrow_color, [end_point, arrowhead1, arrowhead2])


# Angular velocity
seconds_to_rotate = 5
theta_per_second = 2 * np.pi / (60 * seconds_to_rotate)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Initialize text input variables
input_text = ""
input_rect = pygame.Rect(10, 40, 200, 50)
input_active = False

# Text next to the input box
instruction_text = font.render(
    "Enter 3D coordinates (e.g., 1.0, 2.0, 3.0):", True, black
)
instruction_rect = instruction_text.get_rect(topleft=(10, 10))

# Cursor variables
cursor_width = 2
cursor_color = black
cursor_blink_interval = 500  # in milliseconds
cursor_last_toggle = pygame.time.get_ticks()
cursor_visible = True

# Function for drawing the input box
def draw_input_box():
    pygame.draw.rect(screen, black, input_rect, 2)
    text_surface = font.render(input_text, True, black)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Draw the instruction text
    screen.blit(instruction_text, instruction_rect.topleft)

    # Draw the cursor if the input box is active and the cursor is visible
    if input_active and cursor_visible:
        cursor_x = (
            input_rect.x + 5 + text_surface.get_width()
        )  # Cursor position at the end of the text
        pygame.draw.line(
            screen,
            cursor_color,
            (cursor_x, input_rect.y + 5),
            (cursor_x, input_rect.y + input_rect.height - 5),
            cursor_width,
        )

    # Draw the coordinates text box
    pygame.draw.rect(screen, black, coordinates_box, 2)
    coordinates_surface = font.render(coordinates_text, True, black)
    screen.blit(coordinates_surface, (coordinates_box.x + 5, coordinates_box.y + 5))


# Initialize coordinates text box variables
coordinates_box = pygame.Rect(450, 560, 330, 32)
coordinates_text = f'Current axis: {np.round(axis, decimals = 1)}'

# Main loop
running = True

# Add possiblity to redefine rotation axis within window

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicks on the input box
            if input_rect.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            # Capture key events when the input box is active
            if input_active:
                # Add blinking line to input box

                if event.key == pygame.K_RETURN:
                    try:
                        # Attempt to convert the entered text to a numpy array of floats
                        coordinates = np.array(
                            [float(x) for x in input_text.split(",")]
                        )
                        if len(coordinates) != 3:
                            print("Invalid input. Please enter valid 3D coordinates.")
                        else:
                            axis = coordinates
                            # Normalize the axis
                            axis = axis / np.linalg.norm(axis)
                        coordinates_text = f'Current axis: {np.round(axis, decimals = 1)}'
                    except ValueError:
                        coordinates_text = 'Invalid input. Please enter valid 3D coordinates.'
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        elif event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Draw the input box
    draw_input_box()

    # Display rotation axis as arrow from center of cube
    draw_axis_arrow()

    # Rotate cube
    cube = rotate_qube(theta_per_second, axis, cube)
    display_cube(cube)

    # Update the display
    pygame.display.flip()

    # Control refresh rate
    pygame.time.Clock().tick(60)

    # Toggle cursor visibility at regular intervals
    current_time = pygame.time.get_ticks()
    if current_time - cursor_last_toggle > cursor_blink_interval:
        cursor_visible = not cursor_visible
        cursor_last_toggle = current_time


pygame.quit()
