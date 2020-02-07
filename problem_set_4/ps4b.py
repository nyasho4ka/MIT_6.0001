# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

ALPHABET_SYMBOLS_COUNT = 26


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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')

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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase

        shift_letters_lower = self.get_shifted_letters(letters_lower, shift)
        shift_letters_upper = self.get_shifted_letters(letters_upper, shift)

        shift_letter = self.concat_shifted_letters(shift_letters_lower, shift_letters_upper)
        return shift_letter

    def get_shifted_letters(self, letters, shift):
        shifted_letters = {}

        for letter_position in range(len(letters)):
            shifted_position = self.get_shifted_position(letter_position, shift)
            shifted_letters[letters[letter_position]] = letters[shifted_position]

        return shifted_letters

    @staticmethod
    def get_shifted_position(letter_position, shift):
        return (letter_position + shift) % ALPHABET_SYMBOLS_COUNT

    @staticmethod
    def concat_shifted_letters(first_letters, second_letters):
        first_letters.update(second_letters)
        return first_letters

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_dict = self.build_shift_dict(shift)
        encrypted_message = self.encrypt_message(shifted_dict)
        return encrypted_message

    def encrypt_message(self, shifted_dict):
        message = ''
        for char in self.message_text:
            if char in shifted_dict:
                message += shifted_dict[char]
            else:
                message += char
        return message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = ''

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # variable for max matches
        max_matches = 0
        # variable for max matches shift
        max_matches_shift = 0
        # for every possible shift
        for shift in range(26):
            # shift encrypted message
            message = self.apply_shift(shift)
            # check match count
            match_count = self.get_match_count(message)
            # if matches more than earlier
            if match_count > max_matches:
                # update max matches variable
                max_matches = match_count
                # update max matches shift variable
                max_matches_shift = shift
        # decrypt message with appropriate shift
        decrypted_message = self.apply_shift(max_matches_shift)
        # return tuple of shift and decrypted message
        return ALPHABET_SYMBOLS_COUNT - max_matches_shift, decrypted_message

    def get_match_count(self, message):
        matches = 0
        for word in message.split():
            if word.lower() in self.valid_words:
                matches += 1
        return matches


def test_all_plaintext(user_inputs, expected_outputs):
    actual_outputs = []
    for user_input, shift in user_inputs:
        message = PlaintextMessage(user_input, shift)
        encrypted_message = message.apply_shift(shift)
        actual_outputs.append(encrypted_message)

    if actual_outputs == expected_outputs:
        print("SUCCESS!")
    else:
        print("FAILURE!")

    print()
    print("Expected: {0}".format(expected_outputs))
    print("Actual: {0}".format(actual_outputs))


def test_all_ciphertext(user_inputs, expected_outputs):
    actual_outputs = []
    for user_input in user_inputs:
        message = CiphertextMessage(user_input)
        shift, decrypted_message = message.decrypt_message()
        actual_outputs.append((shift, decrypted_message))
    if actual_outputs == expected_outputs:
        print("SUCCESS!")
    else:
        print("FAILURE!")

    print()
    print("Expected: {0}".format(expected_outputs))
    print("Actual: {0}".format(actual_outputs))


if __name__ == '__main__':
    story = get_story_string()
    mes = CiphertextMessage(story)
    cipher_shift, decrypted_mes = mes.decrypt_message()
    print("Encrypted message is {0}".format(mes.message_text))
    print("------------------------------------------------")
    print("Decrypted message is {0}".format(decrypted_mes))
    print("------------------------------------------------")
    print("Cipher shift is {0}".format(cipher_shift))

    print("************************************************")
    print("INNER TESTS")

    user_inputs_plain = [("Hello, world!", 4), ("My name is nyashochka?", 7), ("I am an engineer.", 10)]
    expected_outputs_plain = ["Lipps, asvph!", "Tf uhtl pz ufhzovjorh?", "S kw kx oxqsxoob."]
    test_all_plaintext(user_inputs_plain, expected_outputs_plain)

    user_inputs_cipher = ["Fyyfhp fy ifbs!", "Jne vf gur nafjre", "B tf ghm t ltbgm"]
    expected_outputs_cipher = [(5, "Attack at dawn!"), (13, "War is the answer"), (19, "I am not a saint")]
    test_all_ciphertext(user_inputs_cipher, expected_outputs_cipher)
