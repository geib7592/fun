import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

with open("/usr/share/dict/words", "r") as f:
    words = [line.rstrip() for line in f]
WORDS = []
for word in words:
    if len(word) > 3 and all(letter in ALPHABET for letter in word):
        WORDS.append(word)

def get_letters(n, rand=False):
    if rand:
        return random.sample(ALPHABET, n)
    else:
        all_pans = all_pangrams(n)
        pan = all_pans[random.randint(0, len(all_pans))]
        return random.sample(list(set(pan)), n)

def possible_words(letters):
    pos = []
    for word in WORDS:
        if all(letter in letters for letter in word) and letters[0] in word:
            pos.append(word)
    return pos

def all_pangrams(n):
    all_pans = []
    for word in WORDS:
        if len(set(word)) == n:
            all_pans.append(word)
    return all_pans

def pangrams(letters, pos):
    pans = []
    for word in pos:
        if all(letter in word for letter in letters):
            pans.append(word)
    return pans

if __name__ == "__main__":
    letters = get_letters(7)
    print("Letters:", letters)
    pos = possible_words(letters)
    print("Possible Words (" + str(len(pos)) + "):", pos)
    pans = pangrams(letters, pos)
    print("Pangrams:", pans)