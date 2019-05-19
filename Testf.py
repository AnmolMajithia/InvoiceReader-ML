import hug
import spacy

nlp = spacy.load('trainmodelf')

@hug.post('/get_entities')
def get_entities(text):
    doc = nlp(text)
    entities = [{'text': ent.text, 'label': ent.label} for ent in doc.ents]
    return {'entities': entities}
