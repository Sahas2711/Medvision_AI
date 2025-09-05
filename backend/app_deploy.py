import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'models': {}})

# Demo prediction endpoints
@app.route('/predict/<predict_type>', methods=['POST'])
def demo_predict(predict_type):
    return jsonify({
        'success': True,
        'prediction': 'Normal' if predict_type != 'skin' else 'Benign',
        'confidence': '94.2%',
        'all_predictions': {'Normal': '94.2%', 'Abnormal': '5.8%'},
        'recommendations': ['No abnormalities detected', 'Continue regular monitoring'],
        'images': {'original': '', 'gradcam': '', 'overlay': ''}
    })

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('../frontend', path)
    except:
        return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)