from keras.models import model_from_json
import numpy as np
import cv2


class Network():
    def __init__(self):
        self.json_file = open('website\deeplearn\model.json', 'r')
        self.loaded_model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.loaded_model_json)
        # load weights into new model
        self.loaded_model.load_weights("website\deeplearn\model.h5")

    def prediction(self, image):
        im = cv2.resize(image, (224, 224))
        new_image = np.array(im)
        new_image = new_image.reshape(1, 224, 224, 3)
        predict = self.loaded_model.predict(new_image)
        return predict
