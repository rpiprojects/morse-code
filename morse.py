import RPi.GPIO as GPIO
import time

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
	time.sleep(wait_time)

def dot():
	GPIO.output(pinNum, GPIO.HIGH)
	time.sleep(DOT_TIME)

def dash():
	GPIO.output(pinNum, GPIO.HIGH)
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
	line = input('message: ')
	if line == 'q()':
		break;
	parse_line(line)

GPIO.cleanup()