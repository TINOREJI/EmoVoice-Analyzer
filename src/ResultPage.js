import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

// Define a function to map emotions to image sources
const getEmotionImage = (emotion) => {
  switch (emotion.toLowerCase()) {
    case 'happy':
      return '/Images/happy.png';
    case 'sad':
      return '/Images/sad.png';
    case 'angry':
      return '/Images/angry.png';
    case 'surprised':
      return '/Images/surprised.png';
    case 'fear':
      return '/Images/fear.png';
    case 'disgusted':
      return '/Images/disgusted.png';
    default:
      return 'path/to/default.png';
  }
};

const ResultPage = () => {
  const location = useLocation();
  const { emotion } = location.state || { emotion: 'No prediction' };
  const navigate = useNavigate();
  
  const imageSrc = getEmotionImage(emotion);

  const handleBackClick = () => {
    navigate('/');
  };

  return (
    <div className="result-page">
      <h2>Your Predicted Emotion is:</h2>
      <p className="result">{emotion.toUpperCase()}</p>
      <img src={imageSrc} alt={emotion} className="emotion-image" />
      <button onClick={handleBackClick} className="back-button">Go Back</button>
    </div>
  );
};

export default ResultPage;
