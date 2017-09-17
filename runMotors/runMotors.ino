// motor one
int enA = 10;
int in1 = 9;
int in2 = 8;
// motor two
int enB = 5;
int in3 = 7;
int in4 = 6;

//Input buttons to determine direction
int lF = 11;
int lR = 12;

int rF = 4;
int rR = 3;

//Motor modes, 0 off, 1 forward, 2 reverse
int m1 = 0;
int m2 = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(lF,INPUT);
  pinMode(lR,INPUT);
  pinMode(rF,INPUT);
  pinMode(rR,INPUT);
}

void leftFor(int power){
  //Power should between 0 and 255
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, power);
}

void leftRev(int power){
  //Power should between 0 and 255
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, power);
}

void leftOff(){
  //Power should between 0 and 255
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 0);
}

void rightFor(int power){
  //Power should between 0 and 255
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, power);
}

void rightRev(int power){
  //Power should between 0 and 255
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, power);
}

void rightOff(){
  //Power should between 0 and 255
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 0);
}

void loop() {
  leftFor(127);
  rightFor(127);
//  //Reset
//  m1 = 0;
//  m2 = 0;
//
//  //Get states
//  //Left motor
//  if(digitalRead(lF)){
//    m1 = 1;
//  }
//  else if(digitalRead(lR)){
//    m1 = 2;
//  }
//
//  //Right motor
//  if(digitalRead(lF)){
//    m2 = 1;
//  }
//  else if(digitalRead(lR)){
//    m2 = 2;
//  }
//  
//  //Left control
//  if(m1 == 0){
//    leftOff();
//  }
//  else if(m1 == 1){
//    leftFor();
//  }
//  else if(m1 == 2){
//    leftRev();
//  }
//
//  //Right control
//   if(m2 == 0){
//    rightOff();
//  }
//  else if(m2 == 1){
//    rightFor();
//  }
//  else if(m2 == 2){
//    rightRev();
//  }

  //TODO CHANGE TO FEEL NATURAL
  delay(250);
}
