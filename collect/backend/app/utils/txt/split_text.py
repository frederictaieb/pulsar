import re

# Split text in sentences
def split_text(text):
    text = text.strip().replace("...", "§ELLIPSIS§")
    chunks = re.split(r'(?<=[.!?])\s+', text)
    sentences = [c.replace("§ELLIPSIS§", "...").strip() for c in chunks if c.strip()]
    return sentences


