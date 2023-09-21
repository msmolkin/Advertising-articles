# TODO: 1. this is an attempt at turning this into a class
import os
from time import time, sleep
from docx import Document
from read_google_doc import read_google_doc

class FileDownloadError(Exception):
    """Raised when a file is not successfully downloaded from the server."""

    def __init__(self, message="Failed to download file from server"):
        self.message = message
        super().__init__(self.message)

class FileReader:
    def is_sparse(self, file_path):
        stat = os.stat(file_path)

        total_size = stat.st_size   # size of expected file
        actual_size = stat.st_blocks * stat.st_blksize # space allocated for file on disk

        return actual_size < total_size

    def download_file_with_timeout(self, filename, timeout=60):
        if self.is_sparse(filename):
            os.system("open -a OneDrive.app")
            print("Please wait while the file is downloaded from OneDrive.")
            
            start_time = time()
            while self.is_sparse(filename):
                if time() - start_time > timeout:
                    formatted = f"{timeout}-second" if timeout < 60 else f"{timeout // 60}-minute"
                    raise TimeoutError(f"File download exceeded {formatted} timeout.")
                sleep(1)
            print("File downloaded.")

    def read_docx(self, filename):
        doc = Document(filename)
        fullText = []
        
        for para in doc.paragraphs:
            if len(para.text) == 0 or para.text.isspace(): # ignore empty paragraphs
                continue
            else:
                heading_level = None

                # if paragraph is a heading, add a newline before and after it
                if para.style.name.startswith("Heading"):
                    try:
                        heading_level = int(para.style.name[-1])  # get the heading level
                    except ValueError:  # if it's not a numbered heading like "Heading 1"
                        pass
                    fullText.append(("\n" + para.text + "\n", heading_level)) 
                else:
                    fullText.append((para.text, heading_level))

        return fullText

    def check_and_download_file(self, filename):
        try:
            with open(filename, "rb") as f:
                f.read()
        except TimeoutError:    
            try:
                self.download_file_with_timeout(filename)
            except TimeoutError as e:
                print(e)
                print("Unable to access the text file. This may be due to OneDrive not being signed in, paused, or not connected to the internet. Please manually download the file and try again.")
                raise FileDownloadError("Downloading operation timed out.")

    @staticmethod
    def is_heading(paragraph):
        # Primitive test
        return 0 < len(paragraph) < 100
        # return paragraph.startswith("#")

    def read_article(self, filename: str = "original_article.txt", gdocs_url: str = None, gdocs_id: str = None):
        try:
            if gdocs_id is not None or gdocs_url is not None:
                return read_google_doc(gdocs_url, gdocs_id)
            
            self.check_and_download_file(filename)

            if filename.endswith(".txt") or os.path.isfile(filename) and not "." in filename:
                with open(filename, "r") as f:
                    a = f.readlines()
                    result = [(line.rstrip(), FileReader.is_heading(line.rstrip())) for idx, line in enumerate(a, start=1)]
                    print(result)  # [('hi', 1), ('hihi', 2), ('# hi', 3), ('### hello', 4)]
                    return f.read()
            elif filename.endswith(".rtf"):
                with open(filename, "r") as f:
                    return f.read()
            elif filename.endswith(".docx"): # Word document
                return self.read_docx(filename)
            elif filename.endswith(".doc"):
                raise ValueError("DOC file detected. Please convert to DOCX file.")
            else:
                raise ValueError("File type not supported.")
        

        except FileNotFoundError:
            print(f"{filename} does not exist or couldn't be found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def print_article(self, article_content):
        if isinstance(article_content, str):
            print(article_content)
        elif isinstance(article_content, list):
            for paragraph, heading_level in article_content:
                if heading_level is not None:
                    print(f"{'#' * heading_level} {paragraph.strip()}")
                else:
                    print(paragraph)
                print()
    
    def test_read_article(self, *args, **kwargs):
        filename = gdocs_url = gdocs_id = None
        if args:
            if isinstance(args[0], str):
                if args[0][-4:] in ['.txt', '.rtf', 'docx', '.doc']:
                    filename = args[0]
                elif args[0].startswith('http'): # assuming the gdocs_url starts with 'http'
                    gdocs_url = args[0]
                else:
                    gdocs_id = args[0] # treat as the gdocs_id if not a file or url

        filename = filename or kwargs.get("filename", "original_article.txt")
        gdocs_url = gdocs_url or kwargs.get("gdocs_url")
        gdocs_id = gdocs_id or kwargs.get("gdocs_id")   
        self.print_article(self.read_article(filename, gdocs_url, gdocs_id))

if __name__ == "__main__":
    file_reader = FileReader()
    """
    file_reader.test_read_article()
    file_reader.test_read_article([f for f in os.listdir() if f.startswith('v')][0]) # test with sparse file
    file_reader.test_read_article(filename="expat_us_tax.rtf") # test with RTF file
    file_reader.test_read_article(filename="AT-15-238 macroaxis.com JMC (A9648WC900) CAN.docx") # test with DOCX file
    file_reader.test_read_article(filename="original_article.doc") # test with DOC file # TODO: will download a DOC file directly to test this if this becomes a common file type
    file_reader.test_read_article(gdocs_url="https://docs.google.com/document/d/1oMWUwJ_eMIPxtR3sHPA4v67X0oUGqghRHrTa_2XgmMI/edit") # test with Google Docs URL
    file_reader.test_read_article(gdocs_id="1oMWUwJ_eMIPxtR3sHPA4v67X0oUGqghRHrTa_2XgmMI") # test with Google Docs ID
    """
    file_reader.test_read_article(filename="802B7D14 Lore.txt") # test with TXT file that exists
    #file_reader.test_read_article(filename="5729-T2131 - O22750-L107911-M119491 - macroaxis.com.docx")

# import os
# from time import time, sleep
# # from pyth.plugins.rtf15.reader import Rtf15Reader         # pip install pyth
# # from pyth.plugins.plaintext.writer import PlaintextWriter # pip install pyth
# from docx import Document                                   # pip install python-docx

# from read_google_doc import read_google_doc

# def is_sparse(file_path):
#     stat = os.stat(file_path)

#     total_size = stat.st_size   # size of expected file
#     actual_size = stat.st_blocks * stat.st_blksize # space allocated for file on disk

#     return actual_size < total_size

# def download_file_with_timeout(filename, timeout=60):
#     if is_sparse(filename):
#         os.system("open -a OneDrive.app")
#         print("Please wait while the file is downloaded from OneDrive.")
        
#         start_time = time()
#         while is_sparse(filename):
#             if time() - start_time > timeout:
#                 formatted = f"{timeout}-second" if timeout < 60 else f"{timeout // 60}-minute"
#                 raise TimeoutError(f"File download exceeded {formatted} timeout.")
#             sleep(1)
#         print("File downloaded.")

# def read_docx(filename):
#     doc = Document(filename)
#     fullText = []
    
#     for para in doc.paragraphs:
#         if len(para.text) == 0 or para.text.isspace(): # ignore empty paragraphs
#             continue
#         else:
#             heading_level = None

#             # if paragraph is a heading, add a newline before and after it
#             if para.style.name.startswith("Heading"):
#                 try:
#                     heading_level = int(para.style.name[-1])  # get the heading level
#                 except ValueError:  # if it's not a numbered heading like "Heading 1"
#                     pass
#                 fullText.append(("\n" + para.text + "\n", heading_level)) # TODO check if this adds a newline around each heading
#             else:
#                 fullText.append((para.text, heading_level))

#             # print(para.text, para.style.name, len(para.text), sep="\n", end="\n\n")

#     return fullText

# def read_article(filename: str = "original_article.txt", gdocs_url: str = None, gdocs_id: str = None):
#     """Read article from file or Google Docs and return text.
#     Try not to use this without a proper filename.
#     """
#     try:
#         # Google Docs
#         if gdocs_id is not None or gdocs_url is not None:
#             return read_google_doc(gdocs_url, gdocs_id)
#             # raise ValueError("Google Docs file detected. Please convert to TXT file or check whether read_google_doc works properly.")

#         # "Local" file
#         # If the file is sparse, open OneDrive and download the file from OneDrive on MacOS
#         try:
#             with open(filename, "rb") as f:
#                 f.read()
#         except TimeoutError:    
#             try:
#                 # download_file_with_timeout(filename, timeout=3) # for testing purposes
#                 download_file_with_timeout(filename)
#             except TimeoutError as e:
#                 print(e)
#                 print("Unable to access the text file. This may be due to OneDrive not being signed in, paused, or not connected to the internet. Please manually download the file and try again.")
#                 return "Downloading operation timed out."

#         if filename.endswith(".txt") or os.path.isfile(filename) and not "." in filename:
#             with open(filename, "r") as f:
#                 return f.read()
#         elif filename.endswith(".rtf"):
#             # TODO: convert RTF to TXT
#             # with open(filename, "r") as f:
#             #     doc = Rtf15Reader.read(f)
#             #     return PlaintextWriter.write(doc).getvalue()

#             # raise ValueError("RTF file detected. Please convert to TXT file.")
#             with open(filename, "r") as f:
#                 return f.read()
#         elif filename.endswith(".docx"): # Word document
#             return read_docx(filename)
#         elif filename.endswith(".doc"):
#             raise ValueError("DOC file detected. Please convert to DOCX file.")
#         else:
#             raise ValueError("File type not supported.")
    

#     except FileNotFoundError:
#         print(f"{filename} does not exist or couldn't be found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def test_read_article(*args, **kwargs):
#     filename = gdocs_url = gdocs_id = None
#     if args:
#         if isinstance(args[0], str):
#             if args[0][-4:] in ['.txt', '.rtf', 'docx', '.doc']:
#                 filename = args[0]
#             elif args[0].startswith('http'): # assuming the gdocs_url starts with 'http'
#                 gdocs_url = args[0]
#             else:
#                 gdocs_id = args[0] # treat as the gdocs_id if not a file or url

#     filename = filename or kwargs.get("filename", "original_article.txt")
#     gdocs_url = gdocs_url or kwargs.get("gdocs_url")
#     gdocs_id = gdocs_id or kwargs.get("gdocs_id")   
#     print(read_article(filename, gdocs_url, gdocs_id))
#     # read_article(kwargs.get("filename", "original_article.txt"), kwargs.get("gdocs_url", None), kwargs.get("gdocs_id", None))

# if __name__ == "__main__":
#     """
#     test_read_article()
#     test_read_article([f for f in os.listdir() if f.startswith('v')][0]) # test with sparse file
#     test_read_article(filename="expat_us_tax.rtf") # test with RTF file
#     test_read_article(filename="AT-15-238 macroaxis.com JMC (A9648WC900) CAN.docx") # test with DOCX file
#     test_read_article(filename="original_article.doc") # test with DOC file # TODO: will download a DOC file directly to test this if this becomes a common file type
#     test_read_article(gdocs_url="https://docs.google.com/document/d/1oMWUwJ_eMIPxtR3sHPA4v67X0oUGqghRHrTa_2XgmMI/edit") # test with Google Docs URL
#     test_read_article(gdocs_id="1oMWUwJ_eMIPxtR3sHPA4v67X0oUGqghRHrTa_2XgmMI") # test with Google Docs ID
#     test_read_article(filename="802B7D14 Lore.txt") # test with TXT file that exists
#     """
#     test_read_article(filename="5729-T2131 - O22750-L107911-M119491 - macroaxis.com.docx")

# TODO 2: I may have just mesed things up. I just made it so that the read_article function returns a list of tuples instead of a string.