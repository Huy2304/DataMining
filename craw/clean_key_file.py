import os
from text_extract import lemma_words

def clean_key_file(path: str, filename: str) -> bool:
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    groups = {}
    for line in lines:
        if ',' in line:
            parts = line.split(',')
            if len(parts) >= 2:
                key = parts[0].strip()
                pos = parts[1].strip()
                if key and key[0].isalpha():
                    if pos not in groups:
                        groups[pos] = []
                    groups[pos].append(key)
    unique_lines = []
    seen_lemmas = set()
    for pos, keys in groups.items():
        if pos.startswith('N'):
            wordnet_pos = 'n'
        elif pos.startswith('V'):
            wordnet_pos = 'v'
        elif pos.startswith('J'):
            wordnet_pos = 'a'
        elif pos.startswith('R'):
            wordnet_pos = 'r'
        else:
            wordnet_pos = 'n'
        lemmas = lemma_words(keys, wordnet_pos)
        for lemma in lemmas:
            if lemma.lower() not in seen_lemmas:
                seen_lemmas.add(lemma.lower())
                unique_lines.append(f"{lemma},{pos}")
    # Sort by lemma then by pos in ascending alphabetical order
    unique_lines.sort(key=lambda x: (x.split(',')[0].strip(), x.split(',')[1].strip()))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_lines) + '\n')
    return True

if __name__ == "__main__":
    clean_key_file("craw", "key_map.txt")
    clean_key_file("craw", "key_not_map.txt")
