from requests import get
from random import randint
from yaml import safe_load
from colorama import Fore, Back, Style
from time import time

'''
0 - correction location
1 - exists / wrong location
2 - none

'''
colors = [Back.GREEN, Back.YELLOW, Back.RED, Back.CYAN]
results = False
tries = 6

def clear_last_line():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE, end = '')

def print_guess(guess, colour):
    clear_last_line()
    for i in range(5):
        print(Fore.BLACK + colors[colour[i]] + guess[i], end = '')
    print(Style.RESET_ALL)

def print_answer(word, prog):
    print(Fore.BLACK + prog + word + Style.RESET_ALL, end = '')
    print(Style.RESET_ALL)

def generate_word_list(config_file):
    data_source = config_file['DATA']['SOURCE']
    response = get(data_source)
    return response.text.split()

def intersection(lst1, lst2):
    return len(list(set(lst1) & set(lst2)))

def compare(word, guess, colors_mapping):
    size = len(guess)
    if size < 5 or size > 5:
        print("invalid size, 5 letters only")
        return False
    for i in range(5):
        letter = guess[i]
        if letter is word[i]:
            colors_mapping[i] = 0
        elif letter in word:
            colors_mapping[i] = 1
        else:
            colors_mapping[i] = 2
    print_guess(guess, colors_mapping)
    return True if intersection([1, 2], colors_mapping) == 0 else False
    
def six_guesses(word):
    print("~Broke Wordle~")
    i = 0
    while(tries > i):
        i += 1
        guess = input().lower()
        colors_mapping = [2,2,2,2,2]
        results = compare(word, guess, colors_mapping) 
        if results or guess == "answer": 
            break
    if results:
        print_answer("Winner!", colors[0])
    else:
        print_answer("Loser!\nAnswer: " + word, colors[2])
    return i

def main():    
    with open('im/config.yml', 'r') as file:
        config_file = safe_load(file)
    data_size = config_file['DATA']['SIZE']
    words = generate_word_list(config_file)
    start_time = 0
    end_time = 0
    while(1):
        start_time = time()
        try_ct = six_guesses(words[randint(0, data_size-1)])
        end_time = time()
        minutes = int((end_time - start_time)/60)
        secounds = round((end_time - start_time)%60, 2)
        print_answer(" ".join(["Time Lapse:", str(minutes), "min(s)",  str(secounds), "second(s)","\nTries:", str(try_ct)]), colors[3])

if __name__ == '__main__':
    main()