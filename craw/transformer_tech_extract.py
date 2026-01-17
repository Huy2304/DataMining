from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1, hypothesis_template="In the context of computer programming and software development technical skills, this is {}.")

# sum n label = 1. Increasing label must decrease threshold and computer resource
LABELS = [
    "computer_technology",
    "computer_programming",
    "artificial_intelligence",
    "data_science",
    "web_development",
    "cloud_computing",
    "database",
    "software_development",

    # "devops",
    # "machine_learning",
    # "version_control",
    # "security",
    "software_development_framework",
    "software_architecture",
    # "big_data",
    # "microservices",
    # "robotics",
    # "ai_assistant",
    # "image_recognition",
    # "speech_recognition",

    "operating_system",
    "process_automation",
    "mobile_app_development",
    "software_testing",
    "it_infrastructure",
    "computer_networking",
    "computer_tool",
    "computer_platform",
    "internet_of_things",
    "cyber_security",
    "system_monitoring",
    "embedded_systems",
    "system_integration",

    "other"
]

LABEL_TO_REMOVE = [
    "other"
]

def extract_tech_by_capability(phrase: str) -> str:
    orig_phrase = phrase
    orig_tokens = orig_phrase.split()
    # Process orig_tokens: uppercase if no hyphen, else concat without upper
    processed_orig_tokens = []
    for token in orig_tokens:
        if '-' in token:
            processed_orig_tokens.append(token.replace('-', ''))
        else:
            processed_orig_tokens.append(token.upper())
    processed_orig_phrase = ''
    for token in orig_tokens:
        if '-' in token:
            processed_orig_phrase += token.replace('-', '')
        else:
            processed_orig_phrase += token.upper()
        processed_orig_phrase += ' '  # since split removes spaces, but for whole phrase, add space
    processed_orig_phrase = processed_orig_phrase.strip()
    orig_map = {processed: orig for processed, orig in zip(processed_orig_tokens, orig_tokens)}
    orig_map[processed_orig_phrase] = orig_phrase

    # Process phrase
    tokens = []
    for token in orig_tokens:
        if '-' in token:
            tokens.append(token.replace('-', ''))
        else:
            tokens.append(token.upper())
    phrase = processed_orig_phrase
    candidates = list(set(tokens + [phrase]))

    best_result = ""
    best_score = 0.0
    best_label = ""
    orig_best = ""

    for candidate in candidates:
        try:
            result = classifier(candidate, candidate_labels=LABELS)

            top_label = result["labels"][0]
            top_score = result["scores"][0]

            if top_label not in LABEL_TO_REMOVE and top_score > 0.1 and top_score > best_score:
                best_result = candidate
                best_score = top_score
                best_label = top_label
                orig_best = orig_map.get(candidate, candidate)
        except Exception as e:
            print(f"Error classifying {candidate}: {e}")
            continue

    if not best_result:
        print(f"{orig_phrase} ==> {candidates}")
    else:
        print(f"{orig_phrase} ==> {candidates} ==> {orig_best}: {best_score} | {best_label}")
        # print(f"{orig_phrase} ==> {candidates} ==> {best_result}: {best_score} | {best_label}")

    return orig_best

# Test the function
if __name__ == "__main__":
    phrase = "Jenkins CI"
    # phrase = "AWS Certification"
    # phrase = "Ubuntu Cli"
    result = extract_tech_by_capability(phrase)
