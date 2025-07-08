import re

# Check if text is a sentence
def is_sentence(text):
    text = text.strip()
    sentence_endings = re.compile(r'[.!?]["\')\]]*\s+')
    matches = sentence_endings.findall(text)
    return len(matches) == 0