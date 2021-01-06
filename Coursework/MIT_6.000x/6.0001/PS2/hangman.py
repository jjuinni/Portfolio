"""
Problem Set 2 - The Handman Game
"""
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
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word_list = list(secret_word) #converts string to list
    
    #compare secret_word_list with letters_guessed and remove if there is a match
    secret_word_list_copy = secret_word_list[:]
    for e in secret_word_list_copy:
        if e in letters_guessed:
            secret_word_list.remove(e)
    
    if secret_word_list == []:#secret_word was guessed
        return True
    else:
        return False

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word_list = list(secret_word)
    secret_word_list_copy = secret_word_list[:]
    guessed_word = []
    unknown_letter = '_ '
    
    #compare secret_word_list with letters_guessed and add according char to new list(guessed_word)
    for e in secret_word_list_copy:
        if e in letters_guessed:
            guessed_word.append(e)
        else:
            guessed_word.append(unknown_letter)  
    guessed_word_string = ''.join(guessed_word)
    return guessed_word_string #get_guessed_word returns a string type

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    alphabet_list = list(alphabet)
    alphabet_list_copy = alphabet_list[:]
    
    #compare letters_guessed with alphabet_list and remove guessed letters
    for e in letters_guessed:
        if e in alphabet_list_copy:
            alphabet_list.remove(e)
            
    letters_not_guessed = ''.join(alphabet_list)
    return letters_not_guessed

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
    #Game initialization messages
    warnings = 3
    letters_guessed = []
    guesses = 6
    
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long')
    print('You have', warnings, 'warnings left')
    print('-------------')
    
    penality_flag = False #Keeps track of penality happening. Prevent double penalties in a single attempt
    #Game on
    while guesses != 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You have', guesses, 'guesses left')
        print('Available letters:', get_available_letters(letters_guessed))
        
        #User input requirements: lowercase and alphabet string
        user_input = str.lower(input('Please guess a letter: '))
            
        #Append to guessed letters only if it is an alphabet string
        if str.isalpha(user_input) == True:
            #prevents adding letters already guessed
            if user_input not in letters_guessed: 
                letters_guessed.append(user_input) #NOTE. https://stackoverflow.com/questions/3840784/appending-turns-my-list-to-nonetype
            elif user_input in letters_guessed and penality_flag == False:
                if warnings != 0:
                    warnings -= 1
                    penality_flag = True
                    print('Oops! You\'ve already guessed that letter. You now have', warnings, 'warnings: ', get_guessed_word(secret_word, letters_guessed))
                else:
                    guesses -= 1
                    penality_flag = True
                    print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
       
        if user_input in secret_word and penality_flag == False:
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        #letters_guessed not in secret_word_list 
        elif str.isalpha(user_input) == True and penality_flag == False:
            guesses -= 1
            #double penalty for vowels only
            vowels = 'aeiou' 
            if user_input in vowels:
                guesses -= 1
            penality_flag = True
            print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
            
        if str.isalpha(user_input) == False and penality_flag == False:
            if warnings != 0:
                warnings -= 1
                penality_flag = True
                print('Oops! That is not a valid letter. You have', warnings , 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            elif warnings == 0:
                guesses -= 1
                penality_flag = True
                print('Oops! That is not a valid letter. You have', guesses , 'guesses left:', get_guessed_word(secret_word, letters_guessed))
        
        penality_flag = False #Reset flag
        print('-------------')
        
    #Game termination when out of while loop

    #calculate the number of unique letters in the word
    unique_letters = ''
    for letter in secret_word:
        if letter not in unique_letters:
            unique_letters += letter
            
    if is_word_guessed(secret_word, letters_guessed) == True:
        total_score = guesses*len(unique_letters)
        print('Congratulations, you won!')
        print('Your total score for this game is: ', total_score)
    elif guesses == 0:
        print('Sorry, you ran out of guesses. The word was ' + secret_word + ' .')


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
    my_word_no_gaps = my_word.replace(" ","") #remove all whitespaces
    
    if len(my_word_no_gaps) == len(other_word):
        my_word_for_list = []
        for i in range (len(other_word)):
            if my_word_no_gaps[i] == other_word[i] or my_word_no_gaps[i] == '_':   
                my_word_for_list.append(my_word_no_gaps[i])
            my_word_for = ''.join(my_word_for_list)
        #Entering below 'if' means all letters were compared.
        if my_word_for == my_word_no_gaps:
            return True
        else:
            return False
    else:
        return False

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    first_match_flag = False
    for word in wordlist:
        if match_with_gaps(my_word, word) == True:
            first_match_flag = True
            print(word, end =" ")
    for word in wordlist:
        if match_with_gaps(my_word, word) == False and first_match_flag == False:
            print('No matches found')
            break
        
    #Just to eliminate 'None' that will be prompted as our function has no return.
    str = '!'
    return str

#Example Usage
#print(show_possible_matches("t_ _ t"))
#tact tart taut teat tent test text that tilt tint toot tort tout trot tuft twit
#print(show_possible_matches("abbbb_ "))
#No matches found
#print(show_possible_matches("a_ pl_ "))
#ample amply



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
    #Game initialization messages
    warnings = 3
    letters_guessed = []
    guesses = 6
    hint_use = 1
    
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long')
    print('You have', warnings, 'warnings left')
    print('You can ask for one hint during the game by entering *')
    print('-------------')
    
    penality_flag = False #Keeps track of penality happening. Prevent double penalties in a single attempt
    #Game on
    while guesses != 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You have', guesses, 'guesses left')
        print('Available letters:', get_available_letters(letters_guessed))
        
        #User input requirements: lowercase and alphabet string
        user_input = str.lower(input('Please guess a letter: '))
        
        #Hint
        if user_input == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            hint_use -= 1
            penality_flag = True #User should not lose a guess or warning. This will skip all possible penality conditions.
            if hint_use <= 0:
                print('!!! You used your hint !!!')
            
        #Append to guessed letters only if it is an alphabet string
        if str.isalpha(user_input) == True:
            #prevents adding letters already guessed
            if user_input not in letters_guessed: 
                letters_guessed.append(user_input) #NOTE. https://stackoverflow.com/questions/3840784/appending-turns-my-list-to-nonetype
            elif user_input in letters_guessed and penality_flag == False:
                if warnings != 0:
                    warnings -= 1
                    penality_flag = True
                    print('Oops! You\'ve already guessed that letter. You now have', warnings, 'warnings: ', get_guessed_word(secret_word, letters_guessed))
                else:
                    guesses -= 1
                    penality_flag = True
                    print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
       
        if user_input in secret_word and penality_flag == False:
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        #letters_guessed not in secret_word_list 
        elif str.isalpha(user_input) == True and penality_flag == False:
            guesses -= 1
            #double penalty for vowels only
            vowels = 'aeiou' 
            if user_input in vowels:
                guesses -= 1
            penality_flag = True
            print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
            
        if str.isalpha(user_input) == False and penality_flag == False:
            if warnings != 0:
                warnings -= 1
                penality_flag = True
                print('Oops! That is not a valid letter. You have', warnings , 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            elif warnings == 0:
                guesses -= 1
                penality_flag = True
                print('Oops! That is not a valid letter. You have', guesses , 'guesses left:', get_guessed_word(secret_word, letters_guessed))
        
        penality_flag = False #Reset flag
        print('-------------')
        
    #Game termination when out of while loop

    #calculate the number of unique letters in the word
    unique_letters = ''
    for letter in secret_word:
        if letter not in unique_letters:
            unique_letters += letter
            
    if is_word_guessed(secret_word, letters_guessed) == True:
        total_score = guesses*len(unique_letters)
        print('Congratulations, you won!')
        print('Your total score for this game is: ', total_score)
    elif guesses == 0:
        print('Sorry, you ran out of guesses. The word was ' + secret_word + ' .')
    input('Press any key to exit')


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
#     pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
#    secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
 