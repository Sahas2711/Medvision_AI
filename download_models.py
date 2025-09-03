import os
import requests

def download_from_gdrive(file_id, destination):
    """Download file from Google Drive"""
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
            break
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

# Google Drive file IDs (replace with your actual file IDs)
models = {
    'best_retina_model.h5': 'YOUR_GDRIVE_FILE_ID_1',
    'best_tb_mobilenetv2.h5': 'YOUR_GDRIVE_FILE_ID_2',
    'skin_cancer_model.h5': 'YOUR_GDRIVE_FILE_ID_3',
    'best_alzheimer_model.h5': 'YOUR_GDRIVE_FILE_ID_4',
    'bone_fracture_model.h5': 'YOUR_GDRIVE_FILE_ID_5'
}

os.makedirs('frontend', exist_ok=True)
for filename, file_id in models.items():
    if not os.path.exists(f'frontend/{filename}'):
        print(f"Downloading {filename}...")
        try:
            download_from_gdrive(file_id, f'frontend/{filename}')
            print(f"✓ {filename} downloaded")
        except Exception as e:
            print(f"✗ Failed to download {filename}: {e}")