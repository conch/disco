#include <Wire.h>
#include <EEPROM.h>

int saddr = 0;
int addr_offset = 0;
int eeprom_size = 1024; // number of bytes in EEPROM for Atmega328
int correct_handshake[] = {104, 101, 108, 108, 111, 10};

void setup()
{
  Serial.begin(19200);
}

void loop()
{
  if (Serial.available() > 0 && handshake_is_correct())
  {
    for (int i = 0; i < eeprom_size; i += 9)
    {
      int sign = EEPROM.read(i);
      for (int j = 0; j < 8; j++)
      {
        int roll = EEPROM.read(i + j + 1);
        if ((sign >> j) & 1 == 1)
          roll = -roll;
        Serial.println(roll, DEC);
      }
    }
  }
}

boolean handshake_is_correct()
{
  // verify that the handshake is "hello"
  // only send data if the handshake is correct
  if (Serial.available() == 6)
  {
    for (int i = 0; i < 6; i++)
    {
      if (Serial.read() != correct_handshake[i])
        return false;
    }
    return true;
  }
  return false;
}
