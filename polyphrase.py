import random
import string
import nltk
import argparse
from nltk.corpus import words, swadesh
import secrets
import pyperclip  # For clipboard functionality
pyperclip.set_clipboard("xclip") # hack for Linux.
import zxcvbn  # For password strength checking

class PolyPhraseGenerator:
    def __init__(self):
        """Initialize the password generator with dictionaries"""
        self.min_word_length = 3
        self.max_word_length = 8
        self.english_words, self.french_words, self.spanish_words, self.latin_words = self.setup_dictionaries()
        
    def setup_dictionaries(self):
        """Download and setup word dictionaries with error handling"""
        try:
            # TODO : Download and bundle the dictionaries with the script
            nltk.download('words', quiet=True)
            nltk.download('swadesh', quiet=True)
            english_words = [
                word for word in words.words() 
                if self.is_valid_word(word)
            ]
            
            # Filter words for length and remove potential problematic words
            # I chose to keep accentued words with regular accute and grave accents 
            # that are relatively easy to type on international keybaords
            french_words = [
                word for word in swadesh.words('fr')
                if self.is_valid_word(word)
            ]
            
            spanish_words = [
                word for word in swadesh.words('es')
                if self.is_valid_word(word)
            ]
            
            latin_words = [
                word for word in swadesh.words('la')
                if self.is_valid_word(word)
            ]
            
            return english_words, french_words, spanish_words, latin_words
            
        except LookupError as e:
            print(f"Error loading dictionaries: {e}")
            print("Using fallback word lists...")
            return self._get_fallback_words()

    def is_valid_word(self, word):
        """Check if a word meets our criteria"""
        return (
            len(word) >= self.min_word_length 
            and len(word) <= self.max_word_length
            and word.isalpha()
        )

    def _get_fallback_words(self):
        """Provide minimal word lists in case NLTK fails"""
        return (
            ["apple", "beach", "cloud", "dance", "eagle", "forest", "grape", "house", "island", "jungle"],
            ["amour", "belle", "coeur", "douce", "etoile", "fleur", "goutte", "heure", "ile", "joie"],
            ["agua", "beso", "cielo", "dulce", "estrella", "flor", "gato", "hombre", "isla", "jardin"],
            ["amor", "bellum", "caelum", "dulcis", "stella", "flos", "felis", "homo", "insula", "hortus"]
        )

    def generate_special_token(self):
        """Generate a cryptographically secure special token"""
        number = str(secrets.randbelow(10))
        symbol = secrets.choice("!@#$%&*()_+-=[]{};:,.<>?")
        letter = secrets.choice(string.ascii_letters).capitalize()
        elements = [number, symbol, letter]
        random.shuffle(elements)
        return ''.join(elements)

    def generate_password(self, num_words, language, max_length):
        """Generate a secure password with specified number of words"""
        language_options = {
            'poly': [self.english_words, self.french_words, self.spanish_words, self.latin_words],
            'english': [self.english_words],
            'french': [self.french_words],
            'spanish': [self.spanish_words],
            'latin': [self.latin_words]
        }

        if language not in language_options:
            raise ValueError("Unsupported language.")

        word_lists = language_options[language]
        selected_words = []
        
        # Use secrets for cryptographic operations
        for _ in range(num_words):
            word_list = secrets.choice(word_lists)
            word = secrets.choice(word_list)
            selected_words.append(word)
        
        special_token = self.generate_special_token()
        elements = selected_words + [special_token]
        random.shuffle(elements)
        
        # return " ".join(elements)

        password = " ".join(elements)
        
        # Double check length and adjust if needed
        if len(password) < 16:
            # Add another word if too short
            word_list = secrets.choice(word_lists)
            word = secrets.choice(word_list)
            elements.append(word)
            password = " ".join(elements)
        elif len(password) > 32:
            # Remove a word if too long
            elements.pop(0)
            password = " ".join(elements)
            
        return password

    def check_password_strength(self, password):
        """Check password strength using zxcvbn"""
        result = zxcvbn.zxcvbn(password)
        return {
            'score': result['score'],  # 0-4
            'crack_time': result['crack_times_display']['offline_fast_hashing_1e10_per_second'],
            'suggestions': result['feedback']['suggestions']
        }

def main():
    parser = argparse.ArgumentParser(description='Generate secure and somewhat memorable multilingual passwords')
    parser.add_argument('-n', '--num-passwords', type=int, default=3,
                       help='Number of passwords to generate')
    parser.add_argument('-w', '--words', type=int, default=4,
                       help='Number of words per password')
    parser.add_argument('-m', '--max-length', type=int, default=32,
                       help='Max length of password password')
    parser.add_argument('-p', '--password', type=str,
                       help='Check the strength of an existing password')
    parser.add_argument('-l', '--language', type=str, choices=['english','french','latin', 'spanish', 'poly'], default='poly',
                       help='Language of the words in the password')
    # parser.add_argument('-c', '--copy', action='store_true',
    #                    help='Copy the first generated password to clipboard')
    args = parser.parse_args()

    generator = PolyPhraseGenerator()
    print("\nGenerating secure passphrases...")
    if args.password:
        strength = generator.check_password_strength(args.password)
        print(f"Strength: {strength['score']}/4")
        print(f"Estimated crack time: {strength['crack_time']}")
        
        if strength['suggestions']:
            print("Suggestions:", ', '.join(strength['suggestions']))
        return
    
    for i in range(args.num_passwords):
        password = generator.generate_password(args.words, args.language, args.max_length)
        strength = generator.check_password_strength(password)
        
        print(f"\nPolyPhrase {i+1}: \n\033[1m{password}\033[0m")
        print(f"Strength: {strength['score']}/4\t\tCrack time: {strength['crack_time']}\t\tlength: {len(password)}")
        
        if strength['suggestions']:
            print("Suggestions:", ', '.join(strength['suggestions']))
            
        if i == 0 :
            try:
                pyperclip.copy(password)
                print("(Copied to clipboard)")
            except pyperclip.PyperclipException:
                print("Failed to copy to clipboard. Ensure 'xclip' or 'xsel' is installed.")

    print("\nNote: Store these passwords securely and never share them.")

if __name__ == "__main__":
    main()
