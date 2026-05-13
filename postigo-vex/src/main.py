# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Tudor Barcan, Sebastian Postigo                              #
# 	Created:      5/4/2026, 2:15:00 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# ---------------------------------- Robot Configuration ----------------------------------- #
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False) # Right drivetrain motor
leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True) # Left drivetrain motor
liftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False) # Lift motor
inertial_1 = Inertial(Ports.PORT5) # Inertial sensor
liftArmLocation = Rotation(Ports.PORT6) # Lift arm location sensor
bumperSwitch = Bumper(brain.three_wire_port.a) # Bumper switch

# ---------------------------------- Helper Functions ----------------------------------- #
def bump():
    """
    Hold the program's execution until the bumper switch is pressed
    """
    while not bumperSwitch.pressing():
        wait(10, MSEC)

        brain.screen.set_cursor(1,1)
        brain.screen.print("Press the button to start the program")
        pass

    brain.screen.clear_line(1)
    brain.screen.set_cursor(1,1)
    brain.screen.print("Program executed")
    wait(1, SECONDS)

def inertialCalibration():
    """
    1. Calibrate the inertial sensor
    2. Include a 2 second wait time for calibration
    3. Call this function at the start of the program's execution
    """

    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Calibrating the initerial sensor")
    brain.screen.set_cursor(2,1)
    brain.screen.print("Don't move the robot")
    inertial_1.calibrate()          # Calibrate the intertial sesor

    wait(2, SECONDS)                # Time required to calibrate the inertial sensor

    brain.screen.set_cursor(1,1)
    brain.screen.clear_line()
    brain.screen.print("Intertial calibration complete")

def testInertial():
    """
    Test the inertial sensor displaying the heading and rotation data
    """

    brain.screen.clear_screen()
    while not bumperSwitch.pressing():
        wait(10, MSEC)
        brain.screen.set_cursor(1,1)
        brain.screen.print("Heading: " + str(inertial_1.heading()) + " degrees")
        brain.screen.set_cursor(5,1)
        brain.screen.print("Rotation: " + str(inertial_1.rotation()) + " degrees")
        brain.screen.set_cursor(6,1)
        brain.screen.print("Press the button to end the test")

def driveStraightData(e):
    """
    Report position, rotation, and error data to the brain's screen
    Parameter: e = calculated error value
    """

    brain.screen.set_cursor(1,1)
    brain.screen.print("Position: " + str(leftMotor.position())) # Print the left motor's position value
    brain.screen.set_cursor(2,1)
    brain.screen.print("Rotation: " + str(inertial_1.rotation())) # Print the inertial sensor's rotation value
    brain.screen.set_cursor(3,1)
    brain.screen.print("Error: " + str(e)) # Print the error value

def stopMotors():
    """
    Stop both drivetrain motors at the same time
    """

    rightMotor.stop()
    leftMotor.stop()
    wait(0.5, SECONDS) # Wait for 0.5 seconds for the system to stabilize

def driveStraight(distance, setPoint, motorVelocity):
    """
    Drive the robot straight for a specified distance
    Parameters:
        distance: The distance to travel (in inches)
        setPoint: equal to zero degrees for driving straight
        motorVelocity: The nominal velocity of the motors (+) => forward, (-) => backward
    """

    inertial_1.reset_rotation() # Reset the inertial sensor's rotation to zero

    kP = 0.5 # Proportional gain for driving straight
             # Used to calculate the correction to mainain course
             # If to small, correction will occur to slowly
             # If too large, overcorrection will occur
             # Determine best value iteratively through testing
            
    wheelDiameter = 4 # 4 inch wheel diameter
    wheelCircumference = wheelDiameter * math.pi # Calculate wheel circumference

    #Convert the distance in inches to distance in ticks
    # distance (ticks) = (distance (inches) / wheel circumference) * ticks per revolution
    distanceTicks = (distance / wheelCircumference) * 360

    # Reset the motor encoders
    leftMotor.set_position(0, DEGREES)
    rightMotor.set_position(0, DEGREES)

    # Drive forward if motor velocity is positive, backward if negative
    if(motorVelocity > 0):
        while leftMotor.position(DEGREES) < distanceTicks:
            e = setPoint - inertial_1.rotation() # Calculate error
            correction = kP * e # Calculate motor velocity correction

            # Correct motor velocities
            # If e > 0, (setpoint > rotation) => robot is veering to the left
            # If e < 0, (setpoint < rotation) => robot is veering to the right
            leftMotor.set_velocity(motorVelocity + correction, PERCENT)
            rightMotor.set_velocity(motorVelocity - correction, PERCENT)

            # Spin the motors
            leftMotor.spin(FORWARD)
            rightMotor.spin(FORWARD)

            driveStraightData(e) # Report data to the brain's screen
        stopMotors() # Stop the motors once the target distance is reached
    else:
        distance *= -1
        while leftMotor.position(DEGREES) > distanceTicks:
            e = setPoint - inertial_1.rotation() # Calculate error
            correction = kP * e # Calculate motor velocity correction

            # Correct motor velocities
            # If e > 0, (setpoint > rotation) => robot is veering to the left
            # If e < 0, (setpoint < rotation) => robot is veering to the right
            leftMotor.set_velocity(motorVelocity + correction, PERCENT)
            rightMotor.set_velocity(motorVelocity - correction, PERCENT)

            # Spin the motors
            leftMotor.spin(FORWARD)
            rightMotor.spin(FORWARD)

            driveStraightData(e) # Report data to the brain's screen
        stopMotors() # Stop the motors once the target distance is reached
    
            


# ---------------------------------- Main Program ----------------------------------- #
def main():
    """
    The main() function is the program that is executed by the brain
    """

    bump()                  # Call the bump() function to begin the program
    inertialCalibration()   # Calibrate the inertial sensor
    testInertial()          # Test the inertial sensor

    driveStraight(90, 0, 50)# Drive straight with the necessary parameters

#-------------------------------------------------------------------------------------#


main()