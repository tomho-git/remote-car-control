int motor1pin1 = 8;
int motor1pin2 = 9;
int motor2pin1 = 4;
int motor2pin2 = 5;
int motor3pin1 = 6;
int motor3pin2 = 7;
byte command;
#define MOTOR_ONE_FORWARD {digitalWrite (motor1pin1, HIGH); digitalWrite (motor1pin2, LOW);}
#define MOTOR_ONE_BACKWARD {digitalWrite (motor1pin1, LOW); digitalWrite (motor1pin2, HIGH);}
#define MOTOR_TWO_FORWARD {digitalWrite (motor2pin1, HIGH); digitalWrite (motor2pin2, LOW);}
#define MOTOR_TWO_BACKWARD {digitalWrite (motor2pin1, LOW); digitalWrite (motor2pin2, HIGH);}
#define MOTOR_THREE_FORWARD {digitalWrite (motor3pin1, HIGH); digitalWrite (motor3pin2, LOW);}
#define MOTOR_THREE_BACKWARD {digitalWrite (motor3pin1, LOW); digitalWrite (motor3pin2, HIGH);}
#define STOP {digitalWrite (motor1pin1, LOW);digitalWrite (motor1pin2, LOW);digitalWrite (motor2pin1, LOW);digitalWrite (motor2pin2, LOW);digitalWrite (motor3pin1, LOW);digitalWrite (motor3pin2, LOW);}
#define MOVE_FORWARD {MOTOR_ONE_FORWARD MOTOR_THREE_BACKWARD}
#define MOVE_BACKWARD {MOTOR_ONE_BACKWARD MOTOR_THREE_FORWARD}
#define ROTATE_ANTICLOCKWISE {MOTOR_ONE_FORWARD MOTOR_TWO_BACKWARD MOTOR_THREE_FORWARD}
#define ROTATE_CLOCKWISE {MOTOR_ONE_BACKWARD MOTOR_TWO_FORWARD MOTOR_THREE_BACKWARD}
#define DELAY_STOP {delay(1000); STOP}
#define QUICK_STOP {delay(100);STOP}


void setup() {
  Serial.begin(9600);

  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  pinMode(motor3pin1, OUTPUT);
  pinMode(motor3pin2, OUTPUT);
}

void loop() {
  if(Serial.available()){
    command = Serial.read(); 
    Serial.print(command);
    if(command == 'W'){
      MOVE_FORWARD
      DELAY_STOP
    }
    else if (command == 'S'){
      MOVE_BACKWARD
      DELAY_STOP
    }
    
    else if (command == 'Q'){
      ROTATE_ANTICLOCKWISE
      QUICK_STOP
    }
    else if(command == 'E'){
      ROTATE_CLOCKWISE
      QUICK_STOP
    }
    else if(command == 'X'){
      STOP
    }
    
  }
}
