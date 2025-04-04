import spacy
import gender_guesser.detector as gender
import re

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Gender detector
detector = gender.Detector()

def replace_name_gender(text, new_name, new_gender):
    doc = nlp(text)
    modified_text = text

    for ent in doc.ents:
        if ent.label_ == "PERSON":  # Detecting names
            old_name = ent.text
            detected_gender = detector.get_gender(old_name)

            # Adjust pronouns based on detected gender
            pronoun_map = {
                "male": {"he": "she", "his": "her", "him": "her"},
                "female": {"she": "he", "her": "his", "her": "him"}
            }
            pronouns = pronoun_map.get(new_gender, {})

            # Replace name
            modified_text = re.sub(rf"\b{old_name}\b", new_name, modified_text)

            # Replace pronouns
            for old_pronoun, new_pronoun in pronouns.items():
                modified_text = re.sub(rf"\b{old_pronoun}\b", new_pronoun, modified_text, flags=re.IGNORECASE)

    return modified_text

# Example text
text = "Marco was watching TV. The TV went black. A loud voice said, 'This is just a test of the emergency system.' Then a loud sound came from the TV. Marco was scared! His mother said, 'Don't worry! They are just practicing. Come eat your breakfast.'"

# Convert to female Chinese American name
new_text = replace_name_gender(text, "Mei", "female")

print(new_text)
