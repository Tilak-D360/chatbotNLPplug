#@title Get user query { display-mode: 'form' }
import json
import numpy as np
from dialogflowUtils import *
from utils import *

fallback = [
    'I didn\'t get that. Can you say it again?',
    'I missed what you said. What was that?',
    'Sorry, could you say that again?',
    'Sorry, can you say that again?',
    'Can you say that again?',
    'Sorry, I didn\'t get that. Can you rephrase?',
    'Sorry, what was that?',
    'I didn\'t get that. Can you repeat?'
]

def query(text = None, lang = 'en-US', debug = False):
    try:
        if text is None:
            text = input("Enter a query to be processed:\n")
        
        response = json.loads(post(text, lang))
        print('-'*10, 'DialogFlow', '-'*10 ,'\n',response['queryResult']['parameters'],'-'*10, 'DialogFlow', '-'*10 ,'\n')
        return workerFun(response)
    except:
        print('-'*60)
        print(np.random.choice(fallback))\

if __name__ == "__main__":
    text = [
        'color i-j',
        'mes1 2-20'
    ]
    for q in text:    
        res = query(q, 'en-US', True)
        print(workerFun(res))
