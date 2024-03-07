int LED_PIN = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  float Vout = (analogRead(A0)*5)/1023.0;
  // put your main code here, to run repeatedly:
  if(Vout > 0){
    Serial.println("HIGH");
    digitalWrite(LED_PIN, LOW);
  }
  if(Vout == 0){
    Serial.println("LOW");
    digitalWrite(LED_PIN, HIGH);
  }
}