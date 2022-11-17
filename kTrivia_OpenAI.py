from phBot import *
from threading import Timer
import phBotChat
import QtBind
import io
import os
import json
import requests
import struct
import re

pName = 'kTriviaOpenAI'
pVersion = '1.1'
pUrl = ''
pAuthor = "Katzuya"

#Globals
openAItoken = 'YOUR_API_TOKEN'
botName = '[BOT]Event'

def pluginLogger(msg):
    log('[' + pName + '] ' + msg)
    return

def askQuestion(q):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+ openAItoken +"",
    }
    data = '{ "model": "text-davinci-002", "prompt": "Q: '+ q + '", "temperature": 0, "max_tokens": 60, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0 }'
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=data)
    json_data = response.json()
    for element in json_data['choices']:
        answer = element['text']
    new_answer=answer.replace('A: ','')
    final_answer=re.sub(r'\n\s*\n', '\n', new_answer, flags=re.MULTILINE)
    return final_answer

def answerQuestion(msg):
    if "Trivia" in msg :
        return
    elif "is the winner of this Trivia round!" in msg:
        return
    elif "You are the winner of this trivia round." in msg:    
        return       
    else :    
        answerFinal = askQuestion(msg)
        pluginLogger('AI has found answer. ' + answerFinal)
        phBotChat.Private(botName, answerFinal)   
    return                      

def handle_chat(t, player, msg):  
    if t == 6:
        if player == botName:
            answerQuestion(msg)
        return   
    return


# Plugin loaded
log("Plugin: "+pName+" v"+pVersion+" successfully loaded")
