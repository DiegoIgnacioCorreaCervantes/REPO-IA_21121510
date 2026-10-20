import cv2 as cv
import numpy as np
import os

data_set = "Dataset"
faces = sorted(
    d for d in os.listdir(data_set)
    if os.path.isdir(os.path.join(data_set, d))
)
print("Personas:", faces)

labels = []
faces_data = []
label = 0

for person in faces:
    person_path = os.path.join(data_set, person)
    for img_name in os.listdir(person_path):
        img = cv.imread(os.path.join(person_path, img_name), 0)
        if img is None:
            continue
        labels.append(label)
        faces_data.append(img)
    label += 1

face_recognizer = cv.face.FisherFaceRecognizer_create()
face_recognizer.train(faces_data, np.array(labels))
face_recognizer.write("DiegoFisherFace.xml")
print("Modelo escrito: DiegoFisherFace.xml")