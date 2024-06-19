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
            choice = input("Select the file by entering its number: ")
            if choice.lower() == "q":
                print("Exiting program.")
                exit()
            elif choice.isdigit():
                choice = int(choice) - 1
                filename = files[choice]
            else:
                matching_files = [f for f in files if choice.lower() in f.lower()]  # could be startswith, but that's less flexible
                if len(matching_files) == 1:
                    filename = matching_files[0]
                elif len(matching_files) > 1:
                    print("Multiple files match the input. Please select one of the following:")
                    for idx, file in enumerate(matching_files):
                        print(f"{idx + 1}. {file}")
                    choice = input("Select the file by entering its number: ")
                    if choice.isdigit():
                        choice = int(choice) - 1
                        filename = matching_files[choice]
                    else:
                        print("Invalid input. Please enter a number from the list.")
                        continue
                else:
                    print("No files match the input. Please try again.")
                    continue
            print("Selected file:", filename)
            if os.path.isfile(filename):
                return filename
            else:
                print("Invalid selection. Please select again.")
        except (IndexError, ValueError):
            print("Invalid input. Please enter a number from the list.")