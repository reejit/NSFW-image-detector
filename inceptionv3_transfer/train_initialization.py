import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import SGD
from pathlib import Path
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, AveragePooling2D
from tensorflow.keras import initializers, regularizers
from PIL import ImageFile
import tensorflow as tf
ImageFile.LOAD_TRUNCATED_IMAGES = True

# reusable stuff
import constants
import callbacks
import generators

# No kruft plz
clear_session()

# Config
height = constants.SIZES['basic']
width = height
#checkpoint_path="training_1/cp-0005.ckpt"
save_path="saved_model/nsfw_model"

conv_base = InceptionV3(
    weights='imagenet', 
    include_top=False, +
+

    input_shape=(height, width, constants.NUM_CHANNELS)
)

# First time run, no unlocking
conv_base.trainable = False

# Let's see it
print('Summary')
print(conv_base.summary())

# Let's construct that top layer replacement
x = conv_base.output
x = AveragePooling2D(pool_size=(8, 8))(x)
x - Dropout(0.4)(x)
x = Flatten()(x)
x = Dense(256, activation='relu', kernel_initializer=initializers.he_normal(seed=None), kernel_regularizer=regularizers.l2(.0005))(x)
x = Dropout(0.5)(x)
# Essential to have another layer for better accuracy
x = Dense(128,activation='relu', kernel_initializer=initializers.he_normal(seed=None))(x)
x = Dropout(0.25)(x)
predictions = Dense(constants.NUM_CLASSES,  kernel_initializer="glorot_uniform", activation='softmax')(x)

print('Stacking New Layers')
model = Model(inputs = conv_base.input, outputs=predictions)

# Load checkpoint if one is found
#if os.path.exists(checkpoint_path):
#print ("loading ", checkpoint_path)
#model.load_weights(checkpoint_path)
#
# Define callback checkpoint for saving model
#cp_callback = tf.keras.callbacks.ModelCheckpoint(
#        save_path,save_weights_only=False, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callback_list=callbacks.make_callbacks(save_path)
print('Compile model')
# originally adam, but research says SGD with scheduler
# opt = Adam(lr=0.001, amsgrad=True)
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
    train_g enerator,
    callbacks=callback_list,
    epochs=constants.TOTAL_EPOCHS,
    steps_per_epoch=constants.STEPS_PER_EPOCH,
    shuffle=True,
    workers=4,
    use_multiprocessing=False,
    validation_data=validation_generator,
    validation_steps=constants.VALIDATION_STEPS
)
print('Saving Model')
model.save("saved_model/nsfw_model")
