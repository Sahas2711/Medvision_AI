import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from tensorflow.keras.preprocessing.image import load_img, img_to_array  # ✅ Added

app = Flask(__name__)
CORS(app)

# ==================================
# Model Loading
# ==================================
def load_model(path, model_name):
    try:
        model = tf.keras.models.load_model(path)
        print(f"{model_name} model loaded successfully")
        return model
    except Exception as e:
        print(f"Error loading {model_name} model from {path}: {e}")
        return None

retina_model = load_model('../frontend/best_retina_model.h5', 'Retina')
tb_model = load_model('../frontend/best_tb_mobilenetv2.h5', 'TB')
skin_model = load_model('../frontend/skin_cancer_model.h5', 'Skin cancer')
alzheimer_model = load_model('../frontend/best_alzheimer_model.h5', 'Alzheimer')
bone_model = load_model('../frontend/bone_fracture_model.h5', 'Bone fracture')

# ==================================
# Prediction Type Mapping
# ==================================
predict_type_map = {
    'retina': {
        'model': retina_model,
        'target_size': (224, 224),
        'get_recommendations': lambda p: {
            'No DR': ['No diabetic retinopathy detected', 'Continue regular eye examinations'],
            'DR Detected': ['Diabetic retinopathy detected', 'Immediate ophthalmologist consultation required']
        }.get(p, ['Consult healthcare provider']),
        'classes': ['No DR', 'DR Detected']
    },
    'tb': {
        'model': tb_model,
        'target_size': (224, 224),
        'get_recommendations': lambda p: {
            'Normal': ['No TB detected', 'Routine monitoring'],
            'TB Detected': ['TB detected', 'Immediate consultation required']
        }.get(p, ['Consult healthcare provider']),
        'classes': ['Normal', 'TB Detected']
    },
    'skin': {
        'model': skin_model,
        'target_size': (150, 150),
        'get_recommendations': lambda p: {
            'Benign': ['Benign lesion detected', 'Continue monitoring', 'Regular skin checks recommended'],
            'Malignant': ['Malignant lesion detected', 'Urgent dermatologist consultation', 'Immediate medical attention required']
        }.get(p, ['Consult healthcare provider']),
        'classes': ['Benign', 'Malignant']
    },
    'alzheimer': {
        'model': alzheimer_model,
        'target_size': (150, 150),
        'get_recommendations': lambda p: {
            'Normal': ['No Alzheimer detected', 'Continue regular monitoring', 'Maintain healthy lifestyle'],
            'Alzheimer Detected': ['Alzheimer detected', 'Neurologist consultation required', 'Early intervention recommended']
        }.get(p, ['Consult healthcare provider']),
        'classes': ['Normal', 'Alzheimer Detected']
    },
    'bone': {
        'model': bone_model,
        'target_size': (224, 224),
        'get_recommendations': lambda p: {
            'No Fracture': ['No fracture detected', 'Continue normal activities', 'Monitor for persistent pain'],
            'Fracture Detected': ['Fracture detected', 'Orthopedic consultation required', 'Immediate medical attention needed']
        }.get(p, ['Consult healthcare provider']),
        'classes': ['No Fracture', 'Fracture Detected']
    }
}

# ==================================
# Image Processing & Grad-CAM
# ==================================
def preprocess_image(image_data, target_size):
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        raise

def get_last_conv_layer(model):
    try:
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer.name
        # If no Conv2D layer found, try to find any convolutional layer
        for layer in reversed(model.layers):
            if 'conv' in layer.name.lower():
                return layer.name
    except Exception as e:
        print(f"Error finding conv layer: {e}")
    return None

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    try:
        grad_model = tf.keras.models.Model(
            [model.inputs],
            [model.get_layer(last_conv_layer_name).output, model.output]
        )
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            predictions = tf.convert_to_tensor(predictions)
            # Handle different prediction shapes
            if len(predictions.shape) > 1 and predictions.shape[1] > 1:
                pred_idx = np.argmax(predictions[0])
                loss = predictions[:, pred_idx]
            else:
                # For binary classification, use the single output
                if len(predictions.shape) > 1:
                    loss = predictions[:, 0]
                else:
                    loss = predictions
        grads = tape.gradient(loss, conv_outputs)
        if grads is None:
            return None
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1).numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap /= (heatmap.max() + 1e-8)
        return heatmap
    except Exception as e:
        print(f"Error generating heatmap: {e}")
        return None

def generate_gradcam_images(img_array, model):
    try:
        original_img = (img_array[0] * 255).astype(np.uint8)
        last_conv_layer_name = get_last_conv_layer(model)
        if not last_conv_layer_name:
            print("No convolutional layer found")
            return None
        
        heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)
        if heatmap is None:
            print("Failed to generate heatmap")
            return None
            
        heatmap_resized = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap_colored = np.uint8(255 * heatmap_resized)
        heatmap_colored = cv2.applyColorMap(heatmap_colored, cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR), 0.4, heatmap_colored, 0.6, 0)

        def to_base64(img):
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            return base64.b64encode(buffer).decode('utf-8')

        return {
            'original': to_base64(cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)),
            'gradcam': to_base64(heatmap_colored),
            'overlay': to_base64(overlay)
        }
    except Exception as e:
        print(f"Error in generate_gradcam_images: {e}")
        return None

