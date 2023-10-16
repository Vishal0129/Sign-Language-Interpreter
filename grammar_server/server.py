from gramformer import Gramformer
gf = Gramformer(models=1, use_gpu=False)

def get_words(words, threshold):
    unique_words = []
    count = 1  # Initialize count to 1 for the first character

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

# words = ['This', 'This', 'This', 'This', 'This', 'This', 'This', 'This', 'This', 'This', 'This', 'b', 'b', 'our', 'our', 'our', 'our', 'our', 'our', 'our', 'our', 'project', 'project', 'project', 'project', 'project', 'project']
# threshold = 4
# unique_words = get_words(words, threshold)
# print(unique_words)
# sentence = gf.correct(' '.join(unique_words))
# print(list(sentence)[0])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS configuration
origins = [
    "http://192.168.0.101:5173",  # Replace with the actual origin of your React app
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    words: str
    threshold: int

@app.get('/', response_model=dict)
def home():
    return {"message": "Hello World!"}

@app.post('/words')
async def api_grammer(
    labels: str,
    # threshold: int,
):
    print(labels)
    # print(labels, threshold)
    # words = json.loads(data.words)
    # threshold = data.threshold
    # print(words, threshold)
    # unique_words = get_words(words, threshold)
    # sentence = gf.correct(' '.join(unique_words))
    # print(sentence)
    # return {'sentence': list(sentence)[0]}
    return {'sentence': "Hello World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.107", port=8000)
