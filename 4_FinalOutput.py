import json
import logging
import spacy
def convert_to_spacy(JSON_FilePath):
    try:
        training_data = []
        lines=[]
        with open(JSON_FilePath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            try:
                data = json.loads(line)
                text = data['content']
                training_data.append(text)
            except json.decoder.JSONDecodeError:
                pass
        return training_data
    except Exception as e:
        logging.exception("Unable to process " + JSON_FilePath + "\n" + "error = " + str(e))
        return None
nlp=spacy.load('trainmodelf')
examples = convert_to_spacy("data.json")
zx=0
for text in examples:
        f=open("./Output/out"+str(zx)+".txt","w")
        doc_to_test=nlp(text)
        d={}
        zx+=1
        for ent in doc_to_test.ents:
            d[ent.label_]=[]
        for ent in doc_to_test.ents:
            d[ent.label_].append(ent.text)

        for i in set(d.keys()):

            f.write("\n\n")
            f.write(i +":"+"\n")
            for j in set(d[i]):
                f.write(j.replace('\n','')+"\n")
        f.close()
        print(d)
        print()