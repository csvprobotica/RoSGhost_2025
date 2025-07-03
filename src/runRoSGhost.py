# Import LEGO Mindstorms library
from mindstorms import MSHub, Motor, DistanceSensor, ColorSensor
from mindstorms.control import wait_for_seconds

# Initialize hub, motors, and sensors
hub = MSHub()
front_motor = Motor('A')  # Front motor on port A for turning
rear_motor = Motor('B')  # Rear motor on port B for driving
right_ultrasonic_sensor = DistanceSensor('D')  # Right distance sensor on port C
left_ultrasonic_sensor = DistanceSensor('E')  # Left distance sensor on port D
front_ultrasonic_sensor = DistanceSensor('F')  # Front distance sensor on port E
color_sensor = ColorSensor('C')  # Color sensor on port F

# Set speed and turn duration
SPEED = 50
TURN_DURATION = 1.2  # Duration in seconds for a 90-degree turn

# Function to turn 90 degrees to the left
def turn_left():
    front_motor.run_for_seconds(TURN_DURATION, -SPEED)

# Function to turn 90 degrees to the right
def turn_right():
    front_motor.run_for_seconds(TURN_DURATION, SPEED)

# Function to avoid lateral and frontal obstacles
def avoid_obstacles():
    rear_motor.start(SPEED)  # Start moving forward

    while True:
        # Measure distance to lateral walls
        right_distance = right_ultrasonic_sensor.get_distance_cm()
        left_distance = left_ultrasonic_sensor.get_distance_cm()
        front_distance = front_ultrasonic_sensor.get_distance_cm()
        seen_color = color_sensor.get_color()

        # If a wall is detected within 10 cm on the right
        if right_distance is not None and right_distance < 10:
            # Stop the movement
            rear_motor.stop()
            
            # Turn left
            turn_left()
            wait_for_seconds(0.5)
            
            # Resume moving forward
            rear_motor.start(SPEED)
        
        # If a wall is detected within 10 cm on the left
        elif left_distance is not None and left_distance < 10:
            # Stop the movement
            rear_motor.stop()
            
            # Turn right
            turn_right()
            wait_for_seconds(0.5)
            
            # Resume moving forward
            rear_motor.start(SPEED)
        
        # If an object is detected within 10 cm in front
        elif front_distance is not None and front_distance < 10:
            # Stop the movement
            rear_motor.stop()
            
            # If the object is red, avoid inside (left then right)
            if seen_color == 'red':
                turn_left()
                wait_for_seconds(0.5)
                rear_motor.start(SPEED)
                wait_for_seconds(1)  # Move forward a bit to avoid
                rear_motor.stop()
                turn_right()
                wait_for_seconds(0.5)
            
            # If the object is green, avoid outside (right then left)
            elif seen_color == 'green':
                turn_right()
                wait_for_seconds(0.5)
                rear_motor.start(SPEED)
                wait_for_seconds(1)  # Move forward a bit to avoid
                rear_motor.stop()
                turn_left()
                wait_for_seconds(0.5)
            
            # Resume moving forward
            rear_motor.start(SPEED)

# Main function to perform three rotations and stop at the initial position
def perform_three_rotations():
    # Reset the gyroscope
    hub.motion_sensor.reset_yaw_angle()

    # Complete three full rotations (1080 degrees)
    rotations = 0
    while rotations < 3:
        avoid_obstacles()
        yaw_angle = hub.motion_sensor.get_yaw_angle()

        # If a full rotation is completed (approximately 360 degrees)
        if yaw_angle >= 360:
            rotations += 1
            hub.motion_sensor.reset_yaw_angle()

    # Stop the robot
    rear_motor.stop()

# Run the main function
perform_three_rotations()
