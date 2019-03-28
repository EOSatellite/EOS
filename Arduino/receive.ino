#include <IRremote.h>

int RECV_PIN = 11;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup()
{
    Serial.begin(38400);
    irrecv.enableIRIn();
}

void loop()
{
    if (irrecv.decode(&results)) {
        char buf[6];
        sprintf(buf, "%06x", results.value);

        Serial.println(buf);
    }
}
