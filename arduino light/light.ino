int LED_PIN = 13;
int old; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  old = 0; 
}

void loop() {
  float Vout = (analogRead(A0)*5)/1023.0;

  // put your main code here, to run repeatedly:
  if(Vout > 1 && old==1){
    /*Serial.println("HIGH");*/
    digitalWrite(LED_PIN, LOW);
    Serial.write("0");
    old = 0;
  }
  if(Vout < 0.5 && old==0){
    /*Serial.println("LOW");*/
    digitalWrite(LED_PIN, HIGH);
    Serial.write("1");
    old = 1;
  }
}