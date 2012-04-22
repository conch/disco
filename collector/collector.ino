#include <Wire.h>
#include <EEPROM.h>

#include "wiinunchuk.h"

int saddr = 0; // address of the byte that stores the signs of the next 8 bytes
int addr_offset = 0; // address of the current normal byte (not a sign byte), ranges between 0 and 7
int eeprom_size = 1024;

void setup()
{
  nunchuk_init();
  pinMode(13, OUTPUT);
  delay(400);
}

void loop()
{
  nunchuk_get_data();
  if (nunchuk_zbutton() == 1)
  {
    // check if EEPROM is full already
    // turn on light if it is
    if (saddr + addr_offset + 1 >= eeprom_size)
      full();
    else {
      record();
      if (addr_offset + 1 > 7) {
        saddr += 9;
        addr_offset = 0;
      } else
        addr_offset++;
      }
  }

  delay(100);
}

void full()
{
  digitalWrite(13, HIGH);
}

void record()
{
  digitalWrite(13, LOW);
  int roll = nunchuk_rollangle();
  // use two bytes to store each number
  // bit is 1 if number is negative. 0 if it's positive.
  if (roll < 0) {
    EEPROM.write(saddr, EEPROM.read(saddr) | (1 << addr_offset));
    roll = -roll;
  } else
    EEPROM.write(saddr, EEPROM.read(saddr) & ~(1 << addr_offset));
  EEPROM.write(saddr + addr_offset + 1, roll);
}
