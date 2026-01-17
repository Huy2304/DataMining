import os

def clean_key_file(path: str, filename: str) -> bool:
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    seen = set()
    unique_lines = []
    for line in lines:
        line = line.strip()
        if ',' in line:
            key = line.split(',')[0].strip()
            if key and key[0].isalpha() and key not in seen:
                seen.add(key)
                unique_lines.append(line)
    # Sort by key then by pos in ascending alphabetical order
    unique_lines.sort(key=lambda x: (x.split(',')[0].strip(), x.split(',')[1].strip()))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_lines) + '\n')
    return True

if __name__ == "__main__":
    clean_key_file("craw", "key_map.txt")
    clean_key_file("craw", "key_not_map.txt")
