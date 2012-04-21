#include <Wire.h>
#include <EEPROM.h>

int addr = 0;
int eeprom_size = 1024; // number of bytes in EEPROM for Atmega328

void setup()
{
  Serial.begin(19200);
  for (int i = 0; i < eeprom_size; i+=2)
  {
    int sign = EEPROM.read(i);
    int roll = EEPROM.read(i + 1);
    if ((sign >> 7) == 1)
      roll = -roll;
    Serial.print(roll);
    Serial.print("\r\n");
  }
}

void loop() {}
