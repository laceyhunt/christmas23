#include <Adafruit_NeoPixel.h>

#define LED_PIN 6  // Pin connected to the data input of the LED strip
#define NUM_LEDS 60  // Number of LEDs in your strip

#define TRIGGER_PIN 7  // Pin connected to the trigger pin of the proximity sensor
#define ECHO_PIN 8     // Pin connected to the echo pin of the proximity sensor

// Define the distance at which the lights should activate
#define PROXIMITY_THRESHOLD 20  // Adjust this value as needed (in centimeters)

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();  // Initialize all pixels to 'off'
  
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.begin(9600);
}

void loop() {
  long duration;
  int distance;

  // Trigger the proximity sensor
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  // Read the echo pulse duration
  duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate the distance in centimeters
  distance = duration * 0.034 / 2;

  // Check if the proximity sensor detects an object within the threshold
  if (distance < PROXIMITY_THRESHOLD) {
    // If an object is detected, run the light show
    runChristmasLights();
  }
}

void runChristmasLights() {
  // Your animation code here
  // For example, you can use the Adafruit NeoPixel library functions to create various lighting effects
  // For simplicity, let's just set all LEDs to red for demonstration purposes
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));  // Red color
  }
  strip.show();  // Display the updated LED colors
  delay(1000);   // Delay to keep the lights on for a moment
  strip.clear();  // Turn off all LEDs
  strip.show();   // Display the changes
}
