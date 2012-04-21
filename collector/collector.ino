#include <Wire.h>
#include <EEPROM.h>

#include "wiinunchuk.h"

int addr = 0;

void setup()
{
  nunchuk_init();
  pinMode(13, OUTPUT);
}

void loop()
{
  nunchuk_get_data();
  if (nunchuk_zbutton() == 1)
  {
    // check if EEPROM is full already
    // turn on light if it is
    if (addr >= 1024)
      full();
    else
      record();
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
  // use two bytes to store negative numbers
  if (roll < 0) {
    EEPROM.write(addr++, 128);
    roll = -roll;
  } else
    EEPROM.write(addr++, 0);
  EEPROM.write(addr++, roll);
}
