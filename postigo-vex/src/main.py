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

# ---------------------------------- Main Program ----------------------------------- #
def main():
    """
    The main() function is the program that is executed by the brain
    """

    bump()                  # Call the bump() function to begin the program
    inertialCalibration()   # Calibrate the inertial sensor
    testInertial()          # Test the inertial sensor

#-------------------------------------------------------------------------------------#


main()