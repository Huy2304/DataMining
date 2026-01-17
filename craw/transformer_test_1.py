# Library
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the pre-trained model and tokenizer
model_name = "ihk/skillner"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Create a NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Sample text
text = "I have experience in Python, JavaScript, and cloud technologies like AWS and Azure."

# Run the pipeline on the text
ner_results = ner_pipeline(text)

# Filter and display only SKILL entities with high confidence
for entity in ner_results:
    if entity['entity_group'] == 'SKILL' and entity['score'] > 0.5:
        # Clean the word by removing trailing punctuation
        word = entity['word'].rstrip(',. ')
        print(f"Skill: {word}, Score: {entity['score']:.4f}")
