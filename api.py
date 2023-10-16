from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from predict import Predict
import base64
import numpy as np
import cv2
import tempfile
import shutil
import json 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    frameData: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/frame")
async def upload_frame(data: Data):
    try:
        # print(data.frameData[:20])

        # # Decode the base64 data to binary image data
        base64img = data.frameData
        base64img = base64img.replace("data:image/jpeg;base64,", "")
        binary_image_data = base64.b64decode(base64img)

        # # Convert binary image data to a NumPy array
        nparr = np.frombuffer(binary_image_data, np.uint8)
        
        # # Read the image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # cv2.imwrite("test.jpg", image)
        # Pass the processed image to your model function
        label_name = pred.get_hand_gesture_label(image)
        print(label_name)


        return JSONResponse(content={"message": "Frame received and processed successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/video")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Create a temporary directory to store video frames
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = f"{temp_dir}/input_video.webm"

            # Save the uploaded video to a temporary file
            with open(temp_file_path, "wb") as video_file:
                shutil.copyfileobj(file.file, video_file)

            # Open the video file using OpenCV
            video_capture = cv2.VideoCapture(temp_file_path)

            # Read and process each frame
            frame_count = 0
            labels = []
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                # Process the frame here (you can use your model)
                label_name = pred.get_hand_gesture_label(frame)
                labels.append(label_name)
                # print("Processing frame", frame_count)

                frame_count += 1
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    print(labels)
    return JSONResponse(content={"labels":json.dumps(labels)}, status_code=200)





if __name__ == "__main__":
    import uvicorn
    pred = Predict()
    uvicorn.run(app, host="0.0.0.0", port=8000 )
