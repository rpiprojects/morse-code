import RPi.GPIO as GPIO
import time
import json

pinNum = 2
UNIT_AMOUNT = .1
DOT_TIME = UNIT_AMOUNT
DASH_TIME = UNIT_AMOUNT * 3
LETTER_WAIT_TIME = UNIT_AMOUNT
WORD_WAIT_TIME = UNIT_AMOUNT * 3
BETWEEN_WORD_WAIT_TIME = UNIT_AMOUNT * 7

CODE = {
        ' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'
}

GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board and pin layout
GPIO.setup(pinNum,GPIO.OUT) #replace pinNum with whatever pin you used, this sets up that pin as an output

def reset_led(wait_time):
	GPIO.output(pinNum, GPIO.LOW)
	print('sleep:' + str(wait_time))
	time.sleep(wait_time)

def dot():
	GPIO.output(pinNum, GPIO.HIGH)
	time.sleep(DOT_TIME)

def dash():
	GPIO.output(pinNum, GPIO.HIGH)
	time.sleep(DASH_TIME)

def parse_code(code, eow):
	if code == 'x':
		return
	for index, char in enumerate(code):
		print(char)
		if char == '.':
			dot()
		else:
			dash()
		if index < (len(code) - 1):
			reset_led(LETTER_WAIT_TIME)
	if not eow:
		reset_led(WORD_WAIT_TIME)

# handles sleeping between words
def parse_line(line):
	for index, c in enumerate(line.upper()):
		if c == ' ':
			time.sleep(BETWEEN_WORD_WAIT_TIME)
		else:
			if index == (len(line) - 1) or line[index + 1] == ' ':
				parse_code(CODE.get(c, 'x'), True)
			else:
				parse_code(CODE.get(c, 'x'), False)
	reset_led(0.1) # turns off the led while waiting for new input


while True:
	line = input('message: ')
	parse_line(line)

GPIO.cleanup()