# ==================================
# Unified Prediction Route
# ==================================
@app.route('/predict/<predict_type>', methods=['POST'])
def unified_predict(predict_type):
    try:
        config = predict_type_map.get(predict_type)
        if not config:
            return jsonify({'success': False, 'error': 'Invalid prediction type'}), 404
        
        model = config['model']
        target_size = config['target_size']
        get_recs = config['get_recommendations']
        classes = config['classes']

        if model is None:
            raise Exception(f"{predict_type.capitalize()} model not loaded")
        
        # Validate model input shape
        try:
            expected_shape = model.input_shape
            print(f"{predict_type} model input shape: {expected_shape}")
        except Exception as e:
            print(f"Could not get input shape for {predict_type}: {e}")

        data = request.json
        image_data = data['image']
        
        processed_image = preprocess_image(image_data, target_size)
        print(f"Processed image shape for {predict_type}: {processed_image.shape}")
        predictions = model.predict(processed_image, verbose=0)
        predictions = np.array(predictions)
        print(f"Predictions shape for {predict_type}: {predictions.shape}")
        
        # Handle different prediction formats
        if len(predictions.shape) > 1 and predictions.shape[1] > 1:
            # Multi-class classification
            if predictions.shape[0] == 0:
                return jsonify({'success': False, 'error': 'No predictions made'}), 500
            predicted_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_idx])
            predicted_class = classes[predicted_idx]
            all_predictions = {classes[i]: f"{float(p) * 100:.1f}%" for i, p in enumerate(predictions[0])}
        else:
            # Binary classification - handle different shapes
            if len(predictions.shape) > 1:
                probability = float(predictions[0][0])
            else:
                probability = float(predictions[0])
            
            # Ensure probability is between 0 and 1
            probability = max(0.0, min(1.0, probability))
            
            if probability > 0.5:
                predicted_class = classes[1] if len(classes) > 1 else classes[0]
                confidence = probability
            else:
                predicted_class = classes[0]
                confidence = 1 - probability
            
            if len(classes) > 1:
                all_predictions = {
                    classes[0]: f"{(1 - probability) * 100:.1f}%", 
                    classes[1]: f"{probability * 100:.1f}%"
                }
            else:
                all_predictions = {classes[0]: f"{confidence * 100:.1f}%"}

        recommendations = get_recs(predicted_class)
        
        response_data = {
            'success': True,
            'prediction': predicted_class,
            'confidence': f"{confidence * 100:.1f}%",
            'all_predictions': all_predictions,
            'recommendations': recommendations
        }
        
        try:
            gradcam_images = generate_gradcam_images(processed_image, model)
            if gradcam_images:
                response_data['images'] = gradcam_images
            else:
                print(f"No Grad-CAM images generated for {predict_type}")
                response_data['images'] = generate_demo_images()
        except Exception as e:
            print(f"Grad-CAM generation failed for {predict_type}: {e}")
            response_data['images'] = generate_demo_images()

        return jsonify(response_data)
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================================
# Demo Image Generation
# ==================================
def generate_demo_images():
    """Generate demo images when Grad-CAM fails"""
    try:
        # Create simple gradient images
        demo_original = np.zeros((224, 224, 3), dtype=np.uint8)
        demo_original[:, :] = [240, 240, 240]  # Light gray
        
        demo_gradcam = np.zeros((224, 224, 3), dtype=np.uint8)
        for i in range(224):
            demo_gradcam[i, :] = [int(100 + i*0.5), 255, int(100 + i*0.3)]
        
        demo_overlay = np.zeros((224, 224, 3), dtype=np.uint8)
        for i in range(224):
            demo_overlay[i, :] = [255, int(200 - i*0.3), int(100 + i*0.4)]
        
        def to_base64(img):
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            return base64.b64encode(buffer).decode('utf-8')
        
        return {
            'original': to_base64(demo_original),
            'gradcam': to_base64(demo_gradcam),
            'overlay': to_base64(demo_overlay)
        }
    except Exception as e:
        print(f"Error generating demo images: {e}")
        return {
            'original': '',
            'gradcam': '',
            'overlay': ''
        }

# ==================================
# Health Check
# ==================================
@app.route('/health', methods=['GET'])
def health_check():
    model_status = {
        'retina': retina_model is not None,
        'tb': tb_model is not None,
        'skin': skin_model is not None,
        'alzheimer': alzheimer_model is not None,
        'bone': bone_model is not None
    }
    return jsonify({
        'status': 'healthy',
        'models': model_status
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
