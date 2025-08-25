# MedVision AI - Frontend-Backend Integration Guide

## Quick Start

### 1. Start the Backend Server
```bash
# Option 1: Use the batch file (Windows)
double-click start_backend.bat

# Option 2: Manual start
cd backend
pip install -r requirements.txt
python app.py
```

### 2. Open Frontend
Open `frontend/index.html` in your browser

## Integration Features

### ✅ Real AI Model Integration
- **Retina Model**: `best_retina_model.h5` - Real diabetic retinopathy detection
- **TB Model**: `best_tb_mobilenetv2.h5` - Real tuberculosis detection with 3-image output  
- **Skin Cancer Model**: `skin_cancer_model.h5` - Real skin cancer classification
- **Alzheimer Model**: `alzheimers_cnn_model.h5` - Real Alzheimer's detection

### ✅ API Endpoints
- `POST /predict/retina` - Diabetic retinopathy analysis
- `POST /predict/tb` - Tuberculosis analysis (returns 3 images)
- `POST /predict/skin` - Skin cancer analysis  
- `POST /predict/alzheimer` - Alzheimer's analysis
- `GET /health` - Health check for all models

### ✅ Frontend Features
- **Real-time Backend Status**: Shows warning if backend is not running
- **File Upload**: Converts images to base64 for API calls
- **Error Handling**: Proper error messages for network/model issues
- **Loading States**: Spinner animations during analysis
- **Enhanced Results**: TB analysis shows 3 generated analysis images

## How It Works

1. **Image Upload**: User selects medical image file
2. **Base64 Conversion**: Frontend converts image to base64 format
3. **API Call**: Sends POST request to Flask backend with image data
4. **Model Prediction**: Backend processes image through TensorFlow models
5. **Results Display**: Frontend shows prediction, confidence, and recommendations

## Error Handling

- **Backend Offline**: Shows warning banner and helpful error messages
- **Model Loading Issues**: Backend gracefully handles missing model files
- **Network Errors**: Frontend provides clear feedback about connection issues
- **Invalid Images**: Proper validation and error messages

## File Structure
```
ACSC-HACKATHON/
├── frontend/
│   ├── index.html              # Main website
│   ├── script.js               # Integrated with backend APIs
│   ├── styles.css              # UI styling
│   └── *.h5                    # AI model files
├── backend/
│   ├── app.py                  # Flask server with all endpoints
│   └── requirements.txt        # Python dependencies
├── start_backend.bat           # Easy server startup
└── INTEGRATION_GUIDE.md        # This file
```

## Testing the Integration

1. Start backend server
2. Open frontend in browser
3. Upload a medical image
4. Select analysis type (Retina, TB, Skin Cancer, Alzheimer)
5. Click analyze button
6. View real AI predictions and recommendations

## Notes

- Backend runs on `http://localhost:5000`
- All models expect 224x224 RGB images
- CORS is enabled for frontend-backend communication
- Models are loaded once at startup for better performance