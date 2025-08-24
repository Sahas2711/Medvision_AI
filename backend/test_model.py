import tensorflow as tf
import numpy as np

# Load the model
try:
    model = tf.keras.models.load_model('../frontend/best_retina_model.h5')
    print("Model loaded successfully!")
    
    # Print model summary
    print("\nModel Summary:")
    model.summary()
    
    # Test with dummy input
    print(f"\nModel input shape: {model.input_shape}")
    print(f"Model output shape: {model.output_shape}")
    
    # Create test input
    test_input = np.random.random((1, 224, 224, 3))
    print(f"\nTest input shape: {test_input.shape}")
    
    # Make prediction
    prediction = model.predict(test_input)
    print(f"Prediction shape: {prediction.shape}")
    print(f"Prediction values: {prediction[0]}")
    print(f"Number of classes: {len(prediction[0])}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()