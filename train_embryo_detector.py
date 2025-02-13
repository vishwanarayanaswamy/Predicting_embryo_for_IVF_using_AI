import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ✅ Step 1: Ensure dataset exists
DATASET_PATH = "dataset/train/"
if not os.path.exists(DATASET_PATH):
    print("❌ Dataset not found! Please create 'dataset/train/embryo' and 'dataset/train/non_embryo'")
    exit()

# ✅ Step 2: Apply Data Augmentation to Prevent Overfitting
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=30,       # Rotate images randomly
    width_shift_range=0.2,   # Shift width
    height_shift_range=0.2,  # Shift height
    shear_range=0.2,         # Shearing transformation
    zoom_range=0.2,          # Zoom in/out
    horizontal_flip=True,    # Flip images horizontally
    fill_mode="nearest"
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(128, 128),
    batch_size=32,
    class_mode="binary"
)

# ✅ Step 3: Print class mapping (Ensures embryo = 1 and non-embryo = 0)
print("Class Mapping:", train_generator.class_indices)

# ✅ Step 4: Create Embryo Detector Model
def create_embryo_detector():
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(128, 128, 3))

    # ✅ Unfreeze last 10 layers for better training
    for layer in base_model.layers[-10:]:
        layer.trainable = True  

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    output = Dense(1, activation="sigmoid")(x)  # Binary classification: Embryo (1) vs. Not Embryo (0)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss="binary_crossentropy", metrics=["accuracy"])
    
    return model

# ✅ Step 5: Train Model
model = create_embryo_detector()
model.fit(train_generator, epochs=20)  # Train for 20 epochs

# ✅ Step 6: Save Model
MODEL_PATH = "embryo_detector.h5"
model.save(MODEL_PATH)
print(f"✅ Embryo detection model saved as {MODEL_PATH}")
