from flask import Flask, request, jsonify
import librosa
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Define feature extraction functions
def zcr(data, frame_length=2048, hop_length=512):
    zcr = librosa.feature.zero_crossing_rate(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(zcr)

def rmse(data, frame_length=2048, hop_length=512):
    rmse = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(rmse)

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten: bool = True):
    mfcc_feature = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13)
    return np.squeeze(mfcc_feature.T) if not flatten else np.ravel(mfcc_feature.T)

# Main feature extraction function to ensure 2376 length
def extract_features(data, sr, frame_length=2048, hop_length=512):
    result = np.hstack((zcr(data, frame_length, hop_length),
                        rmse(data, frame_length, hop_length),
                        mfcc(data, sr, frame_length, hop_length)))
    result = np.nan_to_num(result, nan=0.0)
    
    # Ensure fixed size of 2376
    expected_size = 2376
    if result.size < expected_size:
        padded_result = np.zeros(expected_size)
        padded_result[:result.size] = result
        return padded_result
    return result[:expected_size]

# Load and extract features
def get_features(path, duration=2.5, offset=0.6):
    data, sample_rate = librosa.load(path, duration=duration, offset=offset)
    return extract_features(data, sample_rate)

@app.route('/predict', methods=['POST'])
def predict():
    audio_file = request.files['audio']
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        audio_file.save(temp_audio.name)
        features = get_features(temp_audio.name)
    
    features = features.reshape(1, 2376, 1)  # Reshape to (1, 2376, 1) for model input

    # Make the prediction
    prediction = model.predict(features)

    # Define labels and predict
    labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    y_pred = np.argmax(prediction, axis=1)
    predicted_class = labels[y_pred[0]]
    print(predicted_class)
    return jsonify({'emotion': predicted_class})  # Send emotion back as a JSON response

if __name__ == "__main__":
    model = load_model('J:\\ML\\EmoVoice\\emotion-detection\\backend\\model\\res_model.h5')  # Replace with the actual path to your model
    app.run(debug=True)
