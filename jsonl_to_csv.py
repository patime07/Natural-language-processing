import json
from camel_tools.tokenizers.word import simple_word_tokenize
import pandas as pd
with open ('/content/gdrive/MyDrive/annotated_corpus/batch4.jsonl', 'r') as f: 
  lines = f.readlines()

#converting annotated text from doccano in JSONL format to CoNLL

#create dataframe
conll = pd.DataFrame()
conll['token'] = []
conll['tag'] = []

#for each text in JSONL
for line in lines: 
  data = json.loads(line)  
  text = data['text']
  labels = data['label']
  #annotate tokens before first NE with 'O'
  if labels[0][0] != 0: 
    tokens = simple_word_tokenize(text[0:labels[0][0]])
    df = pd.DataFrame({'token': tokens, 'tag': ['O']*len(tokens)})
    conll = conll.append(df, ignore_index = True)
  #Annotate each entity and the non-entities after it
  for i in range (1, len(labels)): 
    #delimite entity
    ent_beg = labels[i][0]
    ent_end = labels[i][1]
    ent = text[ent_beg:ent_end]
    tag = labels[i][2]
    ent_tokens = simple_word_tokenize(ent)
    print(ent)
    #annotate first token in entity
    try: 
      conll = conll.append({'token': ent_tokens[0], 'tag': 'B-'+tag}, ignore_index = True)
    except: 
      pass
    #entity remaining tokens in entity 
    df = pd.DataFrame({'token': ent_tokens[1:len(ent_tokens)], 'tag': ['I-' + tag]*(len(ent_tokens)-1)})
    conll = conll.append(df, ignore_index = True)
    #check if this is the last entity
    if i != len(labels) - 1: 
      tokens = simple_word_tokenize(text[ent_end:labels[i+1][0]])
    else: 
      tokens = simple_word_tokenize(text[ent_end: len(text)])
    #annotate non-entity with 'O'
    df = pd.DataFrame({'token': tokens, 'tag': ['O']*len(tokens)})
    conll = conll.append(df, ignore_index = True)
