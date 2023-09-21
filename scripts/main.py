import os
from pathlib import Path
import sys
import clean_article_text
# import _ask_gpt
from file_selector import select_file
from os.path import isfile
import file_reader
from ask_gpt import GPTAsker
from inputimeout import inputimeout, TimeoutOccurred

def main():
    if isfile(".DS_Store"):
        os.remove(".DS_Store")

    filename = ""
    orig_article_text = ""
    # if len(sys.argv) < 2 and original_article.txt exists:
    if len(sys.argv) > 1 and isfile(sys.argv[1]):
        filename = sys.argv[1]
    elif isfile("original_article.txt"):
        filename = "original_article.txt"
    
    else:
        try:
            response = inputimeout(prompt='Is the article a Google Doc? (y/n) ', timeout=5).lower()
        except TimeoutOccurred:
            response = 'n'

        if response in "tyu":  # accounts for typos
            gdocs_url = input("Google Docs URL: ")
            orig_article_json = file_reader.FileReader.read_article(gdocs_url=gdocs_url)
            orig_article_text = file_reader.FileReader.parse_article(orig_article_json)
        else:
            while not isfile(filename):
                # let user scroll through and select a file
                filename = select_file()
            
    
    try:
        if not orig_article_text:
            orig_article_paragraphs_list = file_reader.FileReader.read_article(filename)
            orig_article_text = file_reader.FileReader.parse_article(orig_article_paragraphs_list)
    
        cleaned_article = clean_article_text.replace_punctuation(orig_article_text)
        print("Article with punctuation fixed:")
        print(cleaned_article)

        clean_article_text.print_punctuation_mistakes(orig_article_text)

        auth_path = Path(__file__).resolve().parent.parent / "auth"
        openai_api_key_path = os.path.join(auth_path, "openai_api_key.config")
        gpt = GPTAsker(openai_api_key_path)
        gpt.ask_gpt(cleaned_article)
        gpt.parse_response()
        gpt.print_uncopyable_response()
        gpt.copy_parsed_response()
        gpt.print_copyable_response()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)