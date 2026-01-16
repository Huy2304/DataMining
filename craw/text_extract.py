import os
import re
import json
from langdetect import detect as lang_detect
from underthesea import ner, classify
import underthesea
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.chunk import RegexpParser
from typing import Any, List
from sparknlp.base import DocumentAssembler
from sparknlp.annotator import Tokenizer, StopWordsCleaner
from pyspark.ml import Pipeline
from sparknlp import start
import requests

# spark = start()

# documentAssembler = DocumentAssembler() \
#     .setInputCol("text") \
#     .setOutputCol("document")

# tokenizer = Tokenizer() \
#     .setInputCols(["document"]) \
#     .setOutputCol("token")

# stop_words = StopWordsCleaner.pretrained("stopwords_iso", "vi") \
#     .setInputCols(["token"]) \
#     .setOutputCol("cleanTokens")

# pipeline = Pipeline(stages=[documentAssembler, tokenizer, stop_words])

# example = spark.createDataFrame([["Bạn không tốt hơn tôi"]], ["text"])

# results = pipeline.fit(example).transform(example)
# results.select("token.result", "cleanTokens.result").show(truncate=False)

def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)

    try:
        nltk.data.find('corpora/omw')
    except LookupError:
        nltk.download('omw-1.4', quiet=True)

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)

download_nltk_data()

def load_my_stopwords(lang: str, path: str, filename: str) -> set:
    # https://raw.githubusercontent.com/stopwords-iso/stopwords-vi/master/stopwords-vi.txt
    # https://github.com/stopwords-iso/stopwords-iso
    try:
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, f'.\{path}\{filename}'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(data.get(lang, []))
    except Exception as e:
        print(f"load_my_stopwords: {e}")
        return set()

VI_STOPWORDS = load_my_stopwords('vi', '', 'stopwords-iso.json')
EN_STOPWORDS = set(stopwords.words('english')) | load_my_stopwords('en', '', 'stopwords-iso.json')

POS_TAG_MAP = {
    'N': 'NN',      # Noun
    'Nc': 'NN',     # Common noun
    'Nu': 'CD',     # Number
    'Np': 'NNP',    # Proper noun
    'V': 'VB',      # Verb
    'A': 'JJ',      # Adjective
    'P': 'PRP',     # Pronoun
    'R': 'RB',      # Adverb
    'L': 'DT',      # Determiner
    'M': 'CD',      # Measure word/Numeral
    'E': 'IN',      # Preposition
    'C': 'CC',      # Conjunction
    'I': 'UH',      # Interjection
    'T': 'TO',      # Particle
    'Y': 'UH',      # Abbreviation
    'Z': 'NN',      # Other
    'F': '.',       # Punctuation
    'X': 'FW',      # Foreign word
}

def chunk_sent(grammar: str, tagged: List[tuple[Any, str]]) -> List[str]:
    cp = RegexpParser(grammar)
    result = cp.parse(tagged)
    chunks = []
    for subtree in result.subtrees():
        if subtree.label() != 'S':  # Skip the root sentence node
            chunks.append(' '.join(word for word, tag in subtree.leaves()))
    return chunks

def word_tokenize(text: str, lang: str) -> List[str]:
    tokens = []
    pattern = r'\b[A-Z][\w]*(?:\s+[A-Z][\w]*)+'
    processed_text = re.sub(pattern, lambda m: m.group(0).replace(' ', '_'), text)
    if lang == 'en':
        tokenizer = RegexpTokenizer(r'\w+(?:-\w+)*')
        tokens = tokenizer.tokenize(processed_text)
    elif lang == 'vi':
        processed_text = re.sub(r'-', 'HYPHENPLACEHOLDER', processed_text)
        tokens = underthesea.word_tokenize(processed_text)

    tokens = [t.replace('_', ' ').replace('HYPHENPLACEHOLDER', '-') for t in tokens]
    return tokens

def sent_tokenize(text: str, lang: str) -> List[str]:
    tokens = []
    if lang == 'en':
        tokens = nltk.sent_tokenize(text)
    elif lang == 'vi':
        tokens = underthesea.sent_tokenize(text)

    return tokens

def remove_punctuation(tokens: List[str], lang: str) -> List[str]:
    if lang == 'en':
        return tokens
    elif lang == 'vi':
        tokens = [re.sub(r'[^\w\s-]', '', token) for token in tokens if re.sub(r'[^\w\s-]', '', token)]
        return tokens

def remove_stop_words(tokens: List[str], lang: str) -> List[str]:
    if lang == 'en':
        tokens = [word for word in tokens if word not in EN_STOPWORDS]
    elif lang == 'vi':
        tokens = [word for word in tokens if word not in VI_STOPWORDS]

    return tokens

def stem_words(tokens: List[str]) -> List[str]:
    ps = PorterStemmer()
    stemming_words = [ps.stem(word) for word in tokens]
    return stemming_words

def lemma_words(tokens: List[str], wordnet_pos: str='') -> List[str]:
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=wordnet_pos) for word in tokens]
    return lemmatized_words

if __name__ == "__main__":

    # text = "Biết sử dụng Framework Phaser là một lợi thế"
    # text = "Implement backend features using Python/Java and related frameworks."
    # text = "Triển khai tính năng ở phía backend sử dụng Python/Java và frameworks liên quan."
    # text = "Strong background in Computer Vision, Deep Learning, TensorFlow-2 and HTML5"
    text = "Nền tảng mạnh trong mảng Computer Vision, Deep Learning, TensorFlow-2 và HTML5"
    # text = "Analyze complex vision-related problems and propose AI-based approaches"

    detected_lang = lang_detect(text)
    tokens = word_tokenize(text, detected_lang)
    tokens = remove_punctuation(tokens, detected_lang)
    tokens = remove_stop_words(tokens, detected_lang)

    print(tokens)

    # pos_tags = nltk.pos_tag(lemma_words([w.lower() for w in tokens]))
    # pos_tags = underthesea.pos_tag(' '.join([w.lower() for w in tokens]))
    en_tokens = [w for w in tokens if w.isascii()]
    pos_tags = nltk.pos_tag(lemma_words(en_tokens, 'n'))
    for word, pos_tag in pos_tags:
        print(f"{word}: {pos_tag}")
        # print(classify(word))
    print(lemma_words(en_tokens, 'n'))
