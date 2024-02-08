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


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
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
    guessed_word=[]
    for char in secret_word:
        if char in letters_guessed:
            guessed_word.append(char)
        else:
            guessed_word.append('_ ')
    return ''.join(guessed_word)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    string_lowcase=list(string.ascii_lowercase)
    for char in letters_guessed:
        if char in string_lowcase:
            string_lowcase.remove(char)
    return ''.join(string_lowcase)

    

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
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secret_word)))
    print("----------")
    guesses_left=6
    letters_guessed=[]
    warning_left=3
    vowels=["a","e","i","o","u"]
    while guesses_left>=0:
        print("You have {} warnings left.".format(warning_left))
        print("You have {} guesses left.".format(guesses_left))
        print("Available letters: {}".format(get_available_letters(letters_guessed)))
        guess_input=input("Please enter a letter: ")
        guess_input = guess_input.lower()
        
        if guess_input.isalpha():
            if guess_input in letters_guessed:
                print("This letter has already been guessed before.")
                if warning_left>=1:
                    warning_left-=1
                else:
                    guesses_left-=1
            else:
                if guess_input in secret_word:
                    letters_guessed.append(guess_input)
                    print("Good guess: {}".format(get_guessed_word(secret_word, letters_guessed)))
                    print("----------")
                    if is_word_guessed(secret_word, letters_guessed)==True:
                        print("Congratulations, you won!")
                        unique_letter = []
                        for u in secret_word:
                            if u not in unique_letter:
                                unique_letter.append(u)
                        total_score= guesses_left*len(unique_letter)
                        print("Your total score is {}.".format(total_score))
                        break
                else:
                    letters_guessed.append(guess_input)
                    print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))
                    print("----------")
                    if guess_input in vowels:
                        guesses_left-=2
                    else:
                        guesses_left-=1
        else:
            warning_left-=1
            if warning_left>=1:
                print("Please enter an alphabet!")
                print("----------")
            else:
                print("Please enter an alphabet!")
                print("----------")
                warning_left=0
                guesses_left-=1
        if guesses_left<=0 and is_word_guessed(secret_word,letters_guessed)==False:
            print("Sorry you lost, the secret word is {}.".format(secret_word))
            break


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
    my_word_no_space = my_word.replace(" ","")
    letter_guessed=[]
    for char in my_word_no_space:
        if char.isalpha():
            letter_guessed.append(char)
            
    if len(my_word_no_space)!=len(other_word):
        return False
    
    for i in range(len(my_word_no_space)):
        current_letter=my_word_no_space[i]
        other_letter=other_word[i]
        if current_letter!=other_letter and current_letter != "_":
            return False
        if current_letter=="_" and other_letter in letter_guessed:
            return False
    return True
        


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matched_word=[]
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matched_word.append(word)    
            
    if len(matched_word)>0:
        return " ".join(matched_word)
    else:
        return print("No matches found.")


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
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secret_word)))
    print("----------")
    guesses_left=6
    letters_guessed=[]
    warning_left=3
    vowels=["a","e","i","o","u"]
    while guesses_left>=0:
        print("You have {} warnings left.".format(warning_left))
        print("You have {} guesses left.".format(guesses_left))
        print("Available letters: {}".format(get_available_letters(letters_guessed)))
        guess_input=input("Please enter a letter: ")
        guess_input = guess_input.lower()
        
        if guess_input.isalpha():
            if guess_input in letters_guessed:
                print("This letter has already been guessed before.")
                if warning_left>=1:
                    warning_left-=1
                else:
                    guesses_left-=1
            else:
                if guess_input in secret_word:
                    letters_guessed.append(guess_input)
                    print("Good guess: {}".format(get_guessed_word(secret_word, letters_guessed)))
                    print("----------")
                    if is_word_guessed(secret_word, letters_guessed)==True:
                        print("Congratulations, you won!")
                        unique_letter = []
                        for u in secret_word:
                            if u not in unique_letter:
                                unique_letter.append(u)
                        total_score= guesses_left*len(unique_letter)
                        print("Your total score is {}.".format(total_score))
                        break
                else:
                    letters_guessed.append(guess_input)
                    print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))
                    print("----------")
                    if guess_input in vowels:
                        guesses_left-=2
                    else:
                        guesses_left-=1
        else:
            if guess_input=="*":
                print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            else:
                warning_left-=1
                if warning_left>=1:
                    print("Please enter an alphabet!")
                    print("----------")
                else:
                    print("Please enter an alphabet!")
                    print("----------")
                    warning_left=0
                    guesses_left-=1
        if guesses_left<=0 and is_word_guessed(secret_word,letters_guessed)==False:
            print("Sorry you lost, the secret word is {}.".format(secret_word))
            break


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
