from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os

import logging
logging.basicConfig(filename='fastapi.log', level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
)

# Load the dictionary from the JSON file
DICTIONARY_FILE = 'dictionary.json'

def load_dictionary():
    if not os.path.exists(DICTIONARY_FILE):
        response = requests.get('https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/refs/heads/master/dictionary.json')
        with open(DICTIONARY_FILE,'w') as f:
            f.write(json.dumps(response.json()))
        
    with open(DICTIONARY_FILE, 'r') as file:
        return json.load(file)

# Load the dictionary into memory when the server starts
dictionary = load_dictionary()

@app.get("/lookup/{word}")
async def lookup_word(word: str):
    """Lookup a word in the dictionary."""
    definition = dictionary.get(word)
    if definition:
        return JSONResponse(content={word: definition})
    else:
        raise HTTPException(status_code=404, detail="Word not found")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Dictionary API! Use /lookup/{word} to get definitions."}
