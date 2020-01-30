# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for char in secret_word:
        if char not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ''

    for char in secret_word:
        if char in letters_guessed:
            result += char
        else:
            result += '_ '

    return result


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    result = ''
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            result += char
    return result
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses = 6
    warnings = 3
    word_len = len(secret_word)
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of the word that is {0} letters long".format(word_len))
    while not is_word_guessed(secret_word, letters_guessed) and guesses != 0:
        print("----------------")
        print("You have {0} guesses left".format(guesses))
        print("You have {0} warnings left".format(warnings))
        print("Available letters: {0}".format(get_available_letters(letters_guessed)))

        user_input = input("Enter a letter: ").lower()

        if not is_user_input_valid(user_input, letters_guessed):
            print("Invalid input! {0} is not alphabetical or already guessed".format(user_input))
            print(get_guessed_word(secret_word, letters_guessed))
            if warnings > 0:
                warnings -= 1
            else:
                guesses -= 1
            continue

        if user_input in secret_word:
            print("Good guess: ", end=' ')
        else:
            print("Oops! That letter is not in my word: ", end=' ')
            guesses -= get_user_input_penalty(user_input)

        letters_guessed.append(user_input)

        print(get_guessed_word(secret_word, letters_guessed))

    if is_word_guessed(secret_word, letters_guessed):
        total_score = guesses * len(set(secret_word))
        print("Congratulations! You won the game! Your score is {0}".format(total_score))
    else:
        print("Sorry, you lose it.")
    print('"{0}" is the guessed word'.format(secret_word))


def is_user_input_valid(user_input, letters_guessed):
    return user_input.isalpha() and user_input not in letters_guessed


def get_user_input_penalty(user_input):
    vowels = 'aeiou'
    if user_input in vowels:
        return 2
    return 1


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.strip().replace('_ ', '_')
    other_word = other_word.strip()


    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != '_' and not my_word[i] == other_word[i]:
            return False

    # get unique word chars
    unique_letters = get_unique_letters(my_word)

    # get gasp positions
    gasp_positions = get_gasp_positions(my_word)

    for pos in gasp_positions:
        if other_word[pos] in unique_letters:
            return False

    return True


def get_unique_letters(my_word):
    unique_letters = set(my_word)
    unique_letters.remove('_')
    return unique_letters


def get_gasp_positions(my_word):
    positions = []
    for i in range(len(my_word)):
        if my_word[i] == '_':
            positions.append(i)
    return positions


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match_words = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            match_words.append(word)
    if len(match_words) == 0:
        print("No matches found")
        return
    for word in match_words:
        print(word, end=' ')
    print()


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses = 6
    warnings = 3
    word_len = len(secret_word)
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of the word that is {0} letters long".format(word_len))
    while not is_word_guessed(secret_word, letters_guessed) and guesses != 0:
        print("----------------")
        print("You have {0} guesses left".format(guesses))
        print("You have {0} warnings left".format(warnings))
        print("Available letters: {0}".format(get_available_letters(letters_guessed)))

        user_input = input("Enter a letter: ").lower()

        if user_input == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        if not is_user_input_valid(user_input, letters_guessed):
            print("Invalid input! {0} is not alphabetical or already guessed".format(user_input))
            print(get_guessed_word(secret_word, letters_guessed))
            if warnings > 0:
                warnings -= 1
            else:
                guesses -= 1
            continue

        if user_input in secret_word:
            print("Good guess: ", end=' ')
        else:
            print("Oops! That letter is not in my word: ", end=' ')
            guesses -= get_user_input_penalty(user_input)

        letters_guessed.append(user_input)

        print(get_guessed_word(secret_word, letters_guessed))

    if is_word_guessed(secret_word, letters_guessed):
        total_score = guesses * len(set(secret_word))
        print("Congratulations! You won the game! Your score is {0}".format(total_score))
    else:
        print("Sorry, you lose it.")
    print('"{0}" is the guessed word'.format(secret_word))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
