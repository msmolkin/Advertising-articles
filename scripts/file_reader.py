import os
from time import time, sleep
from docx import Document
from read_google_doc import read_google_doc
from parse_google_doc import GoogleDocParser
from read_bazoom_article import read_finalarticle_article

class FileDownloadError(Exception):
    """Raised when a file is not successfully downloaded from the server."""

    def __init__(self, message="Failed to download file from server"):
        self.message = message
        super().__init__(self.message)

class FileReader:
    @staticmethod
    def is_sparse(file_path):
        stat = os.stat(file_path)

        total_size = stat.st_size   # size of expected file
        actual_size = stat.st_blocks * stat.st_blksize # space allocated for file on disk

        return actual_size < total_size

    @staticmethod
    def download_file_with_timeout(filename, timeout=60):
        if FileReader.is_sparse(filename):
            os.system("open -a OneDrive.app")
            print("Please wait while the file is downloaded from OneDrive.")
            
            start_time = time()
            while FileReader.is_sparse(filename):
                if time() - start_time > timeout:
                    formatted = f"{timeout}-second" if timeout < 60 else f"{timeout // 60}-minute"
                    raise TimeoutError(f"File download exceeded {formatted} timeout.")
                sleep(1)
            print("File downloaded.")

    # Removing additional time from going through the runs
    @staticmethod
    def read_docx(filename):
        # TODO: add support for hyperlinks, or at least notify the user that hyperlinks were in the paragraph
        doc = Document(filename)
        fullText = []

        for para in doc.paragraphs:
            if len(para.text) == 0 or para.text.isspace():  # ignore empty paragraphs
                continue
            else:
                heading_level = None
                paragraph_text = ""

                # Check if the paragraph is a heading
                if para.style.name.startswith("Heading"):
                    try:
                        heading_level = int(para.style.name[-1])  # get the heading level
                    except ValueError:  # if it's not a numbered heading like "Heading 1"
                        pass

                paragraph_text = ""
                # if heading_level is not None:
                #     paragraph_text += "\n" # add a newline before headings
                paragraph_text += para.text

                fullText.append((paragraph_text, heading_level))

        return fullText

    @staticmethod
    def check_and_download_file(filename):
        try:
            with open(filename, "rb") as f:
                f.read()
        except TimeoutError:    
            try:
                FileReader.download_file_with_timeout(filename)
            except TimeoutError as e:
                print(e)
                print("Unable to access the text file. This may be due to OneDrive not being signed in, paused, or not connected to the internet. Please manually download the file and try again.")
                raise FileDownloadError("Downloading operation timed out.")

    @staticmethod
    def heading_of(paragraph, heading_type=2):
        # Primitive test
        return heading_type if 0 < len(paragraph) < 100 else None # Markdown version: return paragraph.startswith("#")

    @staticmethod
    def read_text_file(filename):
        with open(filename, "r") as f:
            lines = [line.rstrip() for line in f.readlines() if not line.isspace()]
            formatted_article = [(lines[0], FileReader.heading_of(lines[0].rstrip(), heading_type=1))] # add the title
            formatted_article += [(line, FileReader.heading_of(line.rstrip())) for line in lines[1:]] # add the rest of the article
            return formatted_article
            # return f.read()
    
    @staticmethod
    def read_article(filename: str = "original_article.txt", gdocs_url: str = None, gdocs_id: str = None, final_article_url: str = None):
        try:
            if gdocs_id is not None or gdocs_url is not None:
                return read_google_doc(gdocs_url, gdocs_id)
            elif final_article_url is not None:
                return read_finalarticle_article(final_article_url)
            else:
                FileReader.check_and_download_file(filename)

            if filename.endswith(".txt") or os.path.isfile(filename) and not "." in filename:
                return FileReader.read_text_file(filename)
            elif filename.endswith(".rtf"):
                with open(filename, "r") as f:
                    return f.read()
            elif filename.endswith(".docx"): # Word document
                return FileReader.read_docx(filename)
            elif filename.endswith(".doc"):
                raise ValueError("DOC file detected. Please convert to DOCX file.")
            else:
                raise ValueError("File type not supported.")
        

        except FileNotFoundError:
            print(f"{filename} does not exist or couldn't be found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def parse_article(article_content):
        # if the article content is just a string, return it
        if isinstance(article_content, str):
            return article_content
        elif isinstance(article_content, list) and isinstance(article_content[0], tuple):
            parsed_content = ""
            for paragraph, heading_level in article_content:
                if heading_level is not None:
                    parsed_content += f"\n{'#' * heading_level} {paragraph.strip()}\n\n"
                else:
                    parsed_content += f"{paragraph}\n\n"
            return parsed_content
        # if the article content is a json object, parse it with GoogleDocParser
        elif isinstance(article_content, dict):
            parser = GoogleDocParser(article_content)
            return parser.parse()
    
    @staticmethod
    def print_article(article_content):
        # if I haven't processed the article using tuples, just print it
        if isinstance(article_content, str):
            print(article_content)
        elif isinstance(article_content, list):
            for paragraph, heading_level in article_content:
                if heading_level is not None:
                    print(f"\n{'#' * heading_level} {paragraph.strip()}")
                else:
                    print(paragraph)
                print()
    
    @staticmethod
    def test_read_article(*args, **kwargs):
        filename = gdocs_url = gdocs_id = final_article_url = None
        if args:
            if isinstance(args[0], str):
                if args[0][-4:] in [".txt", ".rtf", "docx", ".doc"] or "." not in args[0]:
                    filename = args[0]
                elif args[0].startswith("http"): # assuming the gdocs_url starts with "http"
                    gdocs_url = args[0]
                else:
                    gdocs_id = args[0] # treat as the gdocs_id if not a file or url

        filename = filename or kwargs.get("filename", "original_article.txt")
        gdocs_url = gdocs_url or kwargs.get("gdocs_url")
        gdocs_id = gdocs_id or kwargs.get("gdocs_id")
        final_article_url = final_article_url or kwargs.get("final_article_url")
        FileReader.print_article(FileReader.read_article(filename, gdocs_url, gdocs_id, final_article_url))

if __name__ == "__main__":
    os.chdir("articles")
    if os.path.isfile(".DS_Store"):
        os.remove(".DS_Store")
    file_reader = FileReader()
    """
    file_reader.test_read_article()
    file_reader.test_read_article(filename="802B7D14 Lore.txt") # test with TXT file that exists
    file_reader.test_read_article([f for f in os.listdir() if f.startswith("v")][0]) # test with sparse file
    file_reader.test_read_article(filename="expat_us_tax.rtf") # test with RTF file
    file_reader.test_read_article(filename="filename.docx") # test with DOCX file
    file_reader.test_read_article(filename="original_article.doc") # test with DOC file # TODO: will download a DOC file directly to test this if this becomes a common file type
    
    file_reader.test_read_article(gdocs_id="article_id") # test with Google Docs ID
    """
    # file_reader.test_read_article(gdocs_url="https://docs.google.com/document/d/article_id/edit") # test with Google Docs URL
    #file_reader.test_read_article(filename="filename.docx")
    file_reader.test_read_article(final_article_url="https://final-article.com/article_id_here/edit")