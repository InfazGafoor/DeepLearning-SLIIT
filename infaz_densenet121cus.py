# -*- coding: utf-8 -*-
"""Infaz -DenseNet121Cus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1exfip1xPLsv-CLPRfgkc93tGNZxgbaxk
"""

from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.layers import Input, Flatten, Dense
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt

#Mount the drive
from google.colab import drive
drive.mount('/content/drive')

# Define input shape
input_shape = (224, 224, 3)

# Define the training dataset path
train_path = '/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Train'
# Define the testing dataset path
valid_path = '/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Test'

# Load the pre-trained DenseNet121 model
# Here we will be using imagenet weights.so,weights='imagenet'
# we will use this model for 9 categories.not for 1000 categories.so,include_top=False
densenet_base = DenseNet121(input_shape=input_shape, weights='imagenet', include_top=False)

densenet_base.summary()

# Freeze the layers of the pre-trained model
for layer in densenet_base.layers:
    layer.trainable = False

#glob() will tell us how many folders are present in the particular pathwithin the brackets
from glob import glob
folders = glob('/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Train/*')
# edit this with actual path

folders

len(folders)

# Add custom layers for your classification task
x = Flatten()(densenet_base.output)
x = Dense(256, activation='relu')(x)
x = Dense(len(folders), activation='softmax')(x)

# Create the model
densenet_model = Model(inputs=densenet_base.input, outputs=x)

# Compile the model
densenet_model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# print the summary of the model
densenet_model.summary()

from tensorflow.keras.preprocessing.image import ImageDataGenerator
#Setting up the training data generator
train_datagen = ImageDataGenerator(rescale = 1./255, # Rescale pixel values to a range of [0, 1]
                                  shear_range = 0.2, # Randomly apply shearing transformation
                                  zoom_range = 0.2,  # Randomly apply zooming transformation
                                  horizontal_flip = True) # Randomly flip images horizontally
#Setting up the test data generator
#For the test data generator, only the rescale parameter is specified. This is because data augmentation techniques like shearing, zooming, and flipping should not be applied to the test dataset. The test dataset should remain as it is to evaluate the model's performance on real, unaltered data.
test_datagen = ImageDataGenerator(rescale = 1./255)

