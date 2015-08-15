import RPi.GPIO as GPIO
import time
import json

with open('morse-config.json') as data_file:
    CONFIG = json.load(data_file)

PIN_NUM = CONFIG["pin-number"]
CODE = CONFIG["codes"]
UNIT_AMOUNT = CONFIG["unit-amount"]
DOT_TIME = UNIT_AMOUNT
DASH_TIME = UNIT_AMOUNT * 3
LETTER_WAIT_TIME = UNIT_AMOUNT
WORD_WAIT_TIME = UNIT_AMOUNT * 3
BETWEEN_WORD_WAIT_TIME = UNIT_AMOUNT * 7


GPIO.setmode(GPIO.BCM)  # numbering scheme that corresponds to breakout board and pin layout
GPIO.setup(PIN_NUM, GPIO.OUT)


def reset_led(wait_time):
    GPIO.output(PIN_NUM, GPIO.LOW)
    time.sleep(wait_time)


def dot():
    GPIO.output(PIN_NUM, GPIO.HIGH)
    time.sleep(DOT_TIME)


def dash():
    GPIO.output(PIN_NUM, GPIO.HIGH)
    time.sleep(DASH_TIME)


def parse_char(code):
    for index, char in enumerate(code):
        if char == '.':
            dot()
        else:
            dash()
        if index < (len(code) - 1):
            reset_led(LETTER_WAIT_TIME)


def parse_word(word):
    for index, char in enumerate(word.upper()):
        c = CODE.get(char, 'x')
        if c != 'x':
            parse_char(c)
            if index < (len(word) - 1):
                reset_led(WORD_WAIT_TIME)


def parse_line(line):
    word_array = line.split(' ')
    for word in word_array:
        parse_word(word)
        reset_led(BETWEEN_WORD_WAIT_TIME)

while True:
    line = raw_input('message: ')
    if line == 'q()':
        break
    parse_line(line)

GPIO.cleanup()
