from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import langid
import torch

# Load model and tokenizer once
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Get supported language codes
supported_languages = tokenizer.lang_code_to_id.keys()

async def translate_to_english(text: str) -> str:
    # Detect the source language
    detected_lang = langid.classify(text)[0]

    # If already in English, return as is
    if detected_lang == "en":
        return text

    # If not supported by M2M100
    if detected_lang not in supported_languages:
        return f"[Error] Detected language '{detected_lang}' not supported by M2M100."

    # Tokenize and translate
    tokenizer.src_lang = detected_lang
    encoded = tokenizer(text, return_tensors="pt")

    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.get_lang_id("en")
    )
    translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated
