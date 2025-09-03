import os
from flask import Flask, send_from_directory, jsonify

try:
    from app import app
except Exception as e:
    print(f"Error importing app: {e}")
    app = Flask(__name__)
    from flask_cors import CORS
    CORS(app)

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'models': {}})

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