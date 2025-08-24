import cv2
import base64
import numpy as np
import tensorflow as tf
from PIL import Image
import io

# Helper function to convert a cv2 image array to a Base64 string
def to_base64(img):
    """Encodes an image array into a Base64 string."""
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

def predict_with_gradcam(image_data, model, labels):
    """
    Predicts and generates Grad-CAM visualizations, returning them as Base64 strings.
    """
    # Preprocess the image
    image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    input_tensor = np.expand_dims(img_array, axis=0)

    # Prediction
    predictions = model.predict(input_tensor)
    pred_prob = float(predictions[0][0])
    pred_label = labels[int(pred_prob >= 0.5)]

    # Find the last convolutional layer
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer = layer.name
            break

    if not last_conv_layer:
        return pred_label, pred_prob, None

    # Grad-CAM model
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(input_tensor)
        loss = predictions[:, 0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1).numpy()
    heatmap = np.maximum(heatmap, 0)
    heatmap /= (heatmap.max() + 1e-8)
    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Resize heatmap to original image size
    heatmap_resized = cv2.resize(heatmap_color, (img_array.shape[1], img_array.shape[0]))
    
    # Create the overlay image
    overlay = cv2.addWeighted(cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR), 0.4, heatmap_resized, 0.6, 0)

    # Encode all three images to Base64
    images = {
        'original': to_base64(cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)),
        'gradcam': to_base64(heatmap_resized),
        'overlay': to_base64(overlay)
    }

    return pred_label, pred_prob, images
