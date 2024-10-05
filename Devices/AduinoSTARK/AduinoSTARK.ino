#include <Wire.h>
#include <MPU6050.h>
#include <Servo.h>

// Declare global variables
MPU6050 mpu;
Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1); // Halt the program
  }

  servo1.attach(9);  // Servo connected to pin D9
  servo2.attach(10); // Servo connected to pin D10

  Serial.println("IronEdge Exoskeleton Initialized");
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Map accelerometer values to servo angles
  int angle1 = map(ax, -17000, 17000, 0, 180);
  int angle2 = map(ay, -17000, 17000, 0, 180);

  // Constrain angles to valid range
  angle1 = constrain(angle1, 0, 180);
  angle2 = constrain(angle2, 0, 180);

  // Move servos
  servo1.write(angle1);
  servo2.write(angle2);

  // Debug output
  Serial.print("ax: "); Serial.print(ax);
  Serial.print(" | ay: "); Serial.print(ay);
  Serial.print(" | angle1: "); Serial.print(angle1);
  Serial.print(" | angle2: "); Serial.println(angle2);

  delay(100); // Adjust as needed
}
