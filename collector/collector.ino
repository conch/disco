#include <Wire.h>
#include <EEPROM.h>

#include "wiinunchuk.h"

int saddr = 0; // address of the byte that stores the signs of the next 8 bytes
int addr_offset = 0; // address of the current normal byte (not a sign byte), ranges between 0 and 7
int eeprom_size = 1024;
volatile int state = LOW;
int times = 0; // used for average
int data[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

void setup()
{
//  Serial.begin(19200);
  nunchuk_init();
  pinMode(13, OUTPUT);
  clear_eeprom();
  attachInterrupt(0, change_state, FALLING);
  digitalWrite(13, HIGH);
}

void loop()
{
  if (times == 10 && state != LOW) {
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

     change_state();
     times = 0;
  } else {
    if (state != LOW) {
      nunchuk_get_data();
      data[times] = nunchuk_rollangle() + 180;
      times++;
    }
  }
}

void change_state()
{
  state = !state;
}

void full()
{
  digitalWrite(13, HIGH);
}

void record()
{
  digitalWrite(13, LOW);
  int roll = (data[4] + data[5]) / 2;
//  Serial.println(roll, DEC);
  // use two bytes to store each number
  // bit is 1 if number is negative. 0 if it's positive.
  if (roll < 0) {
    EEPROM.write(saddr, EEPROM.read(saddr) | (1 << addr_offset));
    roll = -roll;
  } else
    EEPROM.write(saddr, EEPROM.read(saddr) & ~(1 << addr_offset));
  EEPROM.write(saddr + addr_offset + 1, roll);
}

void clear_eeprom()
{
  // reset the memory to 0s at the start of each photoshoot
  for (int i = 0; i < eeprom_size; i++)
  {
    EEPROM.write(i, 0);
  }
}
