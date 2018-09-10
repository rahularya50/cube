# cube

The following video shows the robot in action!
https://www.youtube.com/watch?v=Eo-U3c4iMMw

Six stepper motors are held in an acrylic frame and connected to a Rubik’s cube using 3D-printed adaptors. They’re controlled by an Arduino Mega using A4988 stepper motor drivers and powered by a 35V DC power supply. Four webcams are mounted around the frame so each face of the cube is visible.

The Kociemba algorithm is used to solve the cube, implemented by the
software “Cube Explorer”. The solution is written to a serial port and sent to the
Arduino. The Arduino identifies opportunities to optimize moves, by
turning opposing faces in parallel rather than in sequence, and signals the motor drivers accordingly.

All together, the cube is scanned, processed, and solved in under 1.5 seconds. That’s more than twice as fast as the human world record.
