"""
Problem Set 4C - substitution cipher
"""
import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower_keys = list(VOWELS_LOWER) + list(CONSONANTS_LOWER)
        lower_values = list(vowels_permutation.lower()) + list(CONSONANTS_LOWER)
        upper_keys = list(VOWELS_UPPER) + list(CONSONANTS_UPPER)
        upper_values = list(vowels_permutation.upper()) + list(CONSONANTS_UPPER)
        
        keys = lower_keys + upper_keys
        values = lower_values + upper_values
        
        self.transpose_dict = dict(zip(keys, values))
        return self.transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encrypted_msg_list = []
        
        for char in self.get_message_text():
            if char in transpose_dict:
                encrypted_msg_list.append(transpose_dict[char])
            else: #space and punctuations
                encrypted_msg_list.append(char)
        
        self.encrypted_msg_text = ''.join(encrypted_msg_list)
        return self.encrypted_msg_text
        
def apply_transpose(self, transpose_dict):
    return ''.join([transpose_dict.get(ch, ch) for ch in self.get_message_text()])

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''        
        most_en_words = 0
        most_decrypted_msg = self.get_message_text()
        for permutation in get_permutations(VOWELS_LOWER):
            transpose_dict = self.build_transpose_dict(permutation)
            decrypted_msg = self.apply_transpose(transpose_dict)
            current_en_words = 0
            for word in decrypted_msg.split():
                if is_word(self.get_valid_words(), word):
                    current_en_words += 1
            if current_en_words > most_en_words:
                most_en_words = current_en_words
                most_decrypted_msg = decrypted_msg

        return most_decrypted_msg

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    message_ = SubMessage("Jack Florey is a mythical character.")
    permutation_ = 'uiaeo'
    enc_dict_ = message_.build_transpose_dict(permutation_)
    print("Original message:", message_.get_message_text(), "Permutation:", permutation_)
    print("Expected encryption:", "Juck Fleriy as u mythacul chuructir.")
    print("Actual encryption:", message_.apply_transpose(enc_dict_))
    enc_message_ = EncryptedSubMessage(message_.apply_transpose(enc_dict_))
    print("Decrypted message:", enc_message_.decrypt_message())