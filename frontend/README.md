# MedVision AI - Frontend-Backend Integration

## Overview
This project integrates multiple AI models for medical image analysis with a comprehensive frontend interface.

## Features Implemented

### 1. Multiple Disease Models Integration
- **Retina Model**: `best_retina_model.h5` - Diabetic retinopathy detection
- **TB Model**: `best_tb_mobilenetv2.h5` - Tuberculosis detection with 3-image output
- **Skin Cancer Model**: `skin_cancer_model.h5` - Skin cancer classification

### 2. Frontend Features
- **Disease Information Cards**: Interactive cards for each disease type
- **Separate Analysis Buttons**: Dedicated buttons for TB and Skin Cancer models
- **Multi-Image Display**: TB analysis shows 3 generated analysis images
- **Disease Detail Pages**: Individual HTML pages for each disease with comprehensive information
- **Responsive Design**: Mobile-friendly interface

### 3. Backend API Endpoints
- `POST /predict/retina` - Diabetic retinopathy analysis
- `POST /predict/tb` - Tuberculosis analysis (returns 3 images)
- `POST /predict/skin` - Skin cancer analysis
- `GET /health` - Health check for all models

### 4. Disease Information Pages
- `alzheimer-info.html` - Alzheimer's disease information
- `skin-cancer-info.html` - Skin cancer information
- `diabetic-retinopathy-info.html` - Diabetic retinopathy information
- `bone-fracture-info.html` - Bone fracture information
- `tuberculosis-info.html` - Tuberculosis information

## File Structure
```
frontend/
├── index.html                      # Main page with disease cards
├── script.js                       # JavaScript with model integration
├── styles.css                      # CSS with disease card styling
├── alzheimer-info.html             # Disease info pages
├── skin-cancer-info.html
├── diabetic-retinopathy-info.html
├── bone-fracture-info.html
├── tuberculosis-info.html
├── best_retina_model.h5            # AI models
├── best_tb_mobilenetv2.h5
├── skin_cancer_model.h5
└── download.png

backend/
├── app.py                          # Flask backend with all model endpoints
└── requirements.txt                # Python dependencies
```

## Usage

### Starting the Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Features
1. **Disease Cards**: Click any disease card to view detailed information
2. **Image Upload**: Upload medical images for analysis
3. **Model Selection**: Choose specific analysis type
4. **TB Analysis**: Use "Analyze TB" button for tuberculosis-specific analysis with 3-image output
5. **Skin Cancer Analysis**: Use "Analyze Skin Cancer" button for skin cancer-specific analysis

### Button Visibility Logic
- **General Analysis**: Always visible for all disease types
- **TB Button**: Only visible when "Tuberculosis Detection" is selected
- **Skin Cancer Button**: Only visible when "Skin Cancer Detection" is selected

## Technical Implementation

### TB Model Integration
- Returns 3 analysis images as base64-encoded data
- Displays images in a grid layout
- Provides TB-specific recommendations

### Skin Cancer Model Integration
- Binary classification (Benign/Malignant)
- Skin cancer-specific recommendations
- Dermatologist consultation information

### Disease Navigation
- Cards navigate to dedicated HTML pages
- Each page contains comprehensive disease information
- Specialist consultation details included

## Dependencies
- Flask 2.3.3
- TensorFlow 2.20.0
- OpenCV 4.8.1.78 (for TB image generation)
- PIL/Pillow 10.0.1
- NumPy 1.24.3

## Notes
- Maintains existing retina model functionality
- All models use 224x224 input size
- Demo images generated for TB analysis when backend unavailable
- Responsive design works on mobile devices