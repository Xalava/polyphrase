import nltk
import os
import time
import re

def download_words():
    # Create a directory for downloaded resources if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download required NLTK data - we need both wordnet and omw
    print("Downloading required NLTK resources...")
    nltk.download('wordnet')  # Required as a base for OMW
    nltk.download('omw-1.4')  # The multilingual extension
    nltk.download('swadesh')  # Swadesh list for fallback

    from nltk.corpus import wordnet as wn
    from nltk.corpus import swadesh

    # Language codes and their names
    languages = {
        'eng': 'English',
        'fra': 'French',
        'spa': 'Spanish', 
        'lat': 'Latin'
    }

    # This pattern allows lowercase a-z and some accented lowercase letters commmonly accessible on international keyboards
    # Todo, could be adjusted to different needs
    valid_pattern = re.compile(r'^[a-zàáèéêëîïíìôöòóõùûüúÿñ]+$')

    # Process each language
    for lang_code, lang_name in languages.items():
        start_time = time.time()
        print(f"\nExtracting {lang_name} words from OMW...")
        
        # Will store only the clean words that pass our filter
        clean_words = set()
        
        # Use the Swadesh list for Latin (not in OMW)
        if lang_code == 'lat':
            print(f"No OMW data found for {lang_name}. Using Swadesh list as fallback.")
            for word in swadesh.words(lang_code[:-1]):
                if valid_pattern.match(word):
                    clean_words.add(word)
        else:
            # Process all synsets to extract words
            for synset in list(wn.all_synsets()):
                for word in synset.lemma_names(lang_code):
                    if valid_pattern.match(word):
                        clean_words.add(word)
        
        # Convert to sorted list
        clean_words = sorted(list(clean_words))
        
        print(f"Extracted and cleaned {len(clean_words)} {lang_name} words in {time.time() - start_time:.2f} seconds")
        
        # Save as plain text file (one word per line)
        text_path = f'data/{lang_code}_words.txt'
        with open(text_path, 'w', encoding='utf-8') as f:
            for word in clean_words:
                f.write(word + '\n')
        
        print(f"{lang_name} clean words saved to {text_path}")
        
        # Sample output of first 20 words
        print(f"\nSample of first 20 {lang_name} clean words:")
        for word in clean_words[:20]:
            print(word)

    print("\nWord extraction and cleaning complete for all languages")

if __name__ == '__main__':
    download_words()