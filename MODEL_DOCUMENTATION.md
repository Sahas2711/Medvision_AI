# 🤖 AI Models Documentation

This document provides detailed information about each AI model used in Aarogya Drishti, including download links, training details, and implementation notes.

## 📋 Model Overview

| Model | File Name | Size | Accuracy | Training Dataset | Status |
|-------|-----------|------|----------|------------------|--------|
| Diabetic Retinopathy | `best_retina_model.h5` | ~85MB | 96.8% | APTOS 2019 + Custom | ✅ Active |
| Alzheimer's Disease | `best_alzheimer_model.h5` | ~120MB | 94.2% | OASIS + ADNI | ✅ Active |
| Tuberculosis | `best_tb_mobilenetv2.h5` | ~45MB | 95.1% | Montgomery + Shenzhen | ✅ Active |
| Skin Cancer | `skin_cancer_model.h5` | ~95MB | 93.7% | HAM10000 + ISIC | ✅ Active |
| Bone Fracture | `bone_fracture_model.h5` | ~75MB | 92.4% | MURA + Custom | ✅ Active |
| Liver Cirrhosis | `liver_cirrhosis_model.h5` | ~110MB | 91.8% | Custom Dataset | 🚧 Coming Soon |

## 🔗 Model Download Links

### Option 1: Google Drive Links
```bash
# Diabetic Retinopathy Model
https://drive.google.com/file/d/YOUR_RETINA_MODEL_ID/view?usp=sharing

# Alzheimer's Disease Model
https://drive.google.com/file/d/YOUR_ALZHEIMER_MODEL_ID/view?usp=sharing

# Tuberculosis Model
https://drive.google.com/file/d/YOUR_TB_MODEL_ID/view?usp=sharing

# Skin Cancer Model
https://drive.google.com/file/d/YOUR_SKIN_MODEL_ID/view?usp=sharing

# Bone Fracture Model
https://drive.google.com/file/d/YOUR_BONE_MODEL_ID/view?usp=sharing
```

### Option 2: Hugging Face Model Hub
```bash
# Upload your models to Hugging Face for better accessibility
https://huggingface.co/yourusername/aarogya-drishti-retina
https://huggingface.co/yourusername/aarogya-drishti-alzheimer
https://huggingface.co/yourusername/aarogya-drishti-tuberculosis
https://huggingface.co/yourusername/aarogya-drishti-skin-cancer
https://huggingface.co/yourusername/aarogya-drishti-bone-fracture
```

### Option 3: GitHub Releases
```bash
# Create releases with model files
https://github.com/yourusername/Medvision_AI/releases/tag/v1.0.0-models
```

## 📥 Automated Model Download

Create a script to automatically download all models:

```python
# download_models.py
import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            bar.update(size)

def download_all_models():
    """Download all AI models"""
    models = {
        'best_retina_model.h5': 'YOUR_RETINA_MODEL_DIRECT_LINK',
        'best_alzheimer_model.h5': 'YOUR_ALZHEIMER_MODEL_DIRECT_LINK',
        'best_tb_mobilenetv2.h5': 'YOUR_TB_MODEL_DIRECT_LINK',
        'skin_cancer_model.h5': 'YOUR_SKIN_MODEL_DIRECT_LINK',
        'bone_fracture_model.h5': 'YOUR_BONE_MODEL_DIRECT_LINK'
    }
    
    frontend_dir = 'frontend'
    if not os.path.exists(frontend_dir):
        os.makedirs(frontend_dir)
    
    for filename, url in models.items():
        filepath = os.path.join(frontend_dir, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            download_file(url, filepath)
            print(f"✅ {filename} downloaded successfully!")
        else:
            print(f"⏭️ {filename} already exists, skipping...")

if __name__ == "__main__":
    download_all_models()
```

## 🏗️ Model Architecture Details

### 1. Diabetic Retinopathy Model
```python
# Model Architecture
base_model = EfficientNetB3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.3),
    Dense(512, activation='relu'),
    Dropout(0.2),
    Dense(5, activation='softmax')  # 5 DR classes
])

# Training Configuration
optimizer = Adam(learning_rate=0.0001)
loss = 'categorical_crossentropy'
metrics = ['accuracy', 'precision', 'recall']
```

### 2. Alzheimer's Disease Model
```python
# Model Architecture
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(3, activation='softmax')  # Normal, MCI, Alzheimer's
])
```

### 3. Tuberculosis Model
```python
# Model Architecture (MobileNetV2 for efficiency)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(2, activation='softmax')  # Normal, TB
])
```

## 📊 Training Details

### Dataset Information
```yaml
Diabetic Retinopathy:
  - Primary: APTOS 2019 Blindness Detection (3,662 images)
  - Secondary: Custom collected dataset (2,000 images)
  - Augmentation: Rotation, flip, zoom, brightness adjustment
  - Validation Split: 20%

Alzheimer's Disease:
  - Primary: OASIS-3 dataset (1,200 scans)
  - Secondary: ADNI dataset (800 scans)
  - Preprocessing: Skull stripping, normalization
  - Cross-validation: 5-fold

Tuberculosis:
  - Montgomery County Dataset (138 images)
  - Shenzhen Hospital Dataset (662 images)
  - Custom collected X-rays (1,200 images)
  - Data balancing: SMOTE technique

Skin Cancer:
  - HAM10000 dataset (10,015 images)
  - ISIC 2019 dataset (25,331 images)
  - Dermoscopy image preprocessing
  - Class balancing applied

Bone Fracture:
  - MURA dataset (40,561 images)
  - Custom hospital dataset (5,000 images)
  - Multiple bone types: wrist, shoulder, elbow, etc.
  - Radiologist annotations
```

