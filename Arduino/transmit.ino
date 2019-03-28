// NOTE: Laser must be connected to Pin 3

#include <IRremote.h>

// For sending hex codes via the laser
IRsend irsend;

void setup() {
    // Set the baud rate
    Serial.begin(38400);
}

void loop() {
    // Check if we have enough data in the buffer to send a hex code
    if (Serial.available() >= 6) {
        char buf[7];
        for (int i = 0; i < 6; i++) {
            buf[i] = Serial.read();
        }
        buf[6] = '\0';  // Add the end-of-string character

        auto hex = strtoul(buf, NULL, 16);  // Convert the string to base 16 (hex)

        Serial.println(buf);    // Print out our string

        irsend.sendNEC(hex, 32);    // Send the code via laser
        delay(40);
    }
}
