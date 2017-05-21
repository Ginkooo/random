#!/usr/bin/python
import sys

if len(sys.argv) == 1:
    print("usage: ./slowka.py FILENAME")
    quit()

words = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        en, pl = line.split(':')
        words.append((en.strip(), pl.strip()))

x = input('pl->en(1) or en->pl(2)? ')

while True:
    for en, pl in words:
        to_guess = en if x == '1' else pl
        word = pl if to_guess is en else pl
        answer = input(word + ': ')
        if answer in to_guess:
            print('Correct! - ', end='')
        print(to_guess)
