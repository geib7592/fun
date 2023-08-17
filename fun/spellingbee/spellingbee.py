import sys
import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

with open("/usr/share/dict/words", "r") as f:
    WORDS = [line.rstrip() for line in f if len(line.rstrip()) > 3 and all(letter in ALPHABET for letter in line.rstrip())]

def get_letters(n, rand=False):
    if rand:
        return random.sample(ALPHABET, n)
    else:
        pan = random.choice(all_pangrams(n))
        return random.sample(list(set(pan)), n)

def possible_words(letters):
    return [word for word in WORDS if all(letter in letters for letter in word) and letters[0] in word]

def all_pangrams(n):
    return [word for word in WORDS if len(set(word)) == n]

def pangrams(letters, pos):
    return [word for word in pos if all(letter in word for letter in letters)]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        letters = list(sys.argv[1].lower())
    else:
        letters = get_letters(7)
    print("Letters:", letters)
    pos = possible_words(letters)
    print("Possible Words (" + str(len(pos)) + "):", pos)
    pans = pangrams(letters, pos)
    print("Pangrams (" + str(len(pans)) + "):", pans)