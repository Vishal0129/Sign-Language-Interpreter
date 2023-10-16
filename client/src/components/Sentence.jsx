import { useRef } from "react";
import PropTypes from "prop-types";
import "./Sentence.css";
const Sentence = ({ sentence, audio }) => {
  const audioRef = useRef(null);
  const playAudio = () => {
    if (audio) {
      const audioBlob = new Blob([audio], { type: "audio/mpeg" });
      const audioUrl = URL.createObjectURL(audioBlob);
      audioRef.current.src = audioUrl;
      
      // Create a data URL from the base64 audio data
      const dataUrl = `data:audio/mpeg;base64,${audio}`;
      audioRef.current.src = dataUrl;
      audioRef.current.play();
    }
  };
  

  return (
    // <div>
    //   <p>{sentence}</p>
    //   <button onClick={playAudio}>Play Audio</button>
    //   {/* Add controls to display audio controls */}
    //   <audio ref={audioRef} controls style={{ display: "none" }}></audio>
    // </div>
    <div className="sentence-container">
      <p className="sentence-text">{sentence}</p>
      <button className="play-audio-button" onClick={playAudio}>
        Play Audio
      </button>
      {/* Add controls to display audio player */}
      <audio ref={audioRef} controls className="visible" style={{display:"none"}}></audio>
    </div>
  );
};

Sentence.propTypes = {
  sentence: PropTypes.string.isRequired,
  audio: PropTypes.string, // PropTypes for a base64-encoded audio string
};

export default Sentence;
