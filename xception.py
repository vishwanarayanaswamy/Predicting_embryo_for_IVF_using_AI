import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam

def create_xception_model():
    # Load pre-trained Xception model without the top layer
    base_model = Xception(weights="imagenet", include_top=False, input_shape=(128, 128, 3))

    # Unfreeze last 10 layers for fine-tuning
    for layer in base_model.layers[-10:]:
        layer.trainable = True

    # Add custom layers for embryo classification
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)  # Prevents overfitting
    output = Dense(1, activation="sigmoid")(x)  # Binary classification

    # Create and compile model
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss="binary_crossentropy", metrics=["accuracy"])
    
    return model

if __name__ == "__main__":
    model = create_xception_model()
    model.save("xception_model.h5")
    print("Model saved as xception_model.h5")
