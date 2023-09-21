import os

def list_files():
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "articles"))
    
    text_document_extensions = (".txt", ".rtf", ".docx", ".pdf")
    files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(text_document_extensions)]
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    return files

def select_file():
    while True:
        files = list_files()
        try:
            choice = int(input("Select the file by entering its number: ")) - 1
            filename = files[choice]
            print("Selected file:", filename)
            if os.path.isfile(filename):
                return filename
            else:
                print("Invalid selection. Please select again.")
        except (IndexError, ValueError):
            print("Invalid input. Please enter a number from the list.")