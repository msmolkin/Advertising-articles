import os
import re

import pyperclip
import file_reader


def replace_punctuation(text):
    """ Fix punctuation in article and return fixed text:

    Usage:
    text = '“Hello,” she said. ‘How are you?’'
    result = replace_punctuation(text)
    print(result)
    ```

    Output:
    ```
    "Hello," she said. 'How are you?'
    ```
    """

    # map nonstandard punctuation marks to their simple counterparts
    punctuation_map = {
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '❝': '"',
        '❞': '"',
        '‛': "'",
        '„': '"',
        '‟': '"',
    }
    
    # Use regex to find all nonstandard punctuation marks and replace them with simple punctuation
    for nonstandard, simple in punctuation_map.items():
        text = re.sub(re.escape(nonstandard), simple, text)
    
    print("Copying the fixed article to the clipboard. Please press any key to continue...")
    input()
    pyperclip.copy(text)
    return text

def _find_punctuation_mistakes(text):
    words_with_mistakes = []
    all_words = text.split()
    for word in all_words:
        if re.search(r'[“”‘’]', word):
            words_with_mistakes.append(word)
    # The point of the text below is to make it easier to search for the response in the terminal
    return f"Problematic words with mistakes that need to be changed: {words_with_mistakes}" if len(words_with_mistakes) > 0 else "No punctuation needs to be changed."

def print_punctuation_mistakes(text):
    print(_find_punctuation_mistakes(text))


if __name__ == "__main__":
    filename = input("filename: ") # "802B7D14 Lore.txt"
    try:
        orig_article_text = file_reader.read_article(filename)
    
        # result = replace_punctuation(orig_article_text)
        # print("Article with punctuation fixed:")
        # print(result)

        print_punctuation_mistakes(orig_article_text)
    except FileNotFoundError:
        print(f"{filename} does not exist or couldn't be found in the current directory: {os.getcwd()}")
    except Exception as e:
        print(f"An error occurred: {e}")