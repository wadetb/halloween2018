#include <Arduino.h>
#include <Wire.h>

bool sequence[8][4] = 
{
  {LOW, LOW, LOW, HIGH },
  {LOW, LOW, HIGH, HIGH},
  {LOW, LOW, HIGH, LOW },
  {LOW, HIGH, HIGH, LOW},
  {LOW, HIGH, LOW, LOW },
  {HIGH, HIGH, LOW, LOW},
  {HIGH, LOW, LOW, LOW },
  {HIGH, LOW, LOW, HIGH}
};

void step_init(int pins[4])
{
  pinMode(pins[0], OUTPUT);
  pinMode(pins[1], OUTPUT);
  pinMode(pins[2], OUTPUT);
  pinMode(pins[3], OUTPUT);
}

void step(int pins[4], int state)
{
  int position = state & 7;
  digitalWrite(pins[0], sequence[position][0]);
  digitalWrite(pins[1], sequence[position][1]);
  digitalWrite(pins[2], sequence[position][2]);
  digitalWrite(pins[3], sequence[position][3]);
}

#define VOLDY_CMD_SET_LED             1
#define VOLDY_CMD_CALIBRATE_ARM       2
#define VOLDY_CMD_CALIBRATE_HEAD      3
#define VOLDY_CMD_SET_ARM             4
#define VOLDY_CMD_SET_HEAD            5
#define VOLDY_CMD_CLEAR_LED           6
#define VOLDY_CMD_CLEAR_ARM           7
#define VOLDY_CMD_CLEAR_HEAD          8

int arm_pins[4] = { 8, 9, 10, 11 };
int head_pins[4] = { 4, 5, 6, 7 };
int led_pin = 13;
int slave_address = 8;

#define MAX_KEYS 4

struct key
{
  int target;
  int duration;
  int slowness;
};

struct anim
{
  int state;
  int nkeys;
  struct key keys[MAX_KEYS];
};

struct anim led;
struct anim arm;
struct anim head;

void advance(struct anim *anim)
{
  if (anim->nkeys == 0)
    return;
  if (anim->state != anim->keys[0].target)
    return;
  if (anim->keys[0].duration > 0)
  {
    anim->keys[0].duration--;
  }
  else
  {
    anim->nkeys--;
    memmove(&anim->keys[0], &anim->keys[1], sizeof(struct key) * anim->nkeys);
  }
}

void add_key(struct anim *anim, int target, int duration, int slowness)
{
  if (anim->nkeys == MAX_KEYS)
    return;
  if (duration < 1)
    duration = 1;
  if (slowness < 0)
    slowness = 0;
  struct key *key = &anim->keys[anim->nkeys];
  key->target = target;
  key->duration = duration;
  key->slowness = slowness;
  anim->nkeys++;
}

short read_short()
{
  int dataHi = Wire.read();
  int dataLo = Wire.read();
  return (short)((dataHi << 8) | (dataLo)); 
}

void receive_data(int byte_count)
{
  int cmd = Wire.read();
  short data0 = read_short();
  short data1 = read_short();
  short data2 = read_short();

  while (Wire.available())
    Wire.read();

//  Serial.print("received i2c cmd ");
//  Serial.print(cmd);
//  Serial.print(" data ");
//  Serial.print(data0);
//  Serial.print(" ");
//  Serial.print(data1);
//  Serial.print(" ");
//  Serial.println(data2);
  
  switch (cmd) 
  {
  case VOLDY_CMD_SET_LED: add_key(&led, data0, data1, data2); break;  
  case VOLDY_CMD_CALIBRATE_ARM: arm.state += data0; arm.keys[0].slowness = 3; break;
  case VOLDY_CMD_CALIBRATE_HEAD: head.state += data0; head.keys[0].slowness = 3; break;
  case VOLDY_CMD_SET_ARM: add_key(&arm, data0, data1, data2); break;
  case VOLDY_CMD_SET_HEAD: add_key(&head, data0, data1, data2); break;
  case VOLDY_CMD_CLEAR_LED: led.nkeys = 0; break;
  case VOLDY_CMD_CLEAR_ARM: arm.nkeys = 0; break;
  case VOLDY_CMD_CLEAR_HEAD: head.nkeys = 0; break;
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("setup");
  Wire.begin(slave_address);
  Wire.onReceive(receive_data);
  step_init(arm_pins);
  step_init(head_pins);
  pinMode(led_pin, OUTPUT);
}

int frame;

void loop()
{
  frame++;
  
  advance(&led);
  advance(&arm);
  advance(&head);
  
  if (led.state != led.keys[0].target)
  {
    digitalWrite(led_pin, led.keys[0].target ? HIGH : LOW);
    led.state = led.keys[0].target;
  }

  if (arm.state != arm.keys[0].target && (frame % (1+arm.keys[0].slowness)) == 0)
  {
    int dir = arm.state < arm.keys[0].target ? 1 : -1;
    arm.state += dir;
    step(arm_pins, arm.state);
  }

  if (head.state != head.keys[0].target && (frame % (1+head.keys[0].slowness)) == 0)
  {
    int dir = head.state < head.keys[0].target ? 1 : -1;
    head.state += dir;
    step(head_pins, head.state);
  }

  delay(1);
}

