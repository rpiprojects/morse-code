import RPi.GPIO as GPIO
import time
import json

with open('morse-config.json') as data_file:
    CONFIG = json.load(data_file)

PIN_NUM = CONFIG["receive-pin-number"]
CODE = CONFIG["codes"]
REVERSE_CODES = {y:x for x,y in CODE.items()}
UNIT_AMOUNT = CONFIG["unit-amount"]
UNIT_BUFFER = 0
# times for LED on:
DOT_TIME = UNIT_AMOUNT
DASH_TIME = round(UNIT_AMOUNT * 3, 1)
# times for LED off:
LETTER_WAIT_TIME = UNIT_AMOUNT
WORD_WAIT_TIME = round(UNIT_AMOUNT * 3, 1)
BETWEEN_WORD_WAIT_TIME = round(UNIT_AMOUNT * 7, 1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NUM, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_time = 0
end_time = 0

symbol = ''
symbols = []


def add_to_symbol(character):
  global symbol
  symbol += character
  # print('symbol: ' + symbol)

def save_symbol(string):
  if string == ' ':
    print(' ')
  else:
    print(REVERSE_CODES[string])
  # print('adding string to array' + string)
  # global symbols
  # symbols.append(string)
  # print(symbols)


def on():
  global start_time
  global end_time
  global symbol
  time_led_was_off = 0
  start_time = time.time()
  if end_time != 0:
     time_led_was_off = round(start_time - end_time, 1)

     if (time_led_was_off == WORD_WAIT_TIME):
      save_symbol(symbol)
      symbol = ''
     elif (time_led_was_off == BETWEEN_WORD_WAIT_TIME):
      save_symbol(symbol)
      symbol = ''
      save_symbol(' ')

def off():
  global start_time
  global end_time
  time_led_was_on = 0
  end_time = time.time()
  time_led_was_on = round(end_time - start_time, 1)
  if time_led_was_on == DOT_TIME:
    add_to_symbol('.')
  else:
    add_to_symbol('-')

def my_callback(channel):
  if GPIO.input(PIN_NUM):
    on()
  else:
    off()

GPIO.add_event_detect(PIN_NUM, GPIO.BOTH, callback=my_callback)
while True:
  x = 1

GPIO.cleanup()