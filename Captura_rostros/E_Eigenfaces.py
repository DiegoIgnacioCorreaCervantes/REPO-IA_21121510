import cv2 as cv
import numpy as np
import os

data_set = "Dataset"
faces = sorted(os.listdir(data_set))
print("Personas:", faces)

labels = []
faces_data = []
label = 0

for person in faces:
    person_path = os.path.join(data_set, person)
    if not os.path.isdir(person_path):
        continue
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv.imread(img_path, 0)
        if img is None:
            continue

        #img = cv.resize(img, (100, 100), interpolation=cv.INTER_CUBIC)

        labels.append(label)
        faces_data.append(img)
    print(f"  {person} (label={label}): {labels.count(label)} imágenes")
    label += 1

face_recognizer = cv.face.EigenFaceRecognizer_create()
face_recognizer.train(faces_data, np.array(labels))
face_recognizer.write("DiegoEigenface.xml")
print("Modelo escrito: DiegoEigenface.xml")