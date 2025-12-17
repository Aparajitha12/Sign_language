import cv2
import numpy as np
import tensorflow as tf

# Load your trained CNN model
model = tf.keras.models.load_model("asl_cnn_model.h5")

# Define your label map (modify based on your dataset)
label_map = {i: chr(65 + i) for i in range(26)}  # A-Z

# Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("✅ Press 'q' to quit.")

# Loop for live prediction
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect

    # Draw ROI box (top-left 100,100 to bottom-right 300,300)
    x1, y1, x2, y2 = 100, 100, 300, 300
    roi = frame[y1:y2, x1:x2]

    # Preprocess ROI
    roi_resized = cv2.resize(roi, (64, 64))  # Match training size
    roi_normalized = roi_resized / 255.0     # Normalize pixel values
    roi_reshaped = np.expand_dims(roi_normalized, axis=0)  # Add batch dimension

    # Predict
    pred_prob = model.predict(roi_reshaped, verbose=0)[0]
    pred_class = np.argmax(pred_prob)
    confidence = np.max(pred_prob)

    # Threshold to ignore low-confidence predictions
    if confidence < 0.5:
        predicted_label = "Nothing"
    else:
        predicted_label = label_map.get(pred_class, "Unknown")

    # Show prediction on frame
    cv2.putText(frame, f"Prediction: {predicted_label} ({confidence:.2f})",
                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show the webcam frame
    cv2.imshow("ASL Live Prediction", frame)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Quitting.")
        break

cap.release()
cv2.destroyAllWindows()
