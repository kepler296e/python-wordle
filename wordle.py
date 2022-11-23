import numpy as np
import matplotlib.pyplot as plt
import unicodedata as ud


def strip_accents(s):
    return ''.join(c for c in ud.normalize('NFD', s)
                   if ud.category(c) != 'Mn')


def normalize(s):
    return strip_accents(s).strip().replace(" ", "_").upper()


def get_words():
    words = []
    with open("lang/"+langcode+".txt") as f:
        for line in f:
            if len(normalize(line)) == letters:
                words.append(normalize(line))
    return words


def get_array(default):
    arr = []
    for i in range(lines):
        arr.append([])
        for j in range(letters):
            arr[i].append(default)
    return arr


def save_arr():
    fontsize = 30
    plt.rcParams["figure.figsize"] = (letters, lines)
    for row in range(lines+1):
        plt.plot([0, letters*fontsize],
                 [row*fontsize, row*fontsize], color="black")
    for column in range(letters+1):
        plt.plot([column*fontsize, column*fontsize],
                 [0, lines*fontsize], color="black")
    for row in range(lines):
        for column in range(letters):
            plt.text((1/2+column)*fontsize, (lines-row-1/2)*fontsize,
                     arr[row][column], fontsize=fontsize, ha="center", va="center", color=colors[row][column])
    plt.axis("off")
    plt.savefig('wordle.png', bbox_inches='tight')


def add_letters(gword, line):
    for i in range(letters):
        arr[line][i] = gword[i]
        if gword[i] in word:
            if gword[i] == word[i]:
                colors[line][i] = "green"
            else:
                colors[line][i] = "orange"
        else:
            colors[line][i] = "gray"


def ask_to_play_again():
    global again
    again = input("Do you want to play again? (y/n) ")


def play(line=0):
    gword = normalize(input(": "))
    add_letters(gword[:letters].ljust(letters, "_"), line)
    save_arr()
    if gword == word:
        print("You found the word!")
        ask_to_play_again()
    else:
        if line == lines-1:
            print("You lost!, the word was %s" % word)
            ask_to_play_again()
        else:
            play(line+1)


LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "pk": "Pokemon",
    "an": "Anime",
    "ch": "Characters",
    "cs": "Cars"}


def print_languages():
    for key in LANGUAGES:
        print(key + " " + LANGUAGES[key])


again = "y"
while again == "y":
    print("----- Wordle -----")
    print_languages()
    langcode = ""
    while langcode not in LANGUAGES:
        langcode = input("Choose a language: ")
    letters = int(input("How many letters? "))
    words = get_words()
    while len(words) == 0:
        print("There are no words with %d letters in this language" % letters)
        letters = int(input("How many letters? "))
        words = get_words()
    lines = int(input("How many lines? "))
    arr = get_array("")
    colors = get_array("black")
    word = np.random.choice(words)
    plt.close()
    save_arr()
    play()
print("Bye!")
