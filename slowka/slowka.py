#!/usr/bin/python
import sys
import codecs

def main():
    if len(sys.argv) == 1:
        print("usage: ./slowka.py FILENAME")
        quit()

    words = []

    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        i = 0
        for line in f:
            i += 1
            try:
                en, pl = line.split(':')
            except ValueError:
                raise ValueError(f'Cannot split line {i}')
            words.append((en.strip(), pl.strip()))

    x = input('pl->en(1) or en->pl(2)? ')

    while True:
            for en, pl in words:
                to_guess = en if x == '1' else pl
                word = pl if x=='1' else en
                try:
                    answer = input(word + ': ')
                except UnicodeError:
                    answer = input(word.encode('ascii', 'replace').decode('ascii') + ': ')
                if answer == to_guess:
                    print('Correct! - ', end='')
                try:
                    print(to_guess)
                except UnicodeError:
                    print(to_guess.encode('ascii', 'replace').decode('ascii'))

if __name__ == '__main__':
    main()