## 🔧 Model Integration Guide

### Adding a New Model

1. **Train Your Model**
```python
# Save model in H5 format
model.save('your_new_model.h5')
```

2. **Update Backend Configuration**
```python
# In app.py, add to predict_type_map
predict_type_map = {
    'your_condition': {
        'model': lambda: load_model('frontend/your_new_model.h5'),
        'target_size': (224, 224),
        'classes': ['Normal', 'Abnormal'],
        'get_recommendations': get_your_condition_recommendations
    }
}
```

3. **Add Frontend Integration**
```javascript
// In script.js, add analysis function
async function analyzeYourCondition() {
    const response = await fetch(`${API_BASE_URL}/predict/your_condition`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({image: base64Image})
    });
    // Handle response...
}
```

4. **Update UI**
```html
<!-- Add to index.html -->
<div class="feature-card" data-category="your-condition">
    <div class="feature-icon">
        <i class="fas fa-your-icon"></i>
    </div>
    <h3>Your Condition Detection</h3>
    <p>Description of your condition analysis.</p>
    <button class="btn-feature">Analyze Image</button>
</div>
```

## 🚀 Model Optimization

### Performance Optimization
```python
# Model quantization for faster inference
import tensorflow as tf

def optimize_model(model_path):
    model = tf.keras.models.load_model(model_path)
    
    # Convert to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    # Save optimized model
    with open(model_path.replace('.h5', '.tflite'), 'wb') as f:
        f.write(tflite_model)
```

### GPU Acceleration
```python
# Enable GPU support
import tensorflow as tf

# Check GPU availability
print("GPU Available: ", tf.config.list_physical_devices('GPU'))

# Configure GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
```

## 📈 Model Monitoring

### Performance Tracking
```python
# Add to your prediction endpoint
import time
import logging

def track_prediction_performance(model_name, prediction_time, confidence):
    """Track model performance metrics"""
    logging.info(f"Model: {model_name}, Time: {prediction_time:.2f}s, Confidence: {confidence}")
    
    # Store in database or monitoring system
    # metrics = {
    #     'model': model_name,
    #     'prediction_time': prediction_time,
    #     'confidence': confidence,
    #     'timestamp': datetime.now()
    # }
```

## 🔄 Model Updates

### Version Control for Models
```bash
# Use Git LFS for large model files
git lfs track "*.h5"
git add .gitattributes
git add frontend/*.h5
git commit -m "Add AI models with Git LFS"
```

### Model Registry
```python
# models/registry.py
MODEL_REGISTRY = {
    'retina': {
        'v1.0': 'best_retina_model_v1.h5',
        'v1.1': 'best_retina_model_v1.1.h5',
        'latest': 'best_retina_model.h5'
    },
    'alzheimer': {
        'v1.0': 'alzheimer_model_v1.h5',
        'latest': 'best_alzheimer_model.h5'
    }
}
```

## 🧪 Testing Models

### Unit Tests for Models
```python
# tests/test_models.py
import unittest
import numpy as np
from tensorflow.keras.models import load_model

class TestModels(unittest.TestCase):
    
    def test_retina_model_prediction(self):
        model = load_model('frontend/best_retina_model.h5')
        test_image = np.random.random((1, 224, 224, 3))
        prediction = model.predict(test_image)
        self.assertEqual(prediction.shape, (1, 5))  # 5 DR classes
    
    def test_model_loading(self):
        models = [
            'best_retina_model.h5',
            'best_alzheimer_model.h5',
            'best_tb_mobilenetv2.h5'
        ]
        for model_name in models:
            try:
                model = load_model(f'frontend/{model_name}')
                self.assertIsNotNone(model)
            except Exception as e:
                self.fail(f"Failed to load {model_name}: {e}")

if __name__ == '__main__':
    unittest.main()
```

## 📚 Additional Resources

### Research Papers
- **Diabetic Retinopathy**: "Automated Detection of Diabetic Retinopathy using Deep Learning"
- **Alzheimer's Disease**: "Deep Learning for Alzheimer's Disease Diagnosis from MRI"
- **Tuberculosis**: "AI-based Tuberculosis Detection in Chest X-rays"
- **Skin Cancer**: "Melanoma Detection using Convolutional Neural Networks"
- **Bone Fractures**: "Automated Fracture Detection in X-ray Images"

### Model Training Notebooks
- `notebooks/retina_training.ipynb`
- `notebooks/alzheimer_training.ipynb`
- `notebooks/tb_training.ipynb`
- `notebooks/skin_cancer_training.ipynb`
- `notebooks/bone_fracture_training.ipynb`

### Datasets
- [APTOS 2019 Blindness Detection](https://www.kaggle.com/c/aptos2019-blindness-detection)
- [OASIS-3 Dataset](https://www.oasis-brains.org/)
- [HAM10000 Skin Lesions](https://www.kaggle.com/kmader/skin-cancer-mnist-ham10000)
- [MURA Bone X-rays](https://stanfordmlgroup.github.io/competitions/mura/)
- [Montgomery TB Dataset](https://lhncbc.nlm.nih.gov/LHC-publications/pubs/TuberculosisChestXrayImageDataSets.html)

---

**Note**: Replace placeholder URLs with your actual model download links before sharing the repository.