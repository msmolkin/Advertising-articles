# build a static script to check if an article is AI or not

def detect_ai_words(article_text: str, words: list, possible_words: list) -> list:
    """
    Detect AI-related words in the article text.
    :param article_text: The article text to check.
    :param words: List of definite AI-related words.
    :param possible_words: List of possible AI-related words.
    :return: List of detected AI words.
    """
    words += possible_words
    detected_words = [root for root in words if root in article_text.lower()]
    return list(set(detected_words))

def detect_passive_voice(article_text: str) -> list:
    """
    Detect passive voice indicators in the article text.
    :param article_text: The article text to check.
    :return: List of detected passive voice words.
    """
    passive_voice_words = ["is", "are", "was", "were", "been", "being", "be", "by", "of"]
    detected_passive_voice_words = [word for word in passive_voice_words if word in article_text.lower()]
    return list(set(detected_passive_voice_words))

def print_detection_results(detected_words: list, detection_type: str) -> None:
    """
    Print the results of detection.
    :param detected_words: List of detected words.
    :param detection_type: Type of detection ("AI words" or "passive voice").
    """
    if detected_words:
        print(f"{len(detected_words)} {detection_type} detected:")
        for word in detected_words:
            print(f"- {word}")
    else:
        print(f"No {detection_type} detected.")

def print_is_ai(article_text: str) -> None:
    """
    Print whether the article is AI-generated or not.
    :param article_text: The article text to check.
    """
    ai_words = [
        "delv", "leverag", "labrynth", "paradigm", "elevat", "tapestry", "realm", "resonat",
        "multifacet", "beacon", "interplay", "paramount", "orchestr", "annal", "enigma",
        "indelible", "whims", "bespok", "nuanced", "dynamic", "crucial", "crux", "key", "junct", "craft", "landscap", "apparent", "utiliz"
    ]
    possible_ai_words = ["vital"]
    
    detected_ai_words = detect_ai_words(article_text, ai_words, possible_ai_words)
    detected_passive_voice_words = detect_passive_voice(article_text)
    
    print_detection_results(detected_ai_words, "AI words")
    print_detection_results(detected_passive_voice_words, "passive voice")

def test_print_is_ai():
    # print_is_ai("The tapestry of the article is crucial to the juncture of the story.") # tapestry, crucial, juncture
    # print_is_ai("The article is bespokely crafted") # bespoke, crafted
    # print_is_ai("The article is not AI-generated.") # no AI words detected
    # print_is_ai("The article is not AI-generated. It is a dynamic piece of writing.") # dynamic
    if input("Test on clipboard text? (y/n) ").lower() in "tyu":
        import pyperclip
        clipboard_text = pyperclip.paste()
        print_is_ai(clipboard_text)

if __name__ == "__main__":
    test_print_is_ai()