
#include <WiFi.h>
#include <WiFiMulti.h>
#include "FirebaseESP32.h"

FirebaseData firebaseData;

WiFiMulti WiFiMulti;
int ledPin = 2;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int count = 10;
const char* ssid     = "MY Wi-Fi SSID";
const char* password = "MY Wi-Fi Password";
#define FIREBASE_HOST "https://netflixremote-20291.firebaseio.com/"
#define FIREBASE_AUTH "MY FIREBASE AUTH KEY"
static bool hasWifi = false;


void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Connecting to Wifi");
  Serial.println("Connecting...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  hasWifi = true;
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  for (int i = 0; i < 2; i++) {
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
  }
}

void loop() {
  if (analogRead(36) > 0) {

    for (int i = 0; i < 100; i++) {
      sensorValue += analogRead(36);
    }
    sensorValue /= 100;
  }
  //Serial.println(sensorValue);

  if (sensorValue >= 4095) {
    Serial.println("5: Comedy");
    digitalWrite(ledPin, HIGH);
    Firebase.setInt(firebaseData, "/GenreVal", 5);
  } else if (sensorValue > 4000) {
    Serial.println("6: Crime");
    digitalWrite(ledPin, HIGH);
    Firebase.setInt(firebaseData, "/GenreVal", 6);
  } else if (sensorValue > 3700) {
    Serial.println("16: Horror");
    digitalWrite(ledPin, HIGH);
    Firebase.setInt(firebaseData, "/GenreVal", 16);
  } else if (sensorValue > 0) {
    Serial.println("23: Sci-Fi");
    digitalWrite(ledPin, HIGH);
    Firebase.setInt(firebaseData, "/GenreVal", 23);
  } else {
    digitalWrite(ledPin, LOW);
  }

  sensorValue = 0;
  delay(10);
}
