from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gramformer import Gramformer
from pydantic import BaseModel
import json
from gtts import gTTS
import pyttsx3
import base64

gf = Gramformer(models=1, use_gpu=False)
LANGUAGE = 'en'
off_tts = pyttsx3.init()
off_tts.setProperty('rate', 125)
off_tts.setProperty('volume', 1.0)
voices = off_tts.getProperty('voices')
off_tts.setProperty('voice', voices[1].id)

def get_words(words, threshold=10):
    unique_words = []
    count = 0  # Initialize count to 1 for the first character

    for i in range(1, len(words)):
        if words[i] == words[i - 1]:
            count += 1
        else:
            if count > threshold:
                unique_words.append(words[i - 1])
            count = 1  # Reset count for the new character

    # Check the last group
    if count > threshold:
        unique_words.append(words[-1])

    return unique_words

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    labels : str

@app.get('/')
def home():
    print("Hello World!")
    return {"message": "Hello World!"}

@app.post('/words', response_model=dict)
async def api_grammer(data : Data):
    labels = data.labels
    print(labels)
    words = json.loads(labels)
    unique_words = get_words(words)
    print(unique_words)
    sentence = gf.correct(' '.join(unique_words))
    print(list(sentence)[0])

    if len(unique_words) == 0 or len(unique_words) == 1:
        return {
            'sentence': ' '.join(unique_words)
            }
    return {
        'sentence': list(sentence)[0]
        }

@app.post('/audio', response_model=dict)
async def api_audio(data : Data):
    sentence = data.labels
    if len(sentence) == 0:
        return {
            'audio': ''
        }
    try:
        on_tts = gTTS(text=sentence, lang=LANGUAGE, slow=False)
        on_tts.save('audio.mp3')
    except:
        off_tts.save_to_file(sentence, 'audio.mp3')
        off_tts.runAndWait()

    with open('audio.mp3', 'rb') as f:
        audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes)

    return {
        'audio': audio_b64
    }