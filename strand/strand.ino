#include <Wire.h>
#include <Adafruit_NeoPixel.h>

int slave_address = 7;

Adafruit_NeoPixel strips[] = {
  Adafruit_NeoPixel(150, 30, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(120, 27, NEO_GRB + NEO_KHZ800),
};
int strips_len = sizeof(strips) / sizeof(strips[0]);

short read_short()
{
  int dataHi = Wire.read();
  int dataLo = Wire.read();
  return (short)((dataHi << 8) | (dataLo)); 
}

struct fx_fields
{
  short position;
  short length;
  short spread;
  short r;
  short g;
  short b;
};

struct fx
{
  int strip;
  int delay;
  int lifetime;
  struct fx_fields s;
  struct fx_fields v;
};

#define MAX_FX 8
struct fx allfx[MAX_FX];

#define I(x) ((x)>>4)

void advance_fx(int f, int ms)
{
  struct fx *fx = &allfx[f];

  if (fx->delay > 0)
  {
    fx->delay -= ms;
    Serial.print("delay ");
    Serial.println(fx->delay);
    return;
  }

  if (fx->lifetime > 0)
  {
    fx->lifetime--;
    if (fx->lifetime == 0)
    {
      Serial.print("fx end ");
      Serial.println(f);
    }
  }
  if (fx->lifetime == 0)
    return;

  fx->s.position += fx->v.position;
  fx->s.length += fx->v.length;
  fx->s.spread += fx->v.spread;
  fx->s.r += fx->v.r;
  fx->s.g += fx->v.g;
  fx->s.b += fx->v.b;

  int s = fx->strip;
  int n = strips[s].numPixels();
  if (I(fx->s.position) > n)
  {
    Serial.print("fx end ");
    Serial.println(f);
    fx->lifetime = 0;
  }
}

void draw_fx(int f)
{
  struct fx *fx = &allfx[f];
  int s = fx->strip;
  int n = strips[s].numPixels();
  
  for (int i = 0; i < I(fx->s.length); i++)
  {
    int l = I(fx->s.position + fx->s.spread * i);
    if (l > 0 && l < n)
    {
      int r = I(fx->s.r);
      int g = I(fx->s.g);
      int b = I(fx->s.b);
      strips[s].setPixelColor(l, strips[s].Color(r, g, b));
    }
  }
}

void erase_fx(int f)
{
  struct fx *fx = &allfx[f];
  int s = fx->strip;
  int n = strips[s].numPixels();
  for (int i = 0; i < I(fx->s.length); i++)
  {
    int l = I(fx->s.position + fx->s.spread * i);
    if (l > 0 && l < n)
    {
      strips[s].setPixelColor(l, strips[s].Color(0, 0, 0));
    }
  }
}

void receive_fields(struct fx_fields *f)
{
  f->position = read_short();
  f->length = read_short();
  f->spread = read_short();
  f->r = read_short();
  f->g = read_short();
  f->b = read_short();
}

void receive_data(int byte_count)
{
  int cmd = Wire.read();
  struct fx new_fx;
  new_fx.strip = read_short();
  new_fx.delay = read_short();
  new_fx.lifetime = read_short();
  receive_fields(&new_fx.s);
  receive_fields(&new_fx.v);
  for (int i = 0; i < MAX_FX; i++)
  {
    if (allfx[i].lifetime == 0)
    {
      Serial.print("add fx ");
      Serial.println(i);
      allfx[i] = new_fx;
      break;
    }
  }
}

void setup() 
{
  Serial.begin(115200);
  Serial.println("setup");
  Wire.begin(slave_address);
  Wire.onReceive(receive_data);

  for (int s = 0; s < strips_len; s++)
  {
    strips[s].begin();
    strips[s].show();
  }
}

int lastms;

void loop() 
{
  int nowms = millis();
  int ms = nowms - lastms;
  lastms = nowms;
  
  for (int f = 0; f < MAX_FX; f++)
  {
    if (allfx[f].delay <= 0 && allfx[f].lifetime > 0)
      erase_fx(f);
    advance_fx(f, ms);
    if (allfx[f].delay <= 0 && allfx[f].lifetime > 0)
      draw_fx(f);
  }
  
  for (int s = 0; s < strips_len; s++)
    strips[s].show();

  delay(1);
}

