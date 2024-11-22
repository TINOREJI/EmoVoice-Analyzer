import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './App.css'; // Ensure you have your CSS file for styling

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setAudioFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!audioFile) return;

    const formData = new FormData();
    formData.append('audio', audioFile);

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Pass emotion to the result page
      navigate('/result', { state: { emotion: response.data.emotion } });
    } catch (error) {
      console.error('Error during prediction:', error);
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Emotion Detection from Audio</h1>
      <img src="/Images/2634805.jpg" alt="Emotion Detection" className="image-above-file" />
      <input
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
        className="file-input"
      />
      <button onClick={handleSubmit} className="submit-button">Predict Emotion</button>

      {loading && <div className="loader"></div>} {/* Loading animation */}
    </div>
  );
}

export default App;
