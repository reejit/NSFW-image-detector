import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import SGD
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model, load_model

# reusable stuff
import constants
import callbacks
import generators

# No kruft plz
clear_session()

# Config
save_path="saved_model/nsfw_model"
height = constants.SIZES['basic']
width = height
weights_file = "saved_model/nsfw_model"

print ('Starting from last full model run')
model = load_model('weights.best_inception299.hdf5')

# Unlock a few layers deep in Inception v3
model.trainable = False
set_trainable = False
for layer in model.layers:
    if layer.name == 'conv2d_56':
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False

# Let's see it
print('Summary')
print(model.summary())

# Load checkpoint if one is found
#if os.path.exists(weights_file):
#        print ("loading ", weights_file)
#        model.load_weights(weights_file)

# Get all model callbacks
callback_list=callbacks.make_callbacks(save_path)

print('Compile model')
opt = SGD(momentum=.9)
model.compile(
    loss='categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy']
)

# Get training/validation data via generators
train_generator, validation_generator = generators.create_generators(height, width)

print('Start training!')
model.fit(
    train_generator,
    callbacks=callback_list,
    epochs=constants.TOTAL_EPOCHS,
    steps_per_epoch=constants.STEPS_PER_EPOCH,
    shuffle=True,
    workers=4,
    use_multiprocessing=False,
    validation_data=validation_generator,
    validation_steps=constants.VALIDATION_STEPS
)

# Save it for later
print('Saving Model')
model.save("saved_model/nsfw_model")
