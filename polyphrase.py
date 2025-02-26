import random
import string
import argparse
import secrets
import os
import pyperclip  # For clipboard functionality
import sys       
from download_words import download_words 
import zxcvbn  # For password strength checking

class PolyPhraseGenerator:
    def __init__(self, data_dir):
        """Initialize the password generator with local dictionaries"""
        self.data_dir = data_dir
        self.min_word_length = 3
        self.max_word_length = 8
        self.english_words, self.french_words, self.spanish_words, self.latin_words = self.setup_dictionaries()
        
    def setup_dictionaries(self):
        """Load word dictionaries from local files"""
        try:
            # Check if the data directory exists
            if not os.path.exists(self.data_dir):
                print(f"Error: Data directory '{self.data_dir}' not found.")
                print("Attempting to download word lists...")
                try:
                    download_words()
                except Exception as e:
                    print(f"Error downloading word lists: {e}")
                    print("Please run the word extractor script first.")
                    return self._get_fallback_words()
            
            english_words = self._load_language_words('eng')
            french_words = self._load_language_words('fra')
            spanish_words = self._load_language_words('spa')
            latin_words = self._load_language_words('lat')
                            
            return english_words, french_words, spanish_words, latin_words
            
        except Exception as e:
            print(f"Error loading dictionaries: {e}")
            print("Using fallback word lists...")
            return self._get_fallback_words()
    
    def _load_language_words(self, lang_code):
        """Load words for a specific language from text file"""
        try:
            file_path = os.path.join(self.data_dir, f'{lang_code}_words.txt')
            if not os.path.exists(file_path):
                print(f"Warning: Language file '{file_path}' not found.")
                print("Using fallback words.")
                return self.get_fallback_words(lang_code)
                
            with open(file_path, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            return [word for word in words if self.is_valid_word(word)]
        except Exception as e:
            print(f"Error loading {lang_code} words: {e}")
            print("Using fallback words.")
            return self.get_fallback_words(lang_code)

    def is_valid_word(self, word):
        """Check if a word meets our criteria"""
        return (
            len(word) >= self.min_word_length 
            and len(word) <= self.max_word_length
            # Other conditions are filtered at download
            # and word.isalpha() 
            # and all(c in "áàâäéèêëíìîïóòôöúùûüçñ" for c in word)
        )

    def get_fallback_words(self, lang_code):
        """Provide minimal word lists in case loading fails"""
        fallback_words = {
            'eng': ["apple", "beach", "cloud", "dance", "eagle", "forest", "grape", "house", "island", "jungle"],
            'fra': ["amour", "belle", "coeur", "douce", "etoile", "fleur", "goutte", "heure", "ile", "joie"],
            'spa': ["agua", "beso", "cielo", "dulce", "estrella", "flor", "gato", "hombre", "isla", "jardin"],
            'lat': ["amor", "bellum", "caelum", "dulcis", "stella", "flos", "felis", "homo", "insula", "hortus"]
        }
        return fallback_words.get(lang_code, [])

    def generate_special_token(self):
        """Generate a cryptographically secure special token"""
        number = str(secrets.randbelow(10))
        symbol = secrets.choice("!@#$%&*()_+-=[]{};:,.<>?")
        letter = secrets.choice(string.ascii_letters).capitalize()
        elements = [number, symbol, letter]
        random.shuffle(elements)
        return ''.join(elements)

    def generate_password(self, num_words, language, max_length, min_length):
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
        if len(word_lists) == 0:
            raise ValueError("No word lists found for the selected language.")
        selected_words = []
        
        # Use secrets for cryptographic operations
        for _ in range(num_words):
            word_list = secrets.choice(word_lists)
            word = secrets.choice(word_list)
            selected_words.append(word)
        
        special_token = self.generate_special_token()
        elements = selected_words + [special_token]
        random.shuffle(elements)
        
        password = " ".join(elements)
        
        # Double check length and adjust if needed.
        # Quirk: Min will take precedence over max as we check it in order. It seems more secure
        # It shouldn't be a problem with defaults (max length of word is 8, gap is 16)
        if len(password) > max_length:
            # Remove a word if too long, avoiding the special token
            if elements[-1] == special_token:
                elements.pop(-1)
            else:
                elements.pop(0)
        if len(password) < min_length:
            # Add another word if too short
            word_list = secrets.choice(word_lists)
            word = secrets.choice(word_list)
            elements.append(word)
            password = " ".join(elements)
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
    parser = argparse.ArgumentParser(description='Generate secure and somewhat memorable multilingual passwords.')
    parser.add_argument('-n', '--num-passwords', type=int, default=3,
                       help='Number of passwords to generate')
    parser.add_argument('-w', '--words', type=int, default=3,
                       help='Number of words per password (default 3, adjusted to meet length requirements)')
    parser.add_argument('-m', '--max-length', type=int, default=32,
                       help='Max length of password password (default 32)')
    parser.add_argument('-i', '--min-length', type=int, default=16,
                       help='Min length of password password (default 16)')
    parser.add_argument('-p', '--password', type=str,
                       help='Check the strength of an existing password')
    parser.add_argument('-l', '--language', type=str, choices=['english','french','latin', 'spanish', 'poly'], default='poly',
                       help='Language of the words in the password')
    parser.add_argument('-d', '--data-dir', type=str, default='data',
                       help='Directory containing word list files (default: data)')
    args = parser.parse_args()

    generator = PolyPhraseGenerator(data_dir=args.data_dir)
    print("\nGenerating secure passphrases...")
    if args.password:
        strength = generator.check_password_strength(args.password)
        print(f"Strength: {strength['score']}/4")
        print(f"Estimated crack time: {strength['crack_time']}")
        
        if strength['suggestions']:
            print("Suggestions:", ', '.join(strength['suggestions']))
        return
    
    for i in range(args.num_passwords):
        password = generator.generate_password(args.words, args.language, args.max_length, args.min_length)
        strength = generator.check_password_strength(password)
        
        print(f"\nPolyPhrase {i+1}: \n\033[1m{password}\033[0m")
        print(f"Strength: {strength['score']}/4\t\tCrack time: {strength['crack_time']}\t\tlength: {len(password)}")
        
        if strength['suggestions']:
            print("Suggestions:", ', '.join(strength['suggestions']))
            
        if i == 0 :
            if sys.platform.startswith('linux'):
                try:
                    pyperclip.set_clipboard('xclip')
                except pyperclip.PyperclipException:
                    try:
                        pyperclip.set_clipboard('xsel')
                    except pyperclip.PyperclipException:
                        pass  
            try:
                pyperclip.copy(password)
                print("(Copied to clipboard)")
            except pyperclip.PyperclipException:
                print("Failed to copy to clipboard. Ensure 'xclip' or 'xsel' is installed.")

    print("\nNote: Store these passwords securely and never share them.")

if __name__ == "__main__":
    main()
