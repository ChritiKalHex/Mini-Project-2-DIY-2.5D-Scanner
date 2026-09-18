////////////////////////////////////////////////////////////////////
//                                                                //
//   Use two servos and a IR distance sensor to scan and object   //
//   send the data to a python program to be visualized.          //
//                                                                //
////////////////////////////////////////////////////////////////////

#include <Servo.h>

// Set servo constants.
uint8_t RANGE_MIN = 0;
uint8_t RANGE_MAX = 90;
uint8_t YAW_PORT = 3;
uint8_t PITCH_PORT = 5;
int8_t INCREMENT = 5;

// Set the IR constatns.
uint8_t IR_PORT = 0;
float VOLTS_TO_METERS = 1;

// Initialize the servos and their positions.
Servo yaw_servo;
int8_t yaw = RANGE_MIN;
Servo pitch_servo;
int8_t pitch = RANGE_MIN;
bool yaw_backwards = false;

void setup() {
  // Setup the serial port.
  long baudRate = 9600;       // The baudRate for sending & receiving programs must match
  Serial.begin(baudRate);     // Set the baudRate to 115200 for faster communication

  // Setup the servos.
  yaw_servo.attach(YAW_PORT);
  pitch_servo.attach(PITCH_PORT);
}

void loop() {
  // Set the servo positions.
  yaw_servo.write(yaw);
  pitch_servo.write(pitch);

  // Scan with the IR sensor.
  uint16_t scan1 = analogRead(IR_PORT);
  uint16_t scan2 = analogRead(IR_PORT);
  uint16_t scan3 = analogRead(IR_PORT);

  // Claculate the distance.
  uint16_t voltage = min(min(scan1, scan2), scan3);
  float distance = voltage * VOLTS_TO_METERS;

  // Transmit one line of text to python with the pitch, yaw, and distance values.
  // NOTE: commas are sent between values, after the last value a Newline is sent.
  Serial.print(yaw);    Serial.print(",");
  Serial.print(pitch);    Serial.print(",");
  Serial.println(distance);
  
  // delay after sending data so the serial connection is not over run.
  delay(400);

  // Update the servo positions.
  yaw = yaw + INCREMENT * (yaw_backwards*-2 + 1);

  // If yaw is more than it's maximum, increment pitch
  // and make yaw go backwards.
  if((!yaw_backwards && yaw > RANGE_MAX) || (yaw_backwards && yaw < RANGE_MIN)) {
    pitch = pitch + INCREMENT;
    yaw_backwards = !yaw_backwards;
    yaw = yaw + INCREMENT * (yaw_backwards*-2 + 1);
  }

  // If pitch is more than it's maximum, stop scanning.
  if(pitch > RANGE_MAX) {
    while(true) {
      // Do nothing.
    }
  }
}
