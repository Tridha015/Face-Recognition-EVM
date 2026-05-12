#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int btnA = A0; 
const int btnB = A1;
const int btnC = A2;
const int btnD = A3;
const int resultBtn = 10; 
const int buzzerPin = 11;
const int lockLed = 12;

long voteA = 0, voteB = 0, voteC = 0, voteD = 0;

enum State { LOCKED, READY_TO_VOTE };
State currentState = LOCKED;

void setup() {
  Serial.begin(9600);
  
  pinMode(btnA, INPUT_PULLUP);
  pinMode(btnB, INPUT_PULLUP);
  pinMode(btnC, INPUT_PULLUP);
  pinMode(btnD, INPUT_PULLUP);
  pinMode(resultBtn, INPUT_PULLUP);
  
  pinMode(lockLed, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  lcd.init();
  lcd.backlight();
  
  showScanFaceMessage(); 
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == 'U') { 
      verifySequence(); 
    } 
    else if (data == 'D') { 
      accessDeniedSequence(); 
    }
  }

  if (currentState == READY_TO_VOTE) {
    if (digitalRead(btnA) == LOW) recordVote("Doraemon", &voteA);
    else if (digitalRead(btnB) == LOW) recordVote("Shinchan", &voteB);
    else if (digitalRead(btnC) == LOW) recordVote("Tom&Jerry", &voteC);
    else if (digitalRead(btnD) == LOW) recordVote("Pikachu", &voteD);
  }

 
  if (digitalRead(resultBtn) == LOW) {
    displayLiveResults();
    delay(5000); 
    
    if(currentState == LOCKED) showScanFaceMessage();
    else showCandidateList();
  }
}

void showScanFaceMessage() {
  currentState = LOCKED;
  digitalWrite(lockLed, HIGH); 
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(" WELCOME TO EVM ");
  lcd.setCursor(0, 1);
  lcd.print(" SCAN YOUR FACE ");
}

void verifySequence() {
  tone(buzzerPin, 2000, 150);
  lcd.clear();
  lcd.print("FACE VERIFIED!");
  delay(3000);
  
  lcd.clear();
  lcd.print("CHOOSE YOUR");
  lcd.setCursor(0, 1);
  lcd.print("CANDIDATE...");
  delay(5000);
  
  showCandidateList();
  digitalWrite(lockLed, LOW); 
  currentState = READY_TO_VOTE;
}

void showCandidateList() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("A:Dor   B:Shin");
  lcd.setCursor(0, 1);
  lcd.print("C:Tom   D:Pik");
}

void recordVote(String name, long *count) {
  (*count)++;
  tone(buzzerPin, 2500, 300);
  
  
  Serial.print('V');
  
  lcd.clear();
  lcd.print("VOTE CONFIRMED!");
  lcd.setCursor(0, 1);
  lcd.print("VOTED: " + name);
  delay(4000);
  
  showScanFaceMessage(); 
}

void accessDeniedSequence() {
  tone(buzzerPin, 500, 500); 
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(" ACCESS DENIED! ");
  lcd.setCursor(0, 1);
  lcd.print(" ALREADY VOTED  ");
  
  delay(3000); 
  showScanFaceMessage(); 
}

void displayLiveResults() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("D:"); lcd.print(voteA);
  lcd.print(" S:"); lcd.print(voteB);
  lcd.setCursor(0, 1);
  lcd.print("T:"); lcd.print(voteC);
  lcd.print(" P:"); lcd.print(voteD);
}

