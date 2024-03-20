int LED_PIN = 13;
int old; 
char sensor_number = '1';
int door;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  old = 0; 
  door = 1;
}

void loop() {

  if(door==1){
    float Vout = (analogRead(A0)*5)/1023.0;

    // put your main code here, to run repeatedly:
    if(Vout > 1 && old==1){
      digitalWrite(LED_PIN, LOW);
      Serial.write(sensor_number);
      Serial.write("0");
      old = 0;
    }
    else if(Vout < 0.9 && old==0){
      digitalWrite(LED_PIN, HIGH);
      Serial.write(sensor_number);
      Serial.write("1");
      old = 1;
    }
  }
}