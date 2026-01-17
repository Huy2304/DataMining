import os
from typing import List, Set
from text_extract import download_nltk_data, lang_detect, word_tokenize, remove_punctuation, remove_stop_words, lemma_words, strim_words, remove_empty_words
import nltk

def extract_raw_keys(text: str) -> dict[str, str]:
    detected_lang = lang_detect(text)
    tokens = word_tokenize(text, detected_lang)
    tokens = remove_punctuation(tokens, detected_lang)
    tokens = remove_stop_words(tokens, detected_lang)
    tokens = strim_words(tokens)
    tokens = remove_empty_words(tokens)

    en_tokens = [w for w in tokens if w.isascii()]
    lemmatized = lemma_words(en_tokens, 'n')
    pos_tags = nltk.pos_tag(lemmatized)
    pos_list = ["NN", "NNP"]
    words_to_save = {en_tokens[i]: v for i, (k, v) in enumerate(pos_tags) if v in pos_list}

    return words_to_save

def load_exist_keys(path: str, filename: str) -> set[str]:
    try:
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, f'.\{path}\{filename}'), 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except Exception as e:
        print(f"load_exist_keys: {e}")
        return set()

KEY_MAP = load_exist_keys("", "key_map.txt")
KEY_NOT_MAP = load_exist_keys("", "key_not_map.txt")

def save_key(key: str, pos: str, path: str, filename: str) -> bool:
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, path, filename)
    try:
        with open(filepath, 'r') as f:
            existing_keys = [line.strip().split(',')[0] for line in f]
        if key in existing_keys:
            return False
    except FileNotFoundError:
        return False
    with open(filepath, 'a') as f:
        f.write(key + ',' + pos + '\n')
        return True

def save_raw_to_key_map(data: dict[str, str]) -> bool:
    saved = False
    for key in data.keys():
        if key not in KEY_MAP and key not in KEY_NOT_MAP:
            if save_key(key, data[key], "", "key_map.txt"):
                saved = True
    return saved

if __name__ == "__main__":

    download_nltk_data()

    data = extract_raw_keys("Nền tảng mạnh trong mảng Computer Vision, Deep Learning, TensorFlow-2 và HTML5")
    save_raw_to_key_map(data)
