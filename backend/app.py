from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

# Load the retina model
model = tf.keras.models.load_model('../frontend/best_retina_model.h5')

# Binary classification - your model outputs single probability
# Assuming it predicts probability of diabetic retinopathy
RETINA_CLASSES = ['No DR', 'DR Detected']

def preprocess_image(image_data):
    """Preprocess image for retina model prediction"""
    try:
        print("Starting image preprocessing")
        # Convert base64 to PIL Image
        image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        print(f"Original image size: {image.size}, mode: {image.mode}")
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            print("Converted to RGB")
        
        # Resize to model input size (assuming 224x224)
        image = image.resize((224, 224))
        print(f"Resized to: {image.size}")
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        print(f"Array shape before expand_dims: {img_array.shape}")
        img_array = np.expand_dims(img_array, axis=0)
        print(f"Final array shape: {img_array.shape}")
        
        return img_array
    except Exception as e:
        print(f"Error in preprocessing: {str(e)}")
        raise e

@app.route('/predict/retina', methods=['POST'])
def predict_retina():
    try:
        print("Received prediction request")
        data = request.json
        image_data = data['image']
        print(f"Image data length: {len(image_data)}")
        
        # Preprocess image
        processed_image = preprocess_image(image_data)
        print(f"Processed image shape: {processed_image.shape}")
        
        # Make prediction
        predictions = model.predict(processed_image)
        print(f"Predictions shape: {predictions.shape}")
        print(f"Predictions: {predictions[0]}")
        
        # Binary classification - single output probability
        dr_probability = float(predictions[0][0])
        
        # Threshold at 0.5 for binary classification
        if dr_probability > 0.5:
            predicted_class = 'DR Detected'
            confidence = dr_probability
        else:
            predicted_class = 'No DR'
            confidence = 1 - dr_probability
            
        print(f"Predicted class: {predicted_class}, Confidence: {confidence}")
        
        # Generate recommendations based on prediction
        recommendations = get_recommendations(predicted_class)
        
        return jsonify({
            'success': True,
            'prediction': predicted_class,
            'confidence': f"{confidence * 100:.1f}%",
            'all_predictions': {
                'No DR': f"{(1 - dr_probability) * 100:.1f}%",
                'DR Detected': f"{dr_probability * 100:.1f}%"
            },
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_recommendations(prediction):
    """Get medical recommendations based on prediction"""
    recommendations_map = {
        'No DR': [
            'No diabetic retinopathy detected',
            'Continue regular eye examinations',
            'Maintain good blood sugar control',
            'Follow healthy lifestyle habits'
        ],
        'DR Detected': [
            'Diabetic retinopathy detected',
            'Immediate ophthalmologist consultation required',
            'Monitor blood glucose levels closely',
            'Consider treatment options as advised by specialist'
        ]
    }
    
    return recommendations_map.get(prediction, ['Consult healthcare provider'])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)