#make sure you provide the same target size as initiated for the image size
training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Train',
                                                 target_size = (224,224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

#make sure you provide the same target size as initiated for the image size
test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Test',
                                            target_size = (224,224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# fit the model
# Run the cell. It will take some time to execute
r=densenet_model.fit(
    training_set,
    validation_data=test_set,
    epochs=20,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)

# plot the loss
# plt.plot() function is used to display the training loss and validation loss in same plot

plt.plot(r.history['loss'], label='train loss') # give label to training loss
plt.plot(r.history['val_loss'], label='val loss') # give label to validation loss
plt.legend() #to add a legend to the plot
plt.show() #displays the plot on the screen
plt.savefig('AccVal_acc') # save the plot

# save it as a h5 file

from tensorflow.keras.models import load_model

# 'model' is your trained ResNet50 model above
densenet_model.save('DenseNet121Cus.h5')

#The code is using a trained model (model) to make predictions on a dataset (test_set) using the predict method.

y_pred = densenet_model.predict(test_set)

y_pred

#you're using the NumPy library in Python to work with an array called y_pred and you want to find the index (or class) with the highest predicted value along axis 1.
import numpy as np

# Find the class with the highest probability for each sample
y_pred = np.argmax(y_pred, axis=1)

y_pred

#This module is used for loading pre-trained or saved Keras models.

from tensorflow.keras.models import load_model

#This module is used for image preprocessing and augmentation when working with image data.
#It provides functions and classes to load, preprocess, and augment images before feeding them into deep learning models built using TensorFlow's Keras API.
#Common functions include load_img, img_to_array, array_to_img, etc., which help in loading and converting images to NumPy arrays suitable for feeding into a neural network.

from tensorflow.keras.preprocessing import image

# Load a pre-trained model

model = load_model('DenseNet121Cus.h5')

#we can use the loaded model for inference or further training

# To load an image file from the path within brackets and resize it to the target size(load_img function from TensorFlow's Keras preprocessing module )
img=image.load_img('/content/drive/MyDrive/Deep Learning/CarDataset/CarDataset/Test/matiz black/000013.jpg',target_size=(224,224))

image

# image.img_to_array(img): This function takes an image object (typically loaded using image.load_img) as input and converts it into a NumPy array.
# variable x will contain a NumPy array representing the image.
x=image.img_to_array(img)

# print the x
x

#The x.shape attribute is used to determine the shape or dimensions of a NumPy array
#The shape typically consists of three values: (height, width, channels) for a color image or just (height, width) for a grayscale image.
#If it's a color image, the shape will be something like (224, 224, 3), indicating a 224x224 image with 3 channels (Red, Green, Blue).
#If grayscale image output(224,224) with 1 channel

x.shape

# previously we have done rescaling for all the test dataset images.so,we have to do to the new images also
x=x/255
# print x
x

#preparing the image data for use with a deep learning model, likely one that uses the Keras framework.
x=np.expand_dims(x,axis=0)
img_data=preprocess_input(x)
img_data.shape                # to check the shape of the preprocessed image data.

#x = np.expand_dims(x, axis=0): This line uses NumPy's np.expand_dims function to add an extra dimension to your image data x. This is often done to convert a single image (which is typically 3D) into a batch of images with a batch size of 1. The axis=0 argument indicates that you want to add the new dimension as the first dimension. After this line, x will become a 4D NumPy array.

#img_data = preprocess_input(x): This line seems to be using a preprocessing function called preprocess_input on your image data x. The specific preprocessing steps depend on the model and framework you are using. It's common to apply preprocessing to normalize the pixel values or perform other operations required by the model. The result is stored in the variable img_data.

#Finally, img_data.shape is used to check the shape of the preprocessed image data. The shape will depend on the preprocessing steps applied, but it will typically be something like (1, height, width, channels) if you expanded a single image into a batch with a batch size of 1.

#used to make predictions on the input data (img_data) using a pre-trained deep learning model.
model.predict(img_data)

# model: This should be a pre-trained deep learning model that you have loaded or created earlier using TensorFlow's Keras API. The model is capable of performing various tasks such as image classification, object detection, etc., depending on how it was trained.

 #   img_data: This is the input data, typically a preprocessed image or a batch of preprocessed images, that you want to pass to the model for prediction. In your case, it seems to be the result of preprocessing a single image and expanding its dimensions, so it's a 4D NumPy array.

# When you call model.predict(img_data), the model uses its learned weights and architecture to make predictions based on the input data. The output of this operation will be the model's predictions for the provided input data. The shape and content of the predictions will depend on the specific model and task you are working on.

# For example, if you are using an image classification model, the output might be a probability distribution over classes, indicating the likelihood of each class for the given input. You can then extract information from the predictions, such as the predicted class label or class probabilities, to interpret the model's output.

# used to obtain the predicted class labels from the output of a deep learning model for a given input (img_data).
a=np.argmax(model.predict(img_data), axis=1)

# model.predict(img_data): This part of the code uses the pre-trained deep learning model (model) to make predictions on the input data (img_data). The output of this operation is a prediction, which typically includes a probability distribution over classes for each input.

 #   np.argmax(...): After making predictions, np.argmax is used to find the index (or class label) corresponding to the highest predicted probability for each input in the batch. The axis=1 argument specifies that the maximum value should be found along the second axis, which corresponds to the classes.

  #  a = ...: The result of np.argmax(model.predict(img_data), axis=1) is assigned to the variable a, so a will contain an array of predicted class labels for the inputs in img_data.

# print a(a will be an array of these predicted class labels)
a