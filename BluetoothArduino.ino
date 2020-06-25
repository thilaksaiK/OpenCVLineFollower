# define rightFront 5
# define rightBack  6
# define leftFront  10
# define leftBack   3

byte incomingByte = 0;
unsigned long a;
int Speed;
  
void setup() {
  Serial.begin(9600);
  while (!Serial){}

  pinMode(rightFront,OUTPUT);
  pinMode(leftFront,OUTPUT);
  pinMode(rightBack,OUTPUT);
  pinMode(leftBack,OUTPUT);
  
      analogWrite(rightFront,0);
      analogWrite(rightBack,0);
      analogWrite(leftFront,0);
      analogWrite(leftBack,0);
}


void loop() {
  if (Serial.available() > 0) {
    a = millis();
    incomingByte = Serial.read();
    if (incomingByte >=0 and incomingByte<= 128){
    if(incomingByte == 0){
      analogWrite(rightFront,0);
      analogWrite(rightBack,0);
      analogWrite(leftFront,0);
      analogWrite(leftBack,0);
    }
    else if(incomingByte == 128){
      analogWrite(rightFront,0);
      analogWrite(rightBack,200);
      analogWrite(leftFront,0);
      analogWrite(leftBack,200);
    }
    else if(incomingByte == 64){
      analogWrite(rightFront,150);
      analogWrite(rightBack,0);
      analogWrite(leftFront,150);
      analogWrite(leftBack,0);
    }
    else if(incomingByte < 64){
      Speed = (70+incomingByte);
      analogWrite(rightFront,220);
      analogWrite(rightBack,0);
      analogWrite(leftFront,Speed);
      analogWrite(leftBack,0);
    }
    else if(incomingByte > 64){
      Speed = (170-incomingByte);
      analogWrite(rightFront,Speed);
      analogWrite(rightBack,0);
      analogWrite(leftFront,220);
      analogWrite(leftBack,0);
      
    }
    }
  }
  if(millis()-a > 200){
    analogWrite(rightFront,0);
    analogWrite(rightBack,0);
    analogWrite(leftFront,0);
    analogWrite(leftBack,0);
    a = millis();
  }
}
