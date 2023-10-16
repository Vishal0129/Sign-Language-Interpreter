import { useState, useEffect, useRef } from "react";
import axios from "axios";
import urls from "../config";
import "./App.css";
import Sentence from "./components/Sentence";
const VideoRecorder = () => {
  const videoRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [videoBlob, setVideoBlob] = useState(null);
  const [sentenceList, setSentenceList] = useState([]);
  const [audioList, setAudioList] = useState([]);
  useEffect(() => {
    // Initialize the video stream when the component mounts
    if (videoRef.current) {
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then((stream) => {
          videoRef.current.srcObject = stream;
        })
        .catch((error) => {
          console.error("Error accessing webcam:", error);
        });
    }
  }, []);

  const startRecording = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        const recorder = new MediaRecorder(stream);
        const chunks = [];

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            chunks.push(event.data);
          }
        };

        recorder.onstop = () => {
          const videoBlob = new Blob(chunks, { type: "video/webm" });
          setVideoBlob(videoBlob);
        };

        recorder.start();
        setRecording(true);
        setMediaRecorder(recorder);
      })
      .catch((error) => {
        console.error("Error accessing webcam:", error);
      });
  };

  const stopRecording = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const getSentence = async (labels) => {
    console.log(typeof JSON.stringify(labels));
    await fetch(urls.wordsURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ labels: JSON.stringify(labels) }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        // return data;
        var result = data.sentence;
        setSentenceList([...sentenceList, result]);
        getAudio(result);
      })
      .catch((error) => {
        console.error("Error getting words from server:", error);
      });
  };

  const sendVideoToServer = async () => {
    if (videoBlob) {
      const formData = new FormData();
      formData.append("file", videoBlob, "recorded-video.webm");

      try {
        await axios
          .post(urls.videoURL, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            console.log(response);
            var labels = response.data.labels;
            labels = JSON.parse(labels);
            getSentence(labels);
          });
      } catch (error) {
        console.error("Error sending video to server:", error);
      }
    }
  };

  const getAudio = async (sentence) => {
    try {
      const response = await fetch(urls.audioURL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ labels: sentence }),
      });
      if (response.status === 200) {
        const data = await response.json();
        const audio = data.audio;
        setAudioList([...audioList, audio]);
        console.log(audio);
      } else {
        console.error("Error getting audio from server:", response.status);
      }
    } catch (error) {
      console.error("Error getting audio from server:", error);
    }
  };

  return (
    // <div className="video-recorder-container">
    //   <div className="left-panel">
    //     <header className="header">Video Recorder</header>
    //     <video ref={videoRef} autoPlay className="video-element" />
    //     <div className="button-container">
    //       {recording ? (
    //         <button onClick={stopRecording} className="button stop-button">
    //           Stop Recording
    //         </button>
    //       ) : (
    //         <button onClick={startRecording} className="button start-button">
    //           Start Recording
    //         </button>
    //       )}
    //       <button onClick={sendVideoToServer} className="button send-button">
    //         Send Video to Server
    //       </button>
    //     </div>
    //   </div>
    //   <div className="right-panel">
    //     <div className="sentence-list">
    //       <h2>Sentences:</h2>
    //       <ul>
    //         {sentenceList.map((sentence, index) => (
    //           <li key={index}>{sentence}</li>
    //         ))}
    //       </ul>
    //     </div>
    //   </div>
    // </div>

    <div className="video-recorder-container">
      <div className="left-panel">
        <header className="header">Video Recorder</header>
        <video ref={videoRef} autoPlay className="video-element" />
        <div className="button-container">
          {recording ? (
            <button onClick={stopRecording} className="button stop-button">
              Stop Recording
            </button>
          ) : (
            <button onClick={startRecording} className="button start-button">
              Start Recording
            </button>
          )}
          <button onClick={sendVideoToServer} className="button send-button">
            Send Video to Server
          </button>
        </div>
      </div>
      <div className="right-panel">
        <div className="sentence-list">
          <h2>Sentences:</h2>
          <ul>
            {sentenceList.map((sentence, index) => (
                <Sentence sentence={sentence} audio={audioList[index]} key={index} />
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default VideoRecorder;
