from tensorflow.keras.models import load_model

# Paths to your models
models = {
    "alzheimer": r"E:\Projects\ACSC-HACKATHON\frontend\best_alzheimer_model.h5",
    "retina": r"E:\Projects\ACSC-HACKATHON\frontend\best_retina_model.h5",
    "skin_cancer": r"E:\Projects\ACSC-HACKATHON\frontend\skin_cancer_model.h5",
    "tb": r"E:\Projects\ACSC-HACKATHON\frontend\best_tb_mobilenetv2.h5",
    # add bone fracture if needed
}

for name, path in models.items():
    model = load_model(path)
    input_shape = model.input_shape
    print(f"{name} model expects input shape: {input_shape}")
