# build a static script to check if an article is AI or not

@staticmethod
def print_is_ai(article_text: str) -> None:
    """
    Print whether the article is AI-generated or not.
    :param article_text: The article text to check.
    """
    words = [
        "delv",  # delve
        "leverag",  # leverage
        "labrynth",
        "paradigm",
        "elevat",  # elevate
        "tapestry",
        "realm",
        "resonat",  # resonate
        "multifacet",  # multifaceted
        "beacon",
        "interplay",
        "paramount",
        "orchestr",  # orchestrate
        "annal",  # annals
        "enigma",
        "indelible",
        "whims",  # whimsical
        "bespok", # bespoke
        "nuanced",
        "dynamic",
        "crucial",
        "crux",
        "key",
        "junct",  # juncture
        "craft",
        "landscap",  # landscape
        "apparent", # becomes apparent
        # "of" # need to find a way to also detect things such as "the convergence of cryptocurrency and AI technology"
    ]

    detected_words = []
    for root in words:
        if root in article_text.lower():
            detected_words.append(root)

    detected_words = list(set(detected_words))  # remove duplicates

    if detected_words:
        for root in detected_words:
            print("AI word detected! Root word:", root)
            print(f"- {root}")
        print(f"There are {len(detected_words)} AI words detected.")
    else:
        print("No AI words detected.")

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