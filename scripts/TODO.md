TODOs:
1. `file_reader.py`:
     • Improve accuracy when distinguishing numbered headings from regular text.
     • Add hyperlink support during the `read_docx` operation.
     • Implement an efficient method to automatically download DOC files when encountered.
     • Modify the program to correctly add newline characters around each heading in `read_docx`.
     • Develop a function that can convert RTF files to TXT.
     • Update `read_article` function to return a list of tuples instead of a single string.
2. `parse_google_doc.py`:
     • Expand the script to process more than just the text body of Google Docs.
     • Implement a method that removes images and stock photo credits from the parsed content.
3. `ask_gpt.py`:
     • Replace with `ask_llm.py` to allow it to use any high-powered LLM (GPT-4, PaLM 2, LLaMa), as the content returned doesn't matter too much
     • **Save the completed chat JSON**