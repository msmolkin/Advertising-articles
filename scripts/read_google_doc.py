# -*- coding: utf-8 -*-
# How to read a Google Docs file using Python
# Haven't tested this yet

import os.path
import pickle

from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

def read_google_doc(doc_url, doc_id = None): # if it's a word doc, download it instead of treating it as a Google Docs file
    if doc_url is not None:
        doc_id = doc_url.split("/")[5] # using -1 might not work because of /edit or /view that is usually added
    creds = None
    auth_path = Path(__file__).resolve().parent.parent / "auth"
    token_file = "token.pickle"
    token_path = os.path.join(auth_path, token_file)
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(auth_path, "credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("docs", "v1", credentials=creds)

    document = service.documents().get(documentId=doc_id).execute()

    print("The document title is: {}".format(document["title"]))

    # if the document is a Google Docs file, the full text is in the body.content field.
    document["body"]["content"]
    # if the document in Google Docs is a Word file, the full text is in the body.content field, but it's a list of paragraphs.
    # document["body"]["content"][0]["paragraph"]["elements"][0]["textRun"]["content"] # figure out how to parse the doc. see gdoc.json
    # or you may need to download the Word doc first and then read it with the docx library

    return document

def test_read_google_doc(doc_url):
    import json
    document = read_google_doc(doc_url)
    # Save the document as a JSON file
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "articles", "gdoc.json")
    with open(json_file_path, "w") as f:
        f.write(json.dumps(document, indent=4))

# Usage:
if __name__ == "__main__":
    # read_google_doc(doc_url="https://docs.google.com/document/d/1oMWUwJ_eMIPxtR3sHPA4v67X0oUGqghRHrTa_2XgmMI/edit")
    # read_google_doc("https://docs.google.com/document/d/1WXU2ParZc_kWUAweTTK7-7TNWrfoINkfFaGcweU1CAY/edit")
    test_read_google_doc("https://docs.google.com/document/d/1WXU2ParZc_kWUAweTTK7-7TNWrfoINkfFaGcweU1CAY/edit")

# This script will open a new window to authenticate your Google account that has access to the Google Docs when you run the script for the first time.