class GoogleDocParser:
    """
    Parse Google Doc JSON into HTML/TXT/Markdown
    This is a very basic parser that only parses the text and ignores images, tables, etc. Designed to process Google Doc for use with GPT.
    TODO: For now, it only gets the text from the body.
    """

    def __init__(self, doc_content):
        self.doc_content = doc_content
        self.stock_photo_websites = [
            "unsplash.com",
            "shutterstock.com",
            "istockphoto.com",
            "gettyimages.com",
            "pexels.com",
            "pixabay.com",
            "depositphotos.com",
            "adobe.com/stock",
            "dreamstime.com",
            "bigstockphoto.com",
        ]

    def is_useless_link(self, content):
        for website in self.stock_photo_websites:
            if website.lower() in content.lower():
                return True
        return False

    def parse(self):
        # TODO: for now, it just removes the images and stock photo credits and returns the text
        parsed_content = ""

        for item in self.doc_content["body"]["content"]:
            if "paragraph" in item:
                paragraph_elements = item["paragraph"]["elements"]
                for element in paragraph_elements:
                    if "textRun" in element:
                        content = element["textRun"]["content"]
                        if not self.is_useless_link(content):
                            parsed_content += content

                    # Remove inlineObjectElement (images) since they are not needed
                    # Uncomment the following lines if you want to keep the images
                    # elif "inlineObjectElement" in element:
                    #     inline_object_id = element["inlineObjectElement"]["inlineObjectId"]
                    #     inline_object = doc_content["inlineObjects"][inline_object_id]
                    #     image_url = inline_object["inlineObjectProperties"]["embeddedObject"]["imageProperties"]["contentUri"]
                    #     parsed_content += f'<img src="{image_url}" />\n'

        return parsed_content

if __name__ == "__main__":
    import os, json
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "articles", "gdoc.json")
    with open(json_file_path, "r") as f:
        doc_content = json.load(f)

    parser = GoogleDocParser(doc_content)
    parsed_content = parser.parse()
    print(parsed_